# slit_scanner_darkly
Slit scanning. From frames to weird final product.

This is a repository that allows for creating several types of slitscans.

Dependencies:
PIL http://www.pythonware.com/products/pil/
Hickle https://github.com/telegraphic/hickle
Numpy http://www.numpy.org/


Single Slitscans:
Single slitscans come in two flavors: horizontal and vertical. This style of slitscan is inspired by Adam Magyar's (http://www.magyaradam.com/) Urban Flow project.

Moving Slitscans:
Like the single slitscans (horizontal and vertical), but compiled over ~all~ the images in a sequence. Each new frame
is a single slitscan from a different x or y coordinate. 


# Examples:
Github doesn't let me embed YouTube vids... lame.
### Original Footage:
[![Chicago Train Footage](https://img.youtube.com/vi/t-guLsCS_pg/0.jpg)](https://www.youtube.com/watch?v=t-guLsCS_pg)

https://www.youtube.com/watch?v=t-guLsCS_pg
### Single Slitscan (height)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 0`

### Single Slitscan (width)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 1`

### Moving Slitscan (height)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 2`

[![Chicago Train Footage - Slitscan Width](https://img.youtube.com/vi/Mm9q6qhgt7Y/0.jpg)](https://www.youtube.com/watch?v=Mm9q6qhgt7Y)

https://www.youtube.com/watch?v=Mm9q6qhgt7Y
### Moving Slitscan (width)
`cli.py -i <input_dir - set of video frames> -o <output_dir> -slit 5 -t 3`

[![Chicago Train Footage - Slitscan Width](https://img.youtube.com/vi/UCeJmNJHFNI/0.jpg)](https://www.youtube.com/watch?v=UCeJmNJHFNI)

https://www.youtube.com/watch?v=UCeJmNJHFNI
