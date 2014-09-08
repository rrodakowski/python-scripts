#! /usr/bin/env python
import csv

def get_first_and_last_column(filename, separator):
    with file(filename, 'rb') as file_obj:
        for line in csv.reader(file_obj, 
              delimiter=separator,    # Your custom delimiter.
              skipinitialspace=True): # Strips whitespace after delimiter.
            if line: # Make sure there's at least one entry.
                yield line[0], line[-1]

if __name__ == '__main__':
    for pair in get_first_and_last_column(r'test.txt', '|'):
        print pair
