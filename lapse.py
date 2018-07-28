# Build a composite image of every image in a particular directory

import cv2
import json
import glob
import logging
import numpy as np
import argparse
import os

class VideoBuilder:
    img_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']

    def __init__(self, args):
        self.fps = args.fps[0]
        self.out_file = args.output[0]
        self.image_path = args.path[0]
        self.fourcc = cv2.VideoWriter_fourcc(*args.codec[0]) # See OpenCV video docs for more
        self.imgs = []

        for extension in self.img_extensions:
            self.imgs.extend(glob.glob(self.image_path + "/*." + extension))

        # Use first image file in path as template for image output
        try:
            sample = cv2.imread(self.imgs[0], cv2.IMREAD_COLOR)
        except IndexError:
            logging.error("No images found in path {}".format(self.image_path))
            return

        self.out_height, self.out_width = sample.shape[:2]

        logging.info(
            'Auto-detected image dimensions as {}x{}...'.format(self.out_width, self.out_height))

        logging.info('Input settings: {}x{} @ {} FPS'.format(
            self.out_width, self.out_height, self.fps))

    """
    Generate blend video
    """
    def make_blend_video(self):
        video = cv2.VideoWriter(self.out_file, self.fourcc, self.fps, (self.out_width, self.out_height))

        # Array that holds current blended image data
        master = np.zeros((self.out_height, self.out_width, 3), np.float32)
        #master = np.zeros((self.out_height, self.out_width, 3), np.uint8)
        count = 1

        logging.info('Building fading timelapse of {} images in {}...'.format(
            len(self.imgs), self.image_path))

        for filename in self.imgs:
            image = cv2.imread(filename, cv2.IMREAD_COLOR)
            width, height = image.shape[:2]

            if width != self.out_width or height != self.out_height:
                logging.debug(
                    "Skipping invalid shaped image found in path: {}".format(filename))
                continue

            # Use float to allow greater blend precision
            fl_image = np.float32(image)
            master = cv2.addWeighted(master, float(
                (count-1)/count), fl_image, float(1.0/count), 0)
            video.write(np.uint8(master))

            count += 1

        logging.info('Successfully wrote {}'.format(self.out_file))

        video.release()

    """
    Generate flipbook style video
    """
    def make_flipbook(self):
        video = cv2.VideoWriter(self.out_file, self.fourcc, self.fps, (self.out_width, self.out_height))

        logging.info('Building flipbook of {} images in {}...'.format(
            len(self.imgs), self.image_path))

        for filename in self.imgs:
            image = cv2.imread(filename, cv2.IMREAD_COLOR)
            width, height = image.shape[:2]

            if width != self.out_width or height != self.out_height:
                logging.debug(
                    "Skipping invalid shaped image found in path: {}".format(filename))
                continue

            video.write(image)

        logging.info('Successfully wrote {}'.format(self.out_file))

        video.release()

    """
    Generate split style video
    """
    def make_split_video(self):
        video = cv2.VideoWriter(self.out_file, self.fourcc, self.fps, (self.out_width * 2, self.out_height))

        # Array that holds current blended image data
        master = np.zeros((self.out_height, self.out_width, 3), np.float32)
        count = 1

        logging.info('Building split blend/flipbook of {} images in {}...'.format(
            len(self.imgs), self.image_path))

        for filename in self.imgs:
            image = cv2.imread(filename, cv2.IMREAD_COLOR)
            width, height = image.shape[:2]

            if width != self.out_width or height != self.out_height:
                logging.debug(
                    "Skipping invalid shaped image found in path: {}".format(filename))
                continue

            # Use float to allow greater blend precision
            fl_image = np.float32(image)
            master = cv2.addWeighted(master, float(
                (count-1)/count), fl_image, float(1.0/count), 0)
            combo = np.concatenate((image, np.uint8(master)), axis=1)

            video.write(combo)

            count += 1

        logging.info('Successfully wrote {}'.format(self.out_file))

        video.release()


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
    parser.add_argument('-c', '--codec', nargs=1,
                        help='fourcc codec (DIVX, XVID, MJPG, X264, WMV1, WMV2)', type=str, default=['DIVX'])
    parser.add_argument('-t', '--type', nargs=1,
                        help='type of video (blend, flipbook, split)', type=str, default=['blend'])
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    return args

if __name__ == "__main__":
    args = read_args()
    builder = VideoBuilder(args)

    if args.type[0] == 'blend':
        builder.make_blend_video()
    elif args.type[0] == 'flipbook':
        builder.make_flipbook()
    elif args.type[0] == 'split':
        builder.make_split_video()
    else:
        logging.error("Invalid video type, try 'blend' or 'flipbook'")

