__author__ = 'DoctorWatson'
from PIL import Image
import numpy,PIL,os, glob, scipy, uuid
import hickle
# import wand

def make_a_glob(root_dir):
    """
    make directories that work
    :param root_dir: directory for images
    :return: glob of images for future use
    """
    # root_dir = "/Volumes/EOS_DIGITAL/DCIM/100CANON/M06-1451/"
    if not os.path.exists(root_dir):
        print "No such path. ", root_dir

    dir_glob = glob.glob(root_dir + "*.tif")
    print dir_glob

    if len(dir_glob) == 0:
        print "tif files not found... trying dng and jpg"
        dir_glob = glob.glob(root_dir + "*.tiff")
        print dir_glob
        if len(dir_glob) == 0:      # try dng files
            dir_glob = glob.glob(root_dir + "*.dng")
            if len(dir_glob) == 0:      # try jpg files
                dir_glob = glob.glob(root_dir + "*.jpg")
                if len(dir_glob) == 0:  # try jpg files
                    dir_glob = glob.glob(root_dir + "*.jpeg")
                    if len(dir_glob) == 0:
                        dir_glob = glob.glob(root_dir + "*.PNG")

    print "number of frames: ", len(dir_glob)
    print "first image is " + dir_glob[0]
    return dir_glob


def slitscan (dir_glob, slit_size = 2, limit_frames=False, time=1.0):
    # TODO: refactor limit_frames as frame_limit
    """
    standard slitscanning functionality
    :param dir_glob: directory for images
    :param slit_size: size of slit to use for scanning
    :param limit_frames: limits number of frames to 1500 when flagged
    :param time: potential future addition
    :return: slit-scanned image
    """

    # figure out sizing (assumes sizing is long width, short height)
    first = Image.open(dir_glob[0])
    width, height = first.size
    print width, height

    # input sanitization and slicing as needed.
    if slit_size > height:
        print "Slit size exceeds height, using height"
        slit_size = height
    if slit_size < 1:
        print "Slit size must be greater than 1. Set slit to 1."
        slit_size = 1
    if height != slit_size:
        print "Height != slit size. Will slice from center..."

    # LIMIT NUMBER OF FRAMES
    if limit_frames:
        if len(dir_glob) > 1500:
            total_frames = 1500
        else:
            total_frames = len(dir_glob)
    else:
        total_frames = len(dir_glob)

    whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    print("Creating master array....")

    # total_frames = len(dir_glob)

    #make a master array with all our data
    for frame_number in xrange(total_frames):
        next_im = Image.open(dir_glob[frame_number])
        next_array = numpy.array(next_im, numpy.uint8)
        del next_im
        whole_array[frame_number, :, :, :] = next_array
        del next_array

    final_array = numpy.zeros((slit_size*total_frames, width, 3), numpy.uint8)

    # make the final image
    for frame_number in xrange(total_frames):
        next_im = Image.open(dir_glob[frame_number])
        next_array = numpy.array(next_im, numpy.uint8)
        frame_array = next_array
        del next_im
        # frame_array = whole_array[frame_number]
        if slit_size==1:
            frame_array = frame_array[height/2, :, :]
        else:
            # frame_array = frame_array[, :, :]
            frame_array = frame_array[((height/2)-(slit_size/2)):((height/2)+(slit_size/2)), :, :]
        final_array[(frame_number*slit_size):((frame_number*slit_size)+slit_size), :, :] = frame_array
        # print frame_number

    # add image to Image object, show it
    img = Image.fromarray(final_array, 'RGB')
    # img.show()

    rand_name = "/Volumes/BrutonGaster/SLITSCAN3/M03-1636-VIDEO/" + str(uuid.uuid4()) + ".tif"
    img.save(rand_name, format="TIFF")
    print "saved result as ", rand_name

    return img


def moving_slitscan(dir_glob, slit_size=2, limit_frames=False, output_format="JPEG"):
    """
    :param dir_glob: directory for images
    :param slit_size: size of slit to use for scanning
    :param limit_frames: limits number of frames to 1500 when flagged
    :param output_format: format for saving final frames
    :return: slit-scanned image
    """
    hickle_dump = False
    hickle_load = False
    hickle_path = "/Users/watson/Pictures/slitscan_2016/hickled_arrays/test.hkl"
    output_path = "/Users/watson/Pictures/slitscan_2016/results/"

    # **************************** make a new directory to write new image sequence
    vidtest_current = 0
    while os.path.exists(output_path + "vidtest" + str(vidtest_current) + "/"):
        vidtest_current += 1

    os.mkdir(output_path + "vidtest" + str(vidtest_current) + "/")
    frame_path = output_path + "vidtest" + str(vidtest_current) + "/"
    print "Made directory: ", frame_path

    # **************************** figure out sizing
    first = Image.open(dir_glob[0])
    width, height = first.size
    print "Image width is: ", width, " height is: ", height

    # **************************** input sanitization and slicing as needed
    if slit_size > height:
        print "Slit size exceeds height, using height"
        slit_size = height
    if slit_size < 1:
        print "Slit size must be greater than 1. Slit size set to 1."
        slit_size = 1
    if height != slit_size:
        print "Height != slit size. Will slice from center..."

    # LIMIT NUMBER OF FRAMES
    if limit_frames:
        if len(dir_glob) > 1500:
            total_frames = 1500
        else:
            total_frames = len(dir_glob)
    else:
        total_frames = len(dir_glob)

    # *******************  make a master array with all our data *****************
    whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    print "Creating master array....", total_frames, height, width, 3

    # hickle and non-hickle image loading
    if hickle_load:
        print "Loading hickle from ", hickle_path
        whole_array = hickle.load(hickle_path)

    else:
        for frame_number in xrange(total_frames):
            next_im = Image.open(dir_glob[frame_number])
            next_array = numpy.array(next_im, numpy.uint8)
            del next_im
            whole_array[frame_number, :, :, :] = next_array
            del next_array

    # **************************** write to hickle
    if hickle_dump:
        hickle.dump(whole_array, "/Users/watson/Pictures/slitscan_2016/hickled_arrays/test.hkl", mode='w')

    # make an array of size slit*total frames. final_image_size is a single frame
    final_image_size = numpy.zeros(((slit_size*total_frames), width, 3), numpy.uint8)

    # now we make final_frames. array of all the final frames.
    final_frames = []
    for i in range(height/slit_size):
        final_frames.append(final_image_size)

    # print "Final frame array is size: ", final_frames
    print "height/slitsize is: ", height/slit_size

    # ****for each split position:
    #   get each frame from the whole array
    #   grab a slit_size slit from it from split_position
    #   stack each slit side by side into a new array

    for slit_position in range(height/slit_size):
        final_image_size = numpy.zeros(((slit_size * total_frames), width, 3), numpy.uint8)
        for frame_number in range(total_frames):
            frame_to_split = whole_array[frame_number]
            split_result = frame_to_split[(slit_position*slit_size):(slit_position*slit_size)+slit_size, :, :]
            final_image_size[(frame_number*slit_size):(frame_number*slit_size)+slit_size,:,:] = split_result
        img = Image.fromarray(final_image_size, 'RGB')
        if output_format not in "TIFF, JPEG, PNG":
            print "No such output format. Defaulting to JPEG"
            output_format = "JPEG"

        frame_name = frame_path + str(slit_position) + "." + output_format
        img.rotate(270).save(frame_name, format=output_format)
        print "saved result as ", frame_name

#   ffmpeg finishing
#   ffmpeg -framerate 24 -i %d.JPEG -c:v libx264  out7.mp4
#   ffmpeg -framerate 24 -i %d.JPEG -c:v libx264 -s 1920x1200 out7.mp4


    # for frame_number in range(total_frames):
    #         next_array = whole_array[frame_number]
    #         final_image_size = numpy.zeros(((slit_size*total_frames), width, 3), numpy.uint8)
    #         for master_frames in range(len(final_frames)):
    #             print master_frames, "Coords: ", master_frames*slit_size, (master_frames*slit_size)+slit_size, frame_number*slit_size, (frame_number*slit_size) + slit_size
    #             split = next_array[(master_frames*slit_size):(master_frames*slit_size)+slit_size, :, :]
    #             final_frames[master_frames][(frame_number*slit_size):((frame_number*slit_size)+slit_size), :, :] = split
    #             final_image_size[(frame_number*slit_size):((frame_number*slit_size)+slit_size), :, :] = split
    #
    #         del next_array
    #
    # for frame in range(len(final_frames)):
    #     img = Image.fromarray(final_frames[frame], 'RGB')
    #     frame_name = "/Volumes/BrutonGaster/SLITSCAN4/vidtest/" + str(frame) + ".tif"
    #     img.save(frame_name, format="TIFF")
    #     print "saved result as ", frame_name
    # return

    #
    # while current_height < height:
    #     # make the final image
    #     for frame_number in xrange(total_frames):
    #         next_im = Image.open(dir_glob[frame_number])
    #         next_array = numpy.array(next_im, numpy.uint8)
    #         frame_array = next_array
    #         del next_im
    #
    #         # frame_array = whole_array[frame_number]
    #         if slit_size == 1:
    #             frame_array = frame_array[current_height, :, :]
    #         else:
    #             frame_array = frame_array[0:2, :, :]
    #         final_array[(frame_number*slit_size):((frame_number*slit_size)+slit_size), :, :] = frame_array
    #         # print frame_number
    #
    #     current_height = current_height+slit_size
    #     print "Current Height is: ", current_height

        # add image to Image object, show it
        # img = Image.fromarray(final_array, 'RGB')
        # img.show()

    #     frame_name = "/Volumes/BrutonGaster/SLITSCAN4/vidtest/" + str(current_height) + ".tif"
    #     img.save(frame_name, format="TIFF")
    #     print "saved result as ", frame_name
    # return


def moving_slitscan_width2(dir_glob, slit_size=2, limit_frames=False, output_format="JPEG"):
    """
    :param dir_glob: directory for images
    :param slit_size: size of slit to use for scanning
    :param limit_frames: limits number of frames to 1500 when flagged
    :param output_format: format for saving final frames
    :return: slit-scanned image
    """
    hickle_dump = False
    hickle_load = False
    hickle_path = "/Users/watson/Pictures/slitscan_2016/hickled_arrays/test.hkl"
    output_path = "/Users/watson/Pictures/slitscan_2016/results/"

    # **************************** make a new directory to write new image sequence
    vidtest_current = 0
    while os.path.exists(output_path + "vidtest" + str(vidtest_current) + "/"):
        vidtest_current += 1

    os.mkdir(output_path + "vidtest" + str(vidtest_current) + "/")
    frame_path = output_path + "vidtest" + str(vidtest_current) + "/"
    print "Made directory: ", frame_path

    # **************************** figure out sizing
    first = Image.open(dir_glob[0])
    width, height = first.size
    print "Image width is: ", width, " height is: ", height

    # **************************** input sanitization and slicing as needed
    if slit_size > height:
        print "Slit size exceeds height, using height"
        slit_size = height
    if slit_size < 1:
        print "Slit size must be greater than 1. Slit size set to 1."
        slit_size = 1
    if height != slit_size:
        print "Height != slit size. Will slice from center..."

    # LIMIT NUMBER OF FRAMES
    if limit_frames:
        if len(dir_glob) > 1500:
            total_frames = 1500
        else:
            total_frames = len(dir_glob)
    else:
        total_frames = len(dir_glob)

    # *******************  make a master array with all our data *****************
    whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    print "Creating master array....", total_frames, height, width, 3

    # hickle and non-hickle image loading
    if hickle_load:
        print "Loading hickle from ", hickle_path
        whole_array = hickle.load(hickle_path)

    else:
        for frame_number in xrange(total_frames):
            next_im = Image.open(dir_glob[frame_number])
            next_array = numpy.array(next_im, numpy.uint8)
            del next_im
            whole_array[frame_number, :, :, :] = next_array
            del next_array

    # **************************** write to hickle
    if hickle_dump:
        hickle.dump(whole_array, "/Users/watson/Pictures/slitscan_2016/hickled_arrays/test.hkl", mode='w')

    # make an array of size slit*total frames. final_image_size is a single frame
    final_image_size = numpy.zeros((height, (slit_size*total_frames), 3), numpy.uint8)

    # now we make final_frames. array of all the final frames.
    final_frames = []
    for i in range(width/slit_size):
        final_frames.append(final_image_size)

    # print "Final frame array is size: ", final_frames
    print "width/slitsize is: ", width/slit_size

    # ****for each split position:
    #   get each frame from the whole array
    #   grab a slit_size slit from it from split_position
    #   stack each slit side by side into a new array

    for slit_position in range(width/slit_size):
        final_image_size = numpy.zeros((height, (slit_size * total_frames), 3), numpy.uint8)
        for frame_number in range(total_frames):
            frame_to_split = whole_array[frame_number]
            split_result = frame_to_split[:, (slit_position*slit_size):(slit_position*slit_size)+slit_size, :]
            final_image_size[:,(frame_number*slit_size):(frame_number*slit_size)+slit_size,:] = split_result
        img = Image.fromarray(final_image_size, 'RGB')
        if output_format not in "TIFF, JPEG, PNG":
            print "No such output format. Defaulting to JPEG"
            output_format = "JPEG"

        frame_name = frame_path + str(slit_position) + "." + output_format
        img.save(frame_name, format=output_format)
        print "saved result as ", frame_name



def moving_slitscan_width(dir_glob, slit_size=2, limit_frames = False, time=1.0):
    """
    :param dir_glob: directory for images
    :param slit_size: size of slit to use for scanning
    :param limit_frames: limits number of frames to 1500 when flagged
    :param time: potential future addition
    :return: slit-scanned image
    """

    # figure out sizing
    first = Image.open(dir_glob[0])
    width, height = first.size
    print "Image width is: ", width, " height is: ", height


    # input sanitization and slicing as needed.
    if slit_size > height:
        print "Slit size exceeds height, using height"
        slit_size = height
    if slit_size < 1:
        print "Slit size must be greater than 1. Slit size set to 1."
        slit_size = 1
    if height != slit_size:
        print "Height != slit size. Will slice from center..."

    # LIMIT NUMBER OF FRAMES
    if limit_frames:

        if len(dir_glob) > 1500:
            total_frames = 1500
        else:
            total_frames = len(dir_glob)
    else:
        total_frames = len(dir_glob)

    # make a master array with all our data
    whole_array = numpy.zeros((total_frames, height, width, 3), numpy.uint8)
    print "Creating master array, dimensions: ", total_frames, height, width, 3

    for frame_number in xrange(total_frames):
        next_im = Image.open(dir_glob[frame_number])
        next_array = numpy.array(next_im, numpy.uint8)
        del next_im
        whole_array[frame_number, :, :, :] = next_array
        del next_array
        print "Frame number:", frame_number

    final_array = numpy.zeros((height, slit_size*total_frames, 3), numpy.uint8)
    current_width = 0

    while current_width < height:
        # make the final image
        for frame_number in xrange(total_frames):
            # next_im = Image.open(dir_glob[frame_number])
            # next_array = numpy.array(next_im, numpy.uint8)
            # frame_array = next_array
            # del next_im

            frame_array = whole_array[frame_number]
            if slit_size == 1:
                frame_array = frame_array[:, current_width, :]
            else:
                frame_array = frame_array[:, current_width:current_width+slit_size, :]
            final_array[(frame_number*slit_size):((frame_number*slit_size)+slit_size), :, :] = frame_array

        current_width = current_width+slit_size

        img = Image.fromarray(final_array, 'RGB')
        # img.show()

        frame_name = "~/Pictures/Slitscan_2016/results/" + str(current_width) + ".tif"
        img.save(frame_name, format="TIFF")
        print "saved result as ", frame_name

    return

# ******************* future compatibility with video files *********************************
# def slitscan_movie (video_file, slit_size = 2, time=1.0):
#     """
#     :param video_file: movie file
#     :param slit_size: size of slit to use for scanning
#     :param time: potential future addition
#     :return:
#     """
#
#     # figure out sizing
#     # x = 0
#     # clip = VideoFileClip(video_file)
#     # video_array = clip.iter_frames(fps=None, with_times=False, progress_bar=False, dtype='uint8')
#     # print video_array
#     # for number in xrange(video_array):
#     #     new = number
#     #     pass
#
#     width, height = video_array.size
#     print width, height
#
#     if slit_size > height:
#         print "slit size exceeds height, using height"
#         slit_size = height
#     if slit_size < 1:
#         print "Slit size must be greater than 1. Set slit to 1."
#         slit_size = 1
#     if height != slit_size:
#         print "Height != slit size. Slicing from center..."
#
#     whole_array = numpy.zeros((len(dir_glob), height, width, 3), numpy.uint8)
#     print("Creating master array....")
#
#     total_frames = len(dir_glob)
#
#     # make a master array with all our data
#     for frame_number in xrange(total_frames):
#         next_im = Image.open(dir_glob[frame_number])
#         next_array = numpy.array(next_im, numpy.uint8)
#         del next_im
#         whole_array[frame_number, :, :, :] = next_array
#         del next_array
#
#     final_array = numpy.zeros((slit_size*total_frames, width, 3), numpy.uint8)
#
#     # make the final image
#     for frame_number in xrange(total_frames):
#         # next_im = Image.open(dir_glob[frame_number])
#         # frame_array = numpy.array(next_im, numpy.uint8)
#         frame_array = whole_array[frame_number]
#         if slit_size==1:
#             frame_array = frame_array[height/2, :, :]
#         else:
#             frame_array = frame_array[((height/2)-(slit_size/2)):((height/2)+(slit_size/2)), :, :]
#         final_array[(frame_number*slit_size):((frame_number*slit_size)+slit_size), :, :] = frame_array
#
#     img = Image.fromarray(final_array, 'RGB')
#     img.show()
#
#     img.save('/Users/DoctorWatson/IMTEST/done.tif', "TIFF")
#     return img