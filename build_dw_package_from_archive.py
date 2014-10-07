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

#take dbname out of _document_guid files and use that to build the snapshotInfo.xml file
with open(output_dir+os.sep+'snapshotInfo.xml', 'w') as outfile:
    outfile.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
    outfile.write('<snapshotInfo created="2014-09-12 20:22:36" cps_host="cps-prod-app.int.thomsonreuters.com">\n')
    outfile.write('<mode>FULL</mode>\n')
    outfile.write('<dbs>\n')
    for db in databases:
        outfile.write('<db>'+db.strip()+'</db>\n')
    outfile.write('</dbs>\n')
    outfile.write('</snapshotInfo>\n')

#build content type
with open(output_dir+os.sep+'Content_type.xml', 'w') as outfile:
    outfile.write('<wrapper>')
    for f in os.listdir(file_dir):
        if fnmatch.fnmatch(f, '*content*'):
            with open(file_dir+os.sep+f) as infile:
                for line in infile:
                    if "n-load" not in line:
                        outfile.write(line)
    outfile.write('</wrapper>')

# jurisdiction file
with open(output_dir+os.sep+'Jurisdiction.xml', 'w') as outfile:
    outfile.write('<wrapper>')
    for f in os.listdir(file_dir):
        if f.endswith("jurisdiction"):
            with open(file_dir+os.sep+f) as infile:
                for line in infile:
                    if "n-load" not in line:
                        outfile.write(line)
    outfile.write('</wrapper>')

# build index
with open(output_dir+os.sep+'Index.tbl', 'w') as outfile:
    outfile.write('<wrapper>')
    for f in os.listdir(file_dir):
        if f.endswith("document_index"):
            with open(file_dir+os.sep+f) as infile:
                for line in infile:
                    if "n-load" not in line:
                        outfile.write(line)
    outfile.write('</wrapper>')

# build taxtype file
with open(output_dir+os.sep+'Taxtype.tbl', 'w') as outfile:
    outfile.write('<wrapper>')
    for f in os.listdir(file_dir):
        if f.endswith("_taxtype"):
            with open(file_dir+os.sep+f) as infile:
                for line in infile:
                    if "n-load" not in line:
                        outfile.write(line)
    outfile.write('</wrapper>')

#build ancestry file
with open(output_dir+os.sep+'Ancestry.tbl', 'w') as outfile:
    for f in os.listdir(file_dir):
        if f.endswith("document_ancestry"):
            with open(file_dir+os.sep+f) as infile:
                for line in infile:
                    outfile.write(line)

call('{}/sql_unldr.ksh RIA_WEB/RIA_WEB top_line_link > {}/final_top_line_link.tbl'.format(broadside_bin, output_dir), shell=True)
call('{}/sql_unldr.ksh RIA_WEB/RIA_WEB link_tbl > {}/final_link_tbl.tbl'.format(broadside_bin, output_dir), shell=True)
call('{}/sql_unldr.ksh RIA_WEB/RIA_WEB link_pdr > {}/final_link_pdr.tbl'.format(broadside_bin, output_dir), shell=True)

