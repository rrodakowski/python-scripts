#!/usr/bin/python
import MySQLdb
import time
import datetime
import sys
import csv


db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="MYPASSWORD123", # your password
                      db="kls") # name of the data base
cur = db.cursor() 

def get_line(filename, separator):
    with file(filename, 'rb') as file_obj:
        for line in csv.reader(file_obj,
              delimiter=separator,    # Your custom delimiter.
              skipinitialspace=True): # Strips whitespace after delimiter.
            if line: # Make sure there's at least one entry.
                yield line

def load(table, line):
    # you must create a Cursor object. It will let
    #  you execute all the queries you need

    if table=='portfolio':
        query='INSERT INTO `kls`.`portfolio`(`idPortfolio`,`name`)VALUES({},"{}");'.format(line[0],line[1])
    if table=='securities':
        query='INSERT INTO `kls`.`security`(`idSecurity`,`security_name`,`current_price`,`multiplier`)VALUES({},"{}",{},{});'.format(line[0],line[1],line[2],line[3])

    if table=='trades':
        query='INSERT INTO `kls`.`trade`(`idTrades`,`idSecurity`,`idPortfolio`,`shares`)VALUES({},{},{},{});'.format(line[0],line[1],line[2],line[3])

    print query
    cur.execute(query)

if __name__ == '__main__':
    for line in get_line(r'portfolio.csv', ','):
        load("portfolio", line)
    for line in get_line(r'securities.csv', ','):
        load("securities", line)
    for line in get_line(r'trades.csv', ','):
        load("trades", line)

    cur.close()
    db.commit()
    db.close()
