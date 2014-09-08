#!/usr/bin/python
import MySQLdb
import time
import datetime
import sys
from services import FileService 

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="appadmin", # your username
                      passwd="nickPunto8", # your password
                      db="purgatory") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# find all the entries less than one day old, and add to the email message
# body 
now= time.strftime("%Y-%m-%d %H:%M:%S")
yesterday=datetime.date.fromordinal(datetime.date.today().toordinal()-1)
query='SELECT * FROM links_clicked WHERE time_clicked > "{}"'.format(yesterday)
cur.execute(query)

msg_body=[]
for row in cur.fetchall() :
    line="{} {} {} {} {} {} {}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]) 
    msg_body.append(line)

fs = FileService()
if len(msg_body) > 0:
    fs.send_message("Links Report", msg_body, "scallywag", "randall.rodakowski@gmail.com") 
