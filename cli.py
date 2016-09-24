# CLI interface for working with slit_scanner.py, because GUIs r lame
#
# I've been listening to Car Seat Headrest lately. Check out "Fill in the Blank" sometime. If that's your thing.

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
parser.add_argument("-t", "--type", default=0, help="Type of slitscan to be performed. [0]=single, [1]=Moving-Horizontal, or [2]Moving-Vertical")

args = parser.parse_args()

if args.output_dir == "None":
    args.output_dir = args.input_dir

if not os.path.exists(args.input_dir):
    raise IOError("No such path: ", args.input_dir)

if not os.path.exists(args.output_dir):
    raise IOError("No such path: ", args.output_dir)

if args.output_format != "JPEG" and args.output_format != "PNG" and args.output_format != "TIFF":
    print "Unknown output format requested. Acceptable options are: JPEG, PNG, or TIFF. Defaulting to JPEG."
    args.output_format = "JPEG"
print args.output_format
print args.output_dir


test_dir = slit_scanner.make_a_glob(args.input_dir)
slit_scanner.moving_slitscan_width2(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format)
# slit_scanner.moving_slitscan(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format)

# slit_scanner.slitscan(test_dir, args.output_dir, args.slit_size, args.frame_limit, "JPEG")
