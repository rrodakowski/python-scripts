#!/usr/bin/python
import time
import datetime
import sys 
import os
from subprocess import call
import fnmatch
import argparse

parser = argparse.ArgumentParser(description='Search some files')
parser.add_argument('-a', dest='archive', action='store',
 help='archive dir')
parser.add_argument('-o', dest='outdir', action='store',
 help='output dir')
args = parser.parse_args()

file_dir=args.archive
output_dir=args.outdir
broadside_bin='/checkpoint/cm/bin/broadside/scripts'
databases = set()

#Build documents
with open(output_dir+os.sep+'Document.tbl', 'w') as outfile:
    for f in os.listdir(file_dir):
        if f.endswith("_document_guid"):
	    databases.add(re.split(r'_', line)[0])
            with open(file_dir+os.sep+f) as infile:
                for line in infile:
                    outfile.write(line)

call('{}/sql_unldr.ksh RIA_WEB/RIA_WEB top_line_link > {}/final_top_line_link.tbl'.format(broadside_bin, output_dir), shell=True)

