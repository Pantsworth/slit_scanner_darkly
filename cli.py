# CLI interface for working with slit_scanner.py, because GUIs r lame

import argparse
import slit_scanner
import os


parser = argparse.ArgumentParser()
parser._optionals.title = 'arguments'

parser.add_argument("-i", "--input_dir", help="Input directory. Set of frames or a single video. Tests for frames first.", required=True)
parser.add_argument("-o", "--output_dir", default="None", help="Path for output frames (optional) Default: Subdir of input)")
parser.add_argument("-slit", "--slit_size", default=5, type=int, help="Slit Size (optional)")
parser.add_argument("-l", "--frame_limit", default=-1, type=int, help="Limit number of frames to specified int (optional)")
parser.add_argument("-format", "--output_format", default="JPEG", help="Output image format. (optional)")
parser.add_argument("-t", "--type", default="0", help="Type of slitscan to be performed. [0]=single-vertical, [1]=single-horizontal [2]=Moving-Horizontal, [3]=Moving-Vertical, [4]=Moving-Both (Vertical AND Horizontal)")

args = parser.parse_args()

if args.output_dir == "None":
    args.output_dir = args.input_dir

if not os.path.exists(args.input_dir):
    raise IOError("No such path: ", args.input_dir)

if not os.path.exists(args.output_dir):
    raise IOError("No such path: ", args.output_dir)

if args.output_format.lower() != "jpeg" and args.output_format.lower() != "png" and args.output_format.lower() != "tiff":
    print "Unknown output format requested. Acceptable options are: JPEG, PNG, or TIFF. Defaulting to JPEG."
    args.output_format = "JPEG"

args.type = args.type.lower()

if args.type == "single-vertical" or args.type == "0":
    print "\nPerforming single slitscan (vertical)"
    test_dir = slit_scanner.make_a_glob(args.input_dir)
    slit_scanner.slitscan(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format, True, False)

if args.type == "single-horizontal" or args.type == "1":
    print "\nPerforming single slitscan (horizontal)"
    test_dir = slit_scanner.make_a_glob(args.input_dir)
    slit_scanner.slitscan(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format, False, True)

elif args.type == "moving-horizontal" or args.type == "2":
    print "\nPerforming moving-horizontal slitscan. HORIZONTAL slices."
    test_dir = slit_scanner.make_a_glob(args.input_dir)
    slit_scanner.moving_slitscan_both(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format, True, False)

elif args.type == "moving-vertical" or args.type == "3":
    print "\nPerforming moving-vertical slitscan. VERTICAL slices."
    test_dir = slit_scanner.make_a_glob(args.input_dir)
    slit_scanner.moving_slitscan_both(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format, False, True)

elif args.type == "moving-both" or args.type == "4":
    print "\nPerforming both moving-vertical and moving-horizontal slitscans, without having to reload everything."
    test_dir = slit_scanner.make_a_glob(args.input_dir)
    slit_scanner.moving_slitscan_both(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format, True, True)
