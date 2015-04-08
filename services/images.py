#! /usr/bin/env python
__author__ = 'Randall'

import argparse
import os
import time
import logging
from subprocess import call
import glob

#import pytumblr
from PIL import Image
from services import FileService

logger = logging.getLogger(__name__)

class ImageService(object):

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s %(message)s')

    def get_file_stats(self, filename):
        im = Image.open(filename)
        width, height = im.size
        logger.info('Image size is: {}x{}'.format(width, height))

    def show_image(self, filename):
        im = Image.open(filename)
        im.show()

    def resize_file(self, filename, size):
        file, ext = os.path.splitext(filename)
        im = Image.open(filename)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(file + "-thumbnail.jpg", "JPEG")

    def make_thumbnails(self, dirname):
        size = 128, 128
        for infile in glob.glob(dirname+os.sep+"*.jpg"):
            logger.info("Resizing file " + infile)
            self.resize_file(infile, size)


class AnimatedGifMaker(object):
    'This class creates an animated gif from files in a directory.'

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s %(message)s')
          # Authenticate via OAuth
        self.client = pytumblr.TumblrRestClient(
            '9ZpAAcfZ8YDzc0Evqcvhc4LldUPOl305X3v3A8U61GVFrf6V1q',
            'tcKzpTWCnnmMHM5AbY82nSHCR2Yl8qGEGtwVdXk3rovREhHJMS',
            'KGgoUQ0GCo3VDHPr0UK1SozTMm3aVo8OnGQy182iEFWOopmkx4',
            '6meK6IeQ0PZ7aL5dBd9Pgt1MuckWDWzBglmHSlkyzQh8CuiCBi'
        )
        self.fs = FileService()
        self.timestamp = None

    def post_picture(self, filename):
        logger.info("Posting picture: " +filename)

        # Make an info request
        #response = self.client.info()

        #Posts an image to your tumblr.
        #Make sure you point an image in your hard drive. Here, 'image.jpg' must be in the
        #same folder where your script is saved.
        #From yourBlogName.tumblr.com should just use 'yourBlogName'
        #The default state is set to "queue", to publish use "published"
        response = self.client.create_photo('snap-ya', state="published", tags=["testing", "ok"], data=filename)
        logger.info("Done Posting file.")

    def preprocess(self, input_dir, archive_dir):
        logger.info("Initializing...")
        self.timestamp=time.strftime("%Y-%m-%dT%H:%M:%S")
        self.fs.ensure_dir(input_dir)
        self.fs.ensure_dir(archive_dir)
        self.fs.ensure_dir(archive_dir+os.sep+self.timestamp)

        outputfilename=archive_dir+os.sep+self.timestamp+os.sep+'snapya_{}.gif'.format(self.timestamp)
        return outputfilename

    def processImage(self, input_dir, outputfilename):
        logger.info("Creating animated gif. ")

        # resize the images so that they are small enough to meet tumblr's size requirements
        # the width should be at least 500 though so that they take up the full display width
        # on the online blog was 350 x233 now 500 x 375
        for f in os.listdir(input_dir):
            logger.info("Going through " +input_dir)
            if f.endswith("jpg"):
                logger.info('convert {} -resize 500x375 {}.gif'.format(input_dir+os.sep+f, input_dir+os.sep+self.fs.get_basename(f)))
                call('convert {} -resize 500x375 {}.gif'.format(input_dir+os.sep+f, input_dir+os.sep+self.fs.get_basename(f)), shell=True)

        inputfiles=input_dir+os.sep+'*.gif'
        #convert -delay 20 -loop 0 sphere*.gif animatespheres.gif
        call('convert -delay 20 -loop 0 {} {}'.format(inputfiles, outputfilename), shell=True)
        logger.info("Finished creating animated gif. ")

    def cleanup(self, input_dir, archive_dir):
        logger.info("Cleaning up and moving files to the archive dir: "+archive_dir)
        final_dir=archive_dir+os.sep+self.timestamp
        for f in os.listdir(input_dir):
            #if f.endswith("gif"): can put this back in, if I want to only cleanup gif files
            os.rename(input_dir+os.sep+f, final_dir+os.sep+f)

    def main(self, input_dir, archive_dir, doUpload):
        outputfilename = self.preprocess(input_dir, archive_dir)

        self.processImage(input_dir, outputfilename)
        if(doUpload):
            self.post_picture(outputfilename)
        self.cleanup(input_dir, archive_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some files')
    parser.add_argument('-i', required=True, dest='inputdir', action='store', help='input dir')
    parser.add_argument('-a', required=True, dest='archivedir', action='store', help='archive dir')
    parser.add_argument('-u', dest='upload', action='store_true', help='should upload to tumblr?')
    args = parser.parse_args()

    input_dir=args.inputdir
    archive_dir=args.archivedir
    doUpload=args.upload
    AnimatedGifMaker().main(input_dir, archive_dir, doUpload )

    logger.info("Finished Processing File.")
