# Build a composite image of every image in a particular directory

import cv2
import json
import logging
import numpy as np

class VideoBuilder:

    def __init__(self, input_files, fps, out_file, codec):
        self.fps = fps
        self.out_file = out_file
        self.imgs = input_files

        # See OpenCV video docs for more codecs
        self.fourcc = cv2.VideoWriter_fourcc(*codec)

        # Use first image file in path as template for image output
        try:
            sample = cv2.imread(self.imgs[0], cv2.IMREAD_COLOR)
        except IndexError:
            logging.error("No input images provided")
            exit()

        self.out_height, self.out_width = sample.shape[:2]

        logging.info(
            'Auto-detected image dimensions as {}x{}...'.format(self.out_width, self.out_height))

        logging.info('Input settings: {}x{} @ {} FPS'.format(
            self.out_width, self.out_height, self.fps))

    """
    Generate blend video
    """

    def make_blend_video(self):
        video = cv2.VideoWriter(
            self.out_file,
            self.fourcc,
            self.fps,
            (self.out_width,
             self.out_height))

        # Array that holds current blended image data
        master = np.zeros((self.out_height, self.out_width, 3), np.float32)
        count = 1

        logging.info('Building fading timelapse of {} images...'.format(
            len(self.imgs)))

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
                (count - 1) / count), fl_image, float(1.0 / count), 0)
            video.write(np.uint8(master))

            count += 1

        logging.info('Successfully wrote {}'.format(self.out_file))

        video.release()

    """
    Generate flipbook style video
    """

    def make_flipbook(self):
        video = cv2.VideoWriter(
            self.out_file,
            self.fourcc,
            self.fps,
            (self.out_width,
             self.out_height))

        logging.info('Building flipbook of {} images...'.format(
            len(self.imgs)))

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
        video = cv2.VideoWriter(
            self.out_file,
            self.fourcc,
            self.fps,
            (self.out_width * 2,
             self.out_height))

        # Array that holds current blended image data
        master = np.zeros((self.out_height, self.out_width, 3), np.float32)
        count = 1

        logging.info('Building split blend/flipbook of {} images...'.format(
            len(self.imgs)))

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
                (count - 1) / count), fl_image, float(1.0 / count), 0)
            combo = np.concatenate((image, np.uint8(master)), axis=1)

            video.write(combo)

            count += 1

        logging.info('Successfully wrote {}'.format(self.out_file))

        video.release()
