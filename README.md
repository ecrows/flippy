# flippy
Python script for generating videos by rapidly flipping through or overlaying images.

![Preview Example](https://i.imgur.com/LLKZpr5.gif)

## Installation
`pip install flippy`

This will automatically download and install `flippy`, `opencv-python`, and `numpy`.


## Usage

```
flippy /some/image/path
```

This will build a video out of the images in the directory `/some/image/path`, using the auto-detected resolution at the default 20 FPS.

Flippy is heavily configurable, and accepts a number of command line arguments.

```
flippy /some/image/path -o ~/output.avi -f 60.0 -c XVID -t blend

INFO:root:Auto-detected image dimensions as 64x64...
INFO:root:Building fading timelapse of 24247 images in /some/path/faces...
INFO:root:Output settings: 64x64 @ 60.0 FPS
INFO:root:Successfully wrote /home/user/output.avi
```

For the full list of availble arguments, type `flippy --help`.
```
usage: flippy [-h] [-v] [-f FPS] [-o OUTPUT] [-c CODEC] [-t TYPE] [-r REGEX]
                path [path ...]

Build a fading timelapse of overlayed images.

positional arguments:
  path                  path to read image files from

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose logging
  -f FPS, --fps FPS     frames per second
  -o OUTPUT, --output OUTPUT
                        output file
  -c CODEC, --codec CODEC
                        fourcc codec (DIVX, XVID, MJPG, X264, WMV1, WMV2)
  -t TYPE, --type TYPE  type of video (blend, flipbook, split)
  -r REGEX, --regex REGEX
                        file regex for images in path, default matches common
                        lowercase image extensions
```

## Requirements
* [OpenCV](https://opencv.org/)
* [numpy](http://www.numpy.org/)
