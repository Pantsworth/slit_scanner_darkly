import glob, os

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


    print "number of frames: ", len(dir_glob)
    print "first image is " + dir_glob[0]
    return dir_glob


if __name__ == '__main__':
    make_a_glob('/Users/watson/Pictures/slitscan_2016/results/vidtest5')
