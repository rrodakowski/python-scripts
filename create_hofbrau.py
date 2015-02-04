#! /usr/bin/env python
import csv
import argparse
import os
from services import FileService
import xml.etree.cElementTree as ET
from xml.dom import minidom 
from xml.etree import ElementTree

def get_first_and_last_column(filename, separator):
    with file(filename, 'rU') as file_obj:
        for line in csv.reader(file_obj, 
              delimiter=separator):
              
            if line: # Make sure there's at least one entry.
                yield line[0], line[-1]

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search some files')
    parser.add_argument('-i', dest='input', action='store', help='infput file')
    parser.add_argument('-o', dest='outdir', action='store', help='output dir')
    args = parser.parse_args()

    input_file=args.input
    output_dir=args.outdir

    dbset = set()
    root = ET.Element("root")
    fs = FileService()

    for pair in get_first_and_last_column(input_file, ','):
	(key, value) = pair
        product = ET.SubElement(root, "product", name=key)
        databases = value.split(';')
	for database in databases:
            dbset.add(database.strip())
            ET.SubElement(product, "database").text = database.strip() 

    fs.write_raw_text_to_file(output_dir+os.sep+"product_dataset_map.xml", prettify(root))
#    tree = ET.ElementTree(pretty_root)
#    tree.write(output_dir+os.sep+"product_dataset_map.xml")

    output_file=output_dir+os.sep+'hofbrau.list'
    fs.write_to_file(output_file, dbset)
