#! /usr/bin/env python
__author__ = 'Randall'
import os
import time
import logging
from subprocess import call
from subprocess import check_output

logger = logging.getLogger(__name__)


class ImageService(object):

    def __init__(self):
        logger.debug("Creating the ImageService")

    def get_file_stats(self, filename):
        value = check_output('convert {} -ping -format "%w x %h" info:'.format(filename), shell=True)
        logger.info('Image size is: {}'.format(value))

    def resize_file(self, filename, dirname, width, height):
        fullpath = os.path.join(dirname, filename)
        base = os.path.splitext(fullpath)[0]
        extension = os.path.splitext(fullpath)[1]
        outputfile = base + '-out' +extension
        call('convert {} -resize {}x{}\> -quality 80 {}'.format(fullpath, width, height, outputfile), shell=True)

    def make_thumbnails(self, dirname):
        width = 100
        height = 67
        for filename in os.listdir(dirname):
            if filename.endswith(".jpg") or filename.endswith(".JPG"):
                logger.info("Resizing file: " + filename)
                self.resize_file(filename, dirname, width, height)

    def make_animated_gif(self, input_dir, outputfilename):
        logger.info("Creating animated gif. ")

        # resize the images so that they are small enough to meet tumblr's size requirements
        # the width should be at least 500 though so that they take up the full display width
        # on the online blog was 350 x233 now 500 x 375
        for f in os.listdir(input_dir):
            logger.info("Going through " +input_dir)
            if f.endswith("jpg"):
                filename = os.path.basename(f)
                logger.info('convert {} -resize 500x375 {}.gif'.format(input_dir+os.sep+f, input_dir+os.sep+filename))
                call('convert {} -resize 500x375 {}.gif'.format(input_dir+os.sep+f, os.path.join(input_dir, filename)), shell=True)

        inputfiles=input_dir+os.sep+'*.gif'
        # convert -delay 20 -loop 0 sphere*.gif animatespheres.gif
        call('convert -delay 20 -loop 0 {} {}'.format(inputfiles, outputfilename), shell=True)
        logger.info("Finished creating animated gif. ")
