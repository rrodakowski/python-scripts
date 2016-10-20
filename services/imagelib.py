#! /usr/bin/env python
__author__ = 'Randall'
import os
import time
import logging
from subprocess import call
from subprocess import check_output

# For the S3File Manager
# pip install boto3
# pip install awscli
import boto3
from botocore.client import ClientError

logger = logging.getLogger(__name__)


class ImageService(object):
    """A wrapper for working with Imagemagick directly from python"""

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


class S3FileManager:
    """A wrapper for working with S3/AWS"""
    def __init__(self):
        # Let's use Amazon S3
        self.s3 = boto3.resource('s3')

    def print_bucket_names(self):
        # Print out bucket names
        for bucket in self.s3.buckets.all():
            print(bucket.name)

    def create_bucket(self, aws_bucketname):
        self.s3.create_bucket(Bucket=aws_bucketname)

    def delete_bucket(self, aws_bucketname):
        if self._bucket_exists(aws_bucketname):
            bucket = self.s3.Bucket(aws_bucketname)
            for key in bucket.objects.all():
                key.delete()
            bucket.delete()

    def upload_file(self, aws_bucketname, filepath):
        # Upload a new file
        if self._bucket_exists(aws_bucketname):
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as data:
                self.s3.Bucket(aws_bucketname).Object(filename).put(Body=data)

    def download_file(self, aws_bucketname, s3_file, local_download_directory):
        """
        Download a file from the S3 output bucket to your hard drive.
        """
        destination_path = os.path.join(
            local_download_directory,
            os.path.basename(s3_file)
        )
        body = self.s3.Bucket(aws_bucketname).Object(s3_file).get()['Body']
        with open(destination_path, 'wb') as dest:
            # Here we write the file in chunks to prevent
            # loading everything into memory at once.
            for chunk in iter(lambda: body.read(4096), b''):
                dest.write(chunk)

    def delete_files_from_bucket(self, aws_bucketname):
        if self._bucket_exists(aws_bucketname):
            # S3 delete everything in `my-bucket`
            self.s3.Bucket(aws_bucketname).objects.delete()

    def _bucket_exists(self, bucket_name):
        """
        Returns ``True`` if a bucket exists and you have access to
        call ``HeadBucket`` on it, otherwise ``False``.
        """
        try:
            self.s3.meta.client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            print ("error bucket does not exist")
            return False

    def _printBucketNotFoundMessage(self, bucket_name):
        print("Error: bucket '{}' not found".format(bucket_name))
