#! /usr/bin/env python
import argparse
import glob, os
from PIL import Image

def get_file_stats(filename):
    print "Starting to output stats"
    print "Done with stats"

def show_image(filename):
    im = Image.open(filename)
    im.show()

def resize_file(filename, size):
    file, ext = os.path.splitext(filename)
    im = Image.open(filename)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(file + ".thumbnail", "JPEG")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('strings', metavar='N', type=string, nargs='+',
                   help='a filename')
    args = parser.parse_args()
    print args
    size = 128, 128
    filename='/home/randall/Pictures/profile.jpg'

    #for infile in glob.glob("*.jpg"):
    #get_file_stats(filename)
    #resize_file(filename, size)
