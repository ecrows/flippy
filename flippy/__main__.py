import argparse
import re
import logging
import os
from .lapse import VideoBuilder

def read_args():
    parser = argparse.ArgumentParser(
        description='Build a fading timelapse of overlayed images.')

    parser.add_argument('path', nargs='+',
                        help='path to read image files from', type=str)
    parser.add_argument('-v', '--verbose',
                        help='verbose logging', action='store_true')
    parser.add_argument('-f', '--fps', nargs=1,
                        help='frames per second', type=float, default=[20.0])
    parser.add_argument('-o', '--output', nargs=1,
                        help='output file', type=str, default=['video.avi'])
    parser.add_argument(
        '-c',
        '--codec',
        nargs=1,
        help='fourcc codec (DIVX, XVID, MJPG, X264, WMV1, WMV2)',
        type=str,
        default=['DIVX'])
    parser.add_argument(
        '-t',
        '--type',
        nargs=1,
        help='type of video (blend, flipbook, split)',
        type=str,
        default=['blend'])
    parser.add_argument(
        '-r',
        '--regex',
        nargs=1,
        help='file match regex, default matches files with common lowercase image extensions',
        type=str,
        default=['.*\.jpg|.*\.jpeg|.*\.png|.*\.bmp|.*\.gif'])
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    return args

def main():
    args = read_args()

    images = []
    for image in os.listdir(args.path[0]):
        if re.match(args.regex[0], image):
            images.append(os.path.abspath(args.path[0] + "/" + image))

    builder = VideoBuilder(images, args.fps[0], args.output[0], args.codec[0])

    if args.type[0] == 'blend':
        builder.make_blend_video()
    elif args.type[0] == 'flipbook':
        builder.make_flipbook()
    elif args.type[0] == 'split':
        builder.make_split_video()
    else:
        logging.error(
            "Invalid video type, try 'blend', 'flipbook', or 'split'")
        
if __name__ == "__main__":
    main()
