#! /usr/bin/env python

import cx_Oracle

def oracle_connect():
    con = cx_Oracle.connect('pythonhol/welcome@127.0.0.1/orcl')

    cur = con.cursor()
    cur.execute('select * from departments order by department_id')
    res = cur.fetchall()
    for r in res:
        print r

    cur.close()
    con.close()

if __name__ == '__main__':
    oracle_connect()
