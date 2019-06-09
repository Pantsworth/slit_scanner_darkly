"""
Interface for interacting with the slit_scanner.

"""

import argparse
import os

import slit_scanner


# **********************************************************************************************************************
#       Argument parsing
# **********************************************************************************************************************
parser = argparse.ArgumentParser()
parser._optionals.title = 'arguments'

parser.add_argument("-i", "--input_dir",
                    help="Input directory. Set of frames or a single video. Tests for frames first.", required=True)
parser.add_argument("-o", "--output_dir", default="None",
                    help="Path for output frames (optional) Default: Subdir of input)")
parser.add_argument("-slit", "--slit_size", default=5, type=int, help="Slit Size (optional)")
parser.add_argument("-l", "--frame_limit", default=-1, type=int,
                    help="Limit number of frames to specified int (optional)")
parser.add_argument("-format", "--output_format", default="JPEG", help="Output image format. (optional)")
parser.add_argument("-t", "--type", default="0",
                    help="Type of slitscan to be performed. [0]=single-vertical, [1]=single-horizontal "
                         "[2]=Moving-Horizontal, [3]=Moving-Vertical, [4]=Moving-Both (Vertical AND Horizontal), "
                         "[5]=Low-Memory"
                    )
parser.add_argument("-v", "--video", default=0,
                    help="Optional: Encode h.264 video of resulting frames (0 or 1. Default is 0)")

args = parser.parse_args()


# **********************************************************************************************************************
#       Validation
# **********************************************************************************************************************

if args.output_dir == "None":
    args.output_dir = args.input_dir

if not os.path.exists(args.input_dir):
    raise IOError("No such path: ", args.input_dir)

if not os.path.exists(args.output_dir):
    raise IOError("No such path: ", args.output_dir)

acceptable_formats = ["jpeg", "png", "tiff"]
if args.output_format.lower() not in acceptable_formats:
    print("Unknown output format requested. Acceptable options are: JPEG, PNG, or TIFF. Defaulting to JPEG.")
    args.output_format = "JPEG"

args.type = args.type.lower()
test_dir = slit_scanner.make_a_glob(args.input_dir)
out_path = None


# **********************************************************************************************************************
#       Slitscan time!
# **********************************************************************************************************************

if args.type == "single-vertical" or args.type == "0":
    print("\nPerforming single slitscan (vertical)")
    slit_scanner.slitscan(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format, True, False)

if args.type == "single-horizontal" or args.type == "1":
    print("\nPerforming single slitscan (horizontal)")
    slit_scanner.slitscan(test_dir, args.output_dir, args.slit_size, args.frame_limit, args.output_format, False, True)

elif args.type in ["moving-horizontal", "2", "moving-vertical", "3"]:
    moving_horizontal = args.type in ["moving-horizontal", "2"]
    print("\nPerforming moving-horizontal slitscan. HORIZONTAL slices."
          if moving_horizontal else "\nPerforming moving-vertical slitscan. VERTICAL slices.")

    out_path = slit_scanner.moving_slitscan_both(
        test_dir,
        args.output_dir,
        args.slit_size,
        args.frame_limit,
        args.output_format,
        do_height=moving_horizontal,
        do_width=not moving_horizontal
    )

elif args.type == "moving-both" or args.type == "4":
    print("\nPerforming both moving-vertical and moving-horizontal slitscans, without having to reload everything.")
    out_path = slit_scanner.moving_slitscan_both(test_dir, args.output_dir, args.slit_size, args.frame_limit,
                                                 args.output_format, do_height=True, do_width=True)

elif args.type == "low-mem" or args.type == "5":
    print("\nLow-memory version. Very very very very slow, but RAM-efficient.")
    out_path = slit_scanner.lowmem_moving_slitscan(test_dir, args.output_dir, args.slit_size, args.frame_limit,
                                                   args.output_format)

# **********************************************************************************************************************
#       Video Processing
# **********************************************************************************************************************
if args.video and out_path is not None:
    print(out_path)
    if args.type == "2":
        out_path += "height/"
        slit_scanner.make_a_video(out_path, args.output_format, "height.mp4")
    elif args.type == "3":
        out_path += "width/"
        slit_scanner.make_a_video(out_path, args.output_format, "width.mp4")
    elif args.type == "4":
        out_path_width = out_path + "width/"
        slit_scanner.make_a_video(out_path_width, args.output_format, "width.mp4")
        out_path_height = out_path + "height/"
        slit_scanner.make_a_video(out_path_height, args.output_format, "height.mp4")
    elif args.type == "5":
        slit_scanner.make_a_video(out_path, args.output_format, "slitscan.mp4")
