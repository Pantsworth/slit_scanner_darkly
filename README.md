# slit_scanner_darkly
Slit scanning. From frames to weird final product.

[![Chicago Train Footage - Slitscan Width](img/train_width_720.gif)](https://www.youtube.com/watch?v=UCeJmNJHFNI)


This is a repository that allows for creating several types of slitscans (examples available further down the page).

**Setup:**

0. Install [ffmpeg](https://ffmpeg.org/) and [Python 3](https://realpython.com/installing-python/)
1. clone this repo
2. `cd slit_scanner_darkly`
3. `mkdir venv`
4. `python3 -m venv venv/`
5. `source venv/bin/activate`
6. `pip install -r requirements.txt`


**Single Slitscans:**
Single slitscans come in two flavors: horizontal and vertical. This style of slitscan is inspired by [Adam Magyar's Urban Flow project](http://www.magyaradam.com/).

**Moving Slitscans:**
Like the single slitscans (horizontal and vertical), but compiled over ~all~ the images in a sequence. Each new frame
is a single slitscan from a different x or y coordinate. 

# Usage:
**Required Args:**

Flags | Help
------------ | -------------
-i, --input_dir | input directory (set of video frames)
-o, --output_dir | output directory (script will create subfolder)

**Optional:**

Flags | Help
------------ | -------------
-t, --slitscan_type | Type of slitscan to be performed. [0]=single-vertical, [1]=single-horizontal [2]=Moving-Horizontal, [3]=Moving-Vertical, [4]=Moving-Both (Vertical AND Horizontal)
-slit, --slit_size | Slit Size (default=5)
-l, --frame_limit | Limit number of frames to specified int (default = -1)
-format, --output_format | Output image format (default="JPEG")


# Examples:
Github doesn't let me embed YouTube vids... lame. I put a few gifs in, but for full examples see the videos.
### Original Footage:
Train Station:

[![Chicago Train Footage](img/train_720.gif)](https://www.youtube.com/watch?v=t-guLsCS_pg)

https://www.youtube.com/watch?v=t-guLsCS_pg

Bridge:

[![Chicago Bridge Footage](https://img.youtube.com/vi/-JRnao5nn_U/0.jpg)](https://www.youtube.com/watch?v=-JRnao5nn_U)


https://www.youtube.com/watch?v=-JRnao5nn_U

### Single Slitscan (height)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 0`

Train Station:

<img src="img/single_slitscan-height.JPEG" width="500px"/>

Bridge:

<img src="img/single_slitscan-height-bridge.JPEG" width="500"/>


### Single Slitscan (width)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 1`

Train Station:

<img src="img/single_slitscan-width.JPEG" width="500"/>

Bridge:

<img src="img/single_slitscan-width-bridge.JPEG" width="500"/>


### Moving Slitscan (height)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 2`
Train Station:

[![Chicago Train Footage - Slitscan Width](img/train_height_720.gif)](https://www.youtube.com/watch?v=Mm9q6qhgt7Y)

https://www.youtube.com/watch?v=Mm9q6qhgt7Y

Bridge:

[![Chicago Train Footage - Slitscan Width](https://img.youtube.com/vi/e5PUNPEcwTI/0.jpg)](https://www.youtube.com/watch?v=e5PUNPEcwTI)

https://www.youtube.com/watch?v=e5PUNPEcwTI

### Moving Slitscan (width)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 3`

[![Chicago Train Footage - Slitscan Width](img/train_width_720.gif)](https://www.youtube.com/watch?v=UCeJmNJHFNI)

https://www.youtube.com/watch?v=UCeJmNJHFNI

[![Chicago Bridge Footage - Slitscan Width](https://img.youtube.com/vi/3k-TRcbbit8/0.jpg)](https://www.youtube.com/watch?v=3k-TRcbbit8)

https://www.youtube.com/watch?v=3k-TRcbbit8
