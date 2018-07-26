# Build a composite image of every image in a particular directory

import cv2
import json
import glob
import numpy as np
import argparse

IMG_SIZE = 240

parser = argparse.ArgumentParser(description='Build a fading timelapse of overlayed images.')

parser.add_argument('-p', metavar='p', nargs=1, help='path to read image files from')

args = parser.parse_args()

imagepath=args.p[0]

master = np.zeros((IMG_SIZE, IMG_SIZE, 3), np.uint8)

allfiles = glob.glob('{}/*.jpg'.format(imagepath)) # TODO: Other image formats
count = 1

# TODO: Input/output dimensions and formats, auto detect size from first image
width = 240
height = 240
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter('video.avi', fourcc, 20.0, (width,height))

print('Building fading timelapse of all {} images in {}...'.format(len(allfiles), imagepath))

for filename in allfiles:
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    
    # TODO: Preview mode
    # cv2.imshow('Combined', master)
    # cv2.waitKey()
    
    # TODO: Confirm that with very large numbers of images the precision on this is sufficient
    master = cv2.addWeighted(master, float((count-1)/count), image, float(1.0/count), 0)
    video.write(master)
    
    count += 1
    
video.release()