# overlay-lapse
Python script for generating videos by overlaying images.

![Preview Example](examples/anime_face.gif)

usage: lapse.py [-h] [-v] [-f FPS] [-o OUTPUT] [-c CODEC] path [path ...]

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
                        fourcc codec

Example:

python3 lapse.py /some/path/faces\_64px -o ~/output.avi -f 60.0 -c XVID

INFO:root:Auto-detected image dimensions as 64x64...
INFO:root:Building fading timelapse of 24247 images in /some/path/faces\_64px...
INFO:root:Output settings: 64x64 @ 60.0 FPS

