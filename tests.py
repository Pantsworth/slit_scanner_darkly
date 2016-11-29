__author__ = 'Michael Nowakowski'

import unittest, os
import slit_scanner
import time

from moviepy.editor import VideoFileClip


class TestSystem(unittest.TestCase):
    def test_globbing(self):
        find_jpegs = slit_scanner.make_a_glob("./img/")
        test_result = "['./img/single_slitscan-height-bridge.JPEG', './img/single_slitscan-height.JPEG', './img/single_slitscan-width-bridge.JPEG', './img/single_slitscan-width.JPEG']"
        self.assertEqual(str(find_jpegs), test_result)

    def test_system(self):
        pass
        # test_dir = slit_scanner.make_a_glob("/Volumes/Peregrin/slitscan_2016/chicago/c142_frames/")
        # slit_scanner.moving_slitscan(test_dir,"/Volumes/Peregrin/slitscan_2016/results-gandalf/", 10, -1, "JPEG")
        #
        # test_dir2 = slit_scanner.make_a_glob("/Volumes/Peregrin/slitscan_2016/inputs/earth")
        # # slit_scanner.temporal_median_filter_multi2(test_dir2, "/Volumes/Peregrin/slitscan_2016/results-gandalf/", 100, "JPEG",)
        # slit_scanner.conventional_slitscan(test_dir2, "/Volumes/Peregrin/slitscan_2016/results-gandalf/", 600, "JPEG",)


        # dir = practice.make_a_glob("/Volumes/EOS_DIGITAL/DCIM/100CANON/M07-20/")

        # slit_scanner.slitscan(dir, 2, True)

        # dir = slit_scanner.make_a_glob("/Volumes/BrutonGaster/2015 Part 2/9-6-15 Slitscanning Night/M07-0021_C0000/")
        # # dir = practice.make_a_glob("/Volumes/EOS_DIGITAL/DCIM/100CANON/M07-20/")
        #
        # slit_scanner.slitscan(dir, 6, True)

        #
        # with Raw(filename='/Volumes/BrutonGaster/2015 Part 2/8-8-15 Slit Scanning Waves/M08-1206_C0000.dng') as im:
        #     print im.metadata
        #     # im = im.to_buffer()
        #     # im = numpy.array(im)
        #     # im = im.reshape((2,1824))
        #     im.save(filename="/Users/DoctorWatson/Pictures/nerds.tif", filetype='tiff')
        #     print "did that"
