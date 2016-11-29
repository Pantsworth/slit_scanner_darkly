import numpy, os, glob
import sys
import random
from PIL import Image
from timeit import default_timer as timer
from multiprocessing import Process, Pool


def make_a_glob(root_dir):
    """
    Creates a glob of images from specified path. Checks for JPEG, PNG, TIFF, DNG
    :param root_dir: path to set of images
    :return: glob of images from input path
    """
    if not os.path.exists(root_dir):
        raise IOError("No such path: %s" % root_dir)

    if not root_dir.endswith("/"):
        root_dir += "/"

    dir_glob = glob.glob(root_dir + "*.tif")
    extension_list = ["*.tiff", "*.tif", "*.jpeg", "*.png", "*.jpg", "*.dng"]

    for ext in extension_list:
        if len(dir_glob) == 0:
            dir_glob = glob.glob(root_dir + ext)
            if len(dir_glob) == 0:
                dir_glob = glob.glob(root_dir + ext.upper())
            if ext == extension_list[(len(extension_list) - 1)] and len(dir_glob) == 0:
                raise IOError("No images found in directory: %s" % root_dir)
        else:
            break

    print "First image is: " + dir_glob[0]
    print "Number of frames found: ", len(dir_glob)
    return dir_glob


def get_frame_limit(limit_frames, globsize):
    """
    Determines a limit on the number of frames
    :param limit_frames:
    :param globsize:
    :return:
    """
    if limit_frames != -1:
        if globsize > limit_frames:
            total_frames = limit_frames
            print "Frames limited to ", limit_frames
        else:
            print "Frame limit of", limit_frames, "is higher than total # of frames: ", globsize
            total_frames = globsize
    else:
        total_frames = globsize

    return total_frames


def get_slit_fixes_height(slit_size, height, width):
    current_slit = 0
    if slit_size > height:
        print "Slit size exceeds height, using height"
        current_slit = height
    if slit_size < 1:
        print "Slit size must be greater than 1. Slit size set to 1."
        current_slit = 1
    if height != slit_size:
        print "Height != slit size. Will slice from center..."
        current_slit = slit_size
    else:
        current_slit = slit_size
    return current_slit


def get_slit_fixes_width(slit_size, height, width):
    current_slit = 0
    if slit_size > width:
        print "Slit size exceeds width, using width"
        current_slit = width
    if slit_size < 1:
        print "Slit size must be greater than 1. Slit size set to 1."
        current_slit = 1
    if width != slit_size:
        print "width != slit size. Will slice from center..."
        current_slit = slit_size
    else:
        current_slit = slit_size
    return current_slit


def get_frame_size_bytes(dir_glob):
    first = Image.open(dir_glob[0])
    first_array = numpy.array(first, numpy.uint8)
    return first_array.nbytes


def make_output_dir(output_dir):
    """
    Creates uniquely-named new folder along specified path
    :param output_dir: output path
    :return: path to new folder
    """
    if output_dir[len(output_dir)-1] != "/":
        output_dir = output_dir + "/"

    output_path = output_dir

    # **************************** make a new directory to write new image sequence ************************
    slitscan_current = 0
    while os.path.exists(output_path + "slitscan" + str(slitscan_current) + "/"):
        slitscan_current += 1

    os.mkdir(output_path + "slitscan" + str(slitscan_current) + "/")
    frame_path = output_path + "slitscan" + str(slitscan_current) + "/"
    print "Made directory: ", frame_path
    return frame_path


def do_sizing(dir_glob):
    first = Image.open(dir_glob[0])
    width, height = first.size
    print "width is: ", width," height is: ", height
    return width, height


# handy code by Vladimir Ignatyev, found here: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, suffix=''):
    """
    Creates and displays a progress bar in console log.
    :param count: parts completed
    :param total: parts to complete
    :param suffix: any additional descriptors
    :return:
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def save_single(final_array_in, frame_path, output_format):
    """
    Save single slitscan from either height or width process
    :param final_array_in: final array from slitscan function (all the slitscan data)
    :param frame_path: path to send frames to
    :param output_format: JPEG, PNG, or TIFF
    :return: final image
    """
    img = Image.fromarray(final_array_in, 'RGB')
    current_slitscan = 0
    while os.path.exists(frame_path + "single_slitscan" + str(current_slitscan) + output_format):
        current_slitscan += 1
    frame_path = frame_path + "single_slitscan" + str(current_slitscan) + "." + output_format
    img.save(frame_path, format=output_format)
    print "saved result as ", frame_path
    print('\a')
    return img


def slitscan(dir_glob, output_dir, slit_size, limit_frames, output_format, do_height=False, do_width=False):
    """
    standard slitscanning functionality.
    :param dir_glob: directory for images
    :param output_dir: directory for output
    :param slit_size: size of slit to use for scanning
    :param limit_frames: limits number of frames to chosen #
    :param output_format: JPEG, PNG, or TIFF
    :param do_height: perform height-slitscan
    :param do_width: perform width-slitscan
    :return: single slit-scanned image
     ____________________________________
    |                |                  |
    |                |                  |
    |                |                  |
    |                |                  |
    |                |                  |
    |                |                  |
    |________________|__________________|
                     x
        (slit position - always taken from middle)
    """

    frame_path = make_output_dir(output_dir)

    width, height = do_sizing(dir_glob)


    # LIMIT NUMBER OF FRAMES
    total_frames = get_frame_limit(limit_frames, len(dir_glob))

    # whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    # print("Creating master array....")
    # ********************** make a master array with all our data
    # for frame_number in xrange(total_frames):
    #     next_im = Image.open(dir_glob[frame_number])
    #     next_array = numpy.array(next_im, numpy.uint8)
    #     del next_im
    #     whole_array[frame_number, :, :, :] = next_array
    #     del next_array
    #     progress(frame_number, total_frames)

    if not do_height and not do_width:
        print "do_height and do_width are both False. do_height set to True."
        do_height = True

    if do_height:
        slit_size = get_slit_fixes_height(slit_size, height, width)
        final_array = numpy.zeros((slit_size*total_frames, width, 3), numpy.uint8)
        # **********************    make the final image   **********************
        for frame_number in xrange(total_frames):
            next_im = Image.open(dir_glob[frame_number])
            next_array = numpy.array(next_im, numpy.uint8)  # open and read image
            frame_array = next_array
            del next_im
            # frame_array = whole_array[frame_number]

            if slit_size == 1:
                frame_array = frame_array[height/2, :, :]
            else:
                # frame_array = frame_array[, :, :]
                if slit_size % 2 != 0:
                    frame_array = frame_array[((height/2)-(slit_size/2))-1:((height/2)+(slit_size/2)), :, :]
                else:
                    frame_array = frame_array[((height/2)-(slit_size/2)):((height/2)+(slit_size/2)), :, :]
            final_array[(frame_number*slit_size):((frame_number*slit_size)+slit_size), :, :] = frame_array
            progress(frame_number, total_frames)

        result = save_single(final_array, frame_path, output_format)

    if do_width:
        final_array = []
        slit_size = get_slit_fixes_width(slit_size, height, width)
        final_array = numpy.zeros((height, slit_size * total_frames, 3), numpy.uint8)

        # **********************    make the final image   **********************
        for frame_number in xrange(total_frames):
            next_im = Image.open(dir_glob[frame_number])
            next_array = numpy.array(next_im, numpy.uint8)  # open and read image
            frame_array = next_array
            del next_im
            # frame_array = whole_array[frame_number]

            if slit_size == 1:
                frame_array = frame_array[:, width / 2, :]
            else:
                # frame_array = frame_array[, :, :]
                if slit_size % 2 != 0:
                    frame_array = frame_array[:, ((width / 2) - (slit_size / 2)) - 1:((width / 2) + (slit_size / 2)), :]
                else:
                    frame_array = frame_array[:, ((width / 2) - (slit_size / 2)):((width / 2) + (slit_size / 2)), :]
            final_array[:, (frame_number * slit_size):((frame_number * slit_size) + slit_size), :] = frame_array
            progress(frame_number, total_frames)

        result = save_single(final_array, frame_path, output_format)
    return result


def moving_slitscan_both(dir_glob, output_dir, slit_size, limit_frames, output_format, do_height=False, do_width=False):
    """
    makes moving slitscans for height, width or both!

    :param dir_glob: directory for images
    :param output_dir: output directory
    :param slit_size: size of slit to use for scanning
    :param limit_frames: limits number of frames to <limit_frames>
    :param output_format: format for saving final frames
    :param do_height: do the height slitscan
    :param do_width: do the width slitscan
    :return:

    if do_height:
    set of slitscanned images, where each image is assembled by slitscanning from a different
    y-coordinate of the image each time
     ___________________________________
    |                                   |
    |___________________________________| = y coord
    |                                   |
    |                                   |
    |                                   |
    |                                   |
    |___________________________________|
          x =>
        (slit position)


    if do_width:
    set of slitscanned images, where each image is assembled by slitscanning from a different
    x-coordinate of the image each time
     ___________________________________
    |     |                             |
    |     |                             |
    |     |                             |
    |     |                             |
    |     |                             |
    |     |                             |
    |_____|_____________________________|
          x =>
        (slit position)

    # ****for each split position:
    #   get each frame from the whole array
    #   grab a slit_size slit from it from split_position
    #   stack each slit side by side into a new array

    """
    frame_path = make_output_dir(output_dir)

    # **************************** figure out sizing *******************************************************
    width, height = do_sizing(dir_glob)

    # ******************************** LIMIT NUMBER OF FRAMES ********************************
    total_frames = get_frame_limit(limit_frames, len(dir_glob))

    # *******************  make a master array with all our data *****************
    whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    print "Creating master array....", total_frames, height, width, 3

    for frame_number in xrange(total_frames):
        next_im = Image.open(dir_glob[frame_number])
        next_array = numpy.array(next_im, numpy.uint8)
        del next_im
        whole_array[frame_number, :, :, :] = next_array
        del next_array
        progress(frame_number, total_frames)

    print "\nCreating images..."

    if not do_height and not do_width:
        print "Neither height nor width selected. Doing moving height slitscan anyway."
        do_height = True

    if output_format.upper() not in "TIFF, JPEG, PNG":
        print "No such output format. Defaulting to JPEG"
        output_format = "JPEG"

    if do_height:
        print "\nheight/slitsize is: ", height / slit_size
        slit_size = get_slit_fixes_height(slit_size, height, width)
        os.mkdir(frame_path + "height/")
        for slit_position in range(height/slit_size):
            final_image_size = numpy.zeros(((slit_size * total_frames), width, 3), numpy.uint8)
            for frame_number in range(total_frames):
                frame_to_split = whole_array[frame_number]
                split_result = frame_to_split[(slit_position*slit_size):(slit_position*slit_size)+slit_size, :, :]
                final_image_size[(frame_number*slit_size):(frame_number*slit_size)+slit_size,:,:] = split_result
            img = Image.fromarray(final_image_size, 'RGB')
            frame_name = frame_path + "height/" + str(slit_position) + "." + output_format
            img = img.rotate(-90, expand=1)
            img.save(frame_name, format=output_format)
            progress(slit_position, height/slit_size)
        print('\a')  # make a sound (at least on mac...)

    if do_width:
        slit_size = get_slit_fixes_width(slit_size, height, width)
        os.mkdir(frame_path + "width/")
        for slit_position in range(width/slit_size):
            final_image_size = numpy.zeros((height, (slit_size * total_frames), 3), numpy.uint8)
            for frame_number in range(total_frames):
                frame_to_split = whole_array[frame_number]
                split_result = frame_to_split[:, (slit_position*slit_size):(slit_position*slit_size)+slit_size, :]
                final_image_size[:,(frame_number*slit_size):(frame_number*slit_size)+slit_size,:] = split_result
            img = Image.fromarray(final_image_size, 'RGB')
            frame_name = frame_path + "width/" + str(slit_position) + "." + output_format
            img.save(frame_name, format=output_format)
            progress(slit_position, width/slit_size)
        print('\a')  # make a sound (at least on mac...)
    return frame_path


def frame_smasher(dir_glob, output_dir, slit_size, limit_frames, output_format, framesmash_width, framesmash_height):
    """
    smash the frames into random slices appearing at random intervals.

    :param dir_glob: directory for images
    :param output_dir: output directory
    :param slit_size: size of slit to use for scanning
    :param limit_frames: limits number of frames to <limit_frames>
    :param output_format: format for saving final frames
    :param framesmash_width: flag for doing width-based frame smashing
    :param framesmash_height: flag for height-based frame smashing
    :return: set of images, divided into rectangles playing back the video at different times.
    """
    frame_path = make_output_dir(output_dir)

    rect_low = 10
    rect_high = 300

    # if not framesmash_width and not framesmash_height:
    #     print "Both framesmash_width and framesmash_height are False. Defaulting to framesmash_width"
    #     framesmash_width = 1

    framesmash_both = 0
    framesmash_irregular = 0
    framesmash_space = 1

    # **************************** SIZING *******************************************************
    first = Image.open(dir_glob[0])
    width, height = first.size
    print "Image width is: ", width, " height is: ", height

    # **************************** FRAMESMASHER - width *******************************************************
    if framesmash_width:
        os.mkdir(frame_path + "width/")
        dividing_line = 0
        dividing_list_width = []
        while dividing_line < height:
            rand_val = random.randrange(rect_low,rect_high,1)
            dividing_list_width.append(rand_val)
            dividing_line += rand_val
            if dividing_line > height:
                dividing_list_width[len(dividing_list_width)-1] -= (dividing_line-height)
        print "Dividing list-width: ", dividing_list_width

    # **************************** FRAMESMASHER - HEIGHT *******************************************************
    if framesmash_height:
        os.mkdir(frame_path + "height/")
        dividing_line = 0
        dividing_list_height = []
        while dividing_line < width:
            rand_val = random.randrange(rect_low, rect_high, 1)
            dividing_list_height.append(rand_val)
            dividing_line += rand_val
            if dividing_line > width:
                dividing_list_height[len(dividing_list_height) - 1] -= (dividing_line - width)
        print "Dividing list-height: ", dividing_list_height

        # **************************** FRAMESMASHER - RANDOM *******************************************************
    if framesmash_irregular or framesmash_space:
        os.mkdir(frame_path + "width/")
        dividing_line = 0
        dividing_list_width = []
        while dividing_line < height:
            rand_val = random.randrange(rect_low,rect_high,1)
            dividing_list_width.append(rand_val)
            dividing_line += rand_val
            if dividing_line > height:
                dividing_list_width[len(dividing_list_width)-1] -= (dividing_line-height)
        print "Dividing list-width: ", dividing_list_width

    # ******************************** LIMIT NUMBER OF FRAMES ********************************
    total_frames = get_frame_limit(limit_frames, len(dir_glob))

    # if limit_frames != -1:
    #     if len(dir_glob) > limit_frames:
    #         total_frames = limit_frames
    #         print "Frames limited to ", limit_frames
    #     else:
    #         print "Frame limit of", limit_frames,"is higher than total # of frames: ", len(dir_glob)
    #         total_frames = len(dir_glob)
    # else:
    #     total_frames = len(dir_glob)

    max_frame_offset = total_frames
    print "Max frame offset is: ", max_frame_offset

    # *******************  MAKE MASTER ARRAY *****************
    whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    print "Creating master array....", total_frames, height, width, 3
    print "\n"

    for frame_number in xrange(total_frames):
        next_im = Image.open(dir_glob[frame_number])
        next_array = numpy.array(next_im, numpy.uint8)
        del next_im
        whole_array[frame_number, :, :, :] = next_array
        del next_array
        progress(frame_number, total_frames)

    if framesmash_width and framesmash_height:
        whole_array2 = whole_array
    # ******************************** MAKE FINAL IMAGES ********************************
    # print "Final frame array is size: ", final_frames
    print "Creating final images..."

    if framesmash_width:
        width_whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
        marker_total = 0
        # whole_array[frames, height, width, 3]
        for marker in dividing_list_width:
            width_whole_array[:, marker_total:marker_total + marker, :, :] = numpy.roll(
                whole_array[:, marker_total:marker_total + marker, :, :], random.randrange(0, max_frame_offset, 1), axis=0)
            marker_total += marker

        for frame in range(total_frames):
            img = width_whole_array[frame]
            # print "IMG dimensions: ", img
            final_img = Image.fromarray(img, 'RGB')
            frame_name = frame_path + "width/" + str(frame) + "." + output_format
            final_img.save(frame_name, format=output_format)
            progress(frame, total_frames)

    if framesmash_height:
        marker_total = 0
        # whole_array[frames, height, width, 3]
        for marker in dividing_list_height:
            whole_array2[:, :, marker_total:marker_total + marker, :] = numpy.roll(
                whole_array2[:, :, marker_total:marker_total + marker, :], random.randrange(0, max_frame_offset, 1),
                axis=0)
            marker_total += marker

        for frame in range(total_frames):
            img = whole_array2[frame]
            # print "IMG dimensions: ", img
            final_img = Image.fromarray(img, 'RGB')
            frame_name = frame_path + "height/" + str(frame) + "." + output_format
            final_img.save(frame_name, format=output_format)
            progress(frame, total_frames)

    if framesmash_irregular:
        marker_total = 0
        for marker in dividing_list_height:
            whole_array2[:, :, marker_total:marker_total + marker, :] = numpy.roll(
                whole_array2[:, :, marker_total:marker_total + marker, :], random.randrange(0, max_frame_offset, 1),
                axis=0)
            marker_total += marker

        for frame in range(total_frames):
            img = whole_array2[frame]
            # print "IMG dimensions: ", img
            final_img = Image.fromarray(img, 'RGB')
            frame_name = frame_path + "height/" + str(frame) + "." + output_format
            final_img.save(frame_name, format=output_format)
            progress(frame, total_frames)

    if framesmash_space:
        # whole_array[frames, height, width, 3]
        space_whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)

        slots = list(dividing_list_width)
        random.shuffle(slots)
        slots_taken = numpy.zeros((len(dividing_list_width)-1))

        marker_orig_total = 0
        for marker in dividing_list_width:
            for value in range(len(slots)-1):
                if marker == slots[value] and slots_taken[value] == 0:
                    print dividing_list_width, "\n", slots_taken, "\n", slots
                    slots_taken[value] = 1
                    marker_total = sum(slots[0:value])
                    if marker_total == 0:
                        print marker_total
                    space_whole_array[:, marker_total:marker_total + marker, :, :] = whole_array[:, marker_orig_total:marker_orig_total + marker, :, :]
                    marker_orig_total += marker

        for frame in range(total_frames):
            img = space_whole_array[frame]
            # print "IMG dimensions: ", img
            final_img = Image.fromarray(img, 'RGB')
            frame_name = frame_path + str(frame) + "." + output_format
            final_img.save(frame_name, format=output_format)
            progress(frame, total_frames)


    if framesmash_both:
        marker_total = 0
        # whole_array[frames, height, width, 3]
        for marker in dividing_list_width:
            whole_array[:, marker_total:marker_total + marker, :, :] = numpy.roll(
                whole_array[:, marker_total:marker_total + marker, :, :], random.randrange(0, max_frame_offset, 1), axis=0)
            marker_total += marker
        marker_total = 0
        # whole_array[frames, height, width, 3]
        for marker in dividing_list_height:
            whole_array[:, :, marker_total:marker_total + marker, :] = numpy.roll(
                whole_array[:, :, marker_total:marker_total + marker, :], random.randrange(0, max_frame_offset, 1),
                axis=0)
            marker_total += marker

        for frame in range(total_frames):
            img = whole_array[frame]
            # print "IMG dimensions: ", img
            final_img = Image.fromarray(img, 'RGB')
            frame_name = frame_path + "height/" + str(frame) + "." + output_format
            final_img.save(frame_name, format=output_format)
            progress(frame, total_frames)

    print('\a')
    return frame_path


def lowmem_moving_slitscan(dir_glob, output_dir, slit_size, limit_frames, output_format, ram_limit=4000000000):
    # TODO: make low memory version
    """
    a slower but significantly more memory-efficient variant.

    :param dir_glob: directory for images
    :param output_dir: directory for output
    :param slit_size: size of slit to use for scanning
    :param output_format: format for saving final frames
    :param limit_frames: limits number of frames to <value>
    :return: set of slitscanned images, where each image is assembled by slitscanning from a different
    y-coordinate of the image each time
     ___________________________________
    |                                   |
    |___________________________________| = y coord
    |                                   |
    |                                   |
    |                                   |
    |                                   |
    |___________________________________|
          x =>
        (slit position)
    """
    # **************************** make a new directory to write new image sequence
    frame_path = make_output_dir(output_dir)

    # **************************** figure out sizing
    width, height = do_sizing(dir_glob)

    # **************************** input sanitization and slicing as needed
    slit_size = get_slit_fixes_height(slit_size, height, width)

    # LIMIT NUMBER OF FRAMES
    total_frames = get_frame_limit(limit_frames, len(dir_glob))

    # ***** future code for adding slitscan_array to memory considerations
    # print "Making final slitscan frames..."
    # final_image_size = numpy.zeros(((slit_size * total_frames), width, 3), numpy.uint8)
    # slitscan_bytes = final_image_size.nbytes
    # slitscan_frames = ram_limit / slitscan_bytes
    # slitscan_array = []
    # for frame_number in range(slitscan_frames):
    #     slitscan_array = slitscan_array.append(numpy.zeros(((slit_size * total_frames), width, 3), numpy.uint8))
    #
    # for slit_position in range(height/slit_size):
    #     img = Image.fromarray(final_image_size, 'RGB')
    #     frame_name = frame_path + str(slit_position) + "." + output_format
    #     # img = img.rotate(-90, expand=1)
    #     img.save(frame_name, format=output_format)

    # for each video frame:
    #   open frame
    #   for each output frame:
    #       open output frame
    #       add info from opened video frame
    #       close output frame
    #   close video frame

    # ***************** grab a limited number of frames, up to mem_limit worth *********
    partial_video_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    video_frame_size = get_frame_size_bytes(dir_glob)
    ram_frames = ram_limit / video_frame_size
    remaining_frames = total_frames
    frame_offset = 0
    if ram_frames > total_frames:
        ram_frames = total_frames

    while remaining_frames != 0:
        print "Ram frames: %s, Remaining Frames: %s, Frame offset: %s" % (ram_frames, remaining_frames, frame_offset)

        for video_frame in range(ram_frames):
            next_array = numpy.array(Image.open(dir_glob[video_frame + frame_offset]), numpy.uint8)
            partial_video_array[video_frame, :, :, :] = next_array

        for frame_number in range(ram_frames):
            for slit_position in range(height/slit_size):
                frame_to_split = partial_video_array[frame_number]
                split_result = frame_to_split[(slit_position*slit_size):(slit_position*slit_size)+slit_size, :, :]

                frame_name = frame_path + str(slit_position) + "." + output_format
                slit_array = numpy.array(Image.open(frame_name), numpy.uint8)
                slit_array[((frame_number+frame_offset) * slit_size):((frame_number+frame_offset) * slit_size) + slit_size, :, :] = split_result
                slit_img = Image.fromarray(slit_array, 'RGB')
                slit_img.save(frame_name, format=output_format)
            progress(frame_number, total_frames)

        frame_offset += ram_frames
        remaining_frames -= ram_frames

    # print "Making final slitscan frames..."
    # final_image_size = numpy.zeros(((slit_size * total_frames), width, 3), numpy.uint8)
    # for slit_position in range(height/slit_size):
    #     img = Image.fromarray(final_image_size, 'RGB')
    #     frame_name = frame_path + str(slit_position) + "." + output_format
    #     # img = img.rotate(-90, expand=1)
    #     img.save(frame_name, format=output_format)
    #
    # print "\nheight/slitsize is: ", height/slit_size
    # print "Creating images..."
    #
    # for frame_number in xrange(total_frames):
    #     next_im = Image.open(dir_glob[frame_number])
    #     next_array = numpy.array(next_im, numpy.uint8)
    #
    #     for slit_position in range(height/slit_size):
    #         print slit_position
    #         # open final slitscan frame
    #         frame_name = frame_path + str(slit_position) + "." + output_format
    #         slit_image = Image.open(frame_name)
    #         slit_array = numpy.array(slit_image)
    #         # split the video frame
    #         split_result = next_array[(slit_position*slit_size):(slit_position*slit_size)+slit_size, :, :]
    #         print "split result: ", split_result.shape
    #
    #         slit_array[(frame_number*slit_size):(frame_number*slit_size)+slit_size, :, :] = split_result
    #         # save slitscan frame
    #         slit_img = Image.fromarray(slit_array, 'RGB')
    #         # slit_img = slit_img.rotate(-90, expand=1)
    #         slit_img.save(frame_name, format=output_format)
    #     progress(frame_number, total_frames)

    print('\a')  # make a sound (at least on mac...)
    return frame_path


def conventional_slitscan(dir_glob, output_dir, limit_frames, output_format):
    frame_path = make_output_dir(output_dir)

    # **************************** figure out sizing *******************************************************
    width, height = do_sizing(dir_glob)

    # ******************************** LIMIT NUMBER OF FRAMES ********************************
    total_frames = get_frame_limit(limit_frames, len(dir_glob))

    # *******************  make a master array with all our data *****************
    whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    print "Creating master array....", total_frames, height, width, 3

    for frame_number in xrange(total_frames):
        next_im = Image.open(dir_glob[frame_number])
        next_array = numpy.array(next_im, numpy.uint8)
        del next_im
        whole_array[frame_number, :, :, :] = next_array
        del next_array
        progress(frame_number, total_frames)

    current_step = 0
    step = height/255
    current_time = 255
    # for line in range(height/step):
    #     whole_array[:, current_step:current_step+step, :, :] = numpy.roll(whole_array[:, current_step:current_step+step, :, :], current_time, axis=0)
    #     current_step += step
    #     current_time -= 1
    #     print current_step, current_time


    # for line in range(height/step):
    #     whole_array[:, current_step:current_step+step, :, :] = numpy.roll(whole_array[:, current_step:current_step+step, :, :], current_time, axis=0)
    #     current_step += step
    #     if line < (height/step)/2:
    #         current_time -= 1
    #     else:
    #         current_time +=1
    #     print current_step, current_time

    # step = width/255
    # for line in range(width):
    #     whole_array[:, :, current_step:current_step+step, :] = numpy.roll(whole_array[:, :, current_step:current_step+step, :], current_time, axis=0)
    #     current_step += 1
    #     if line < (width/2):
    #         current_time -=1
    #     else:
    #         current_time +=1
    #     print current_step, current_time

    # CIRCULAR SLITSCAN
    center = [height/2, width/2]
    for xcord in range(width):
        for ycord in range(height):
            current_time = int(((((center[0]-ycord)**2)+((center[1]-xcord)**2)) ** 0.5))
            # current_time = int((((((center[0]-ycord)**2)+((center[1]-xcord)**2))) / (width**2 + height**2)))
            whole_array[:, ycord, xcord, :] = numpy.roll(whole_array[:, ycord, xcord, :], current_time, axis=0)

    for frame in range(total_frames):
        img = whole_array[frame]
        # print "IMG dimensions: ", img
        final_img = Image.fromarray(img, 'RGB')
        frame_name = frame_path + str(frame) + "." + output_format
        final_img.save(frame_name, format=output_format)
        progress(frame, total_frames)


def make_a_video(output_dir, output_format, name):
    if not output_dir.endswith("/"):
        output_dir += "/"
    os.system('ffmpeg -r 24 -i ' + output_dir + '%d.' + output_format + ' -c:v libx264 ' + output_dir + name)
    #   ffmpeg finishing
    #   ffmpeg -framerate 24 -i %d.JPEG -c:v libx264  out7.mp4
    #   ffmpeg -framerate 24 -i %d.JPEG -c:v libx264 -s 1920x1200 out7.mp4