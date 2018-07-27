# Build a composite image of every image in a particular directory

import cv2
import json
import glob
import logging
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='Build a fading timelapse of overlayed images.')

parser.add_argument('path', nargs='+', help='path to read image files from', type=str)
parser.add_argument('-v', '--verbose', help='verbose logging', action='store_true')
parser.add_argument('-f', '--fps', nargs=1, help='frames per second', type=float, default=[20.0])
# TODO: Outfile

args = parser.parse_args()

# Logging verbosity
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

fps = args.fps[0]

# Read image path (required)
image_path=args.path[0]

extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']
all_files = []

for extension in extensions:
    all_files.extend(glob.glob(image_path + "/*." + extension))

# Use first file as template for images
try:
    sample = cv2.imread(all_files[0], cv2.IMREAD_COLOR)
except IndexError:
    logging.error("No images found in path {}".format(image_path))
    exit()

out_height, out_width,  = sample.shape[:2]

logging.info('Auto-detected image dimensions as {}x{}...'.format(out_width, out_height))

# DIVX seems to work on Windows and Debian, TODO: add override for other codecs[0:1]
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

# TODO: Input/output dimensions and formats, auto detect size from first image
video = cv2.VideoWriter('video.avi', fourcc, fps, (out_width, out_height))

logging.info('Building fading timelapse of {} images in {}...'.format(len(all_files), image_path))
logging.info('Output settings: {}x{} @ {} FPS'.format(out_width, out_height, fps))

# Array that holds current blended image data
master = np.zeros((out_height, out_width, 3), np.uint8)
count = 1

for filename in all_files:
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    width, height = image.shape[:2]

    # TODO: Ask forgiveness?
    if width != out_width or height != out_height:
        logging.debug("Skipping invalid shaped image found in path: {}".format(filename))
        continue
    
    # TODO: Preview mode
    # cv2.imshow('Combined', master)
    # cv2.waitKey()
    
    # TODO: Confirm that with very large numbers of images the precision on this is sufficient
    master = cv2.addWeighted(master, float((count-1)/count), image, float(1.0/count), 0)
    video.write(master)
    
    count += 1
    
video.release()
