#!/usr/bin/python
#-*- coding=utf-8 -*-

import MySQLdb
import os
import time


# DB Config
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWD = '123456'


# Driectory Path
DIRECTORY_BASE = "/home/xxxx/test/backup/"
CURRENT_POSITION = time.strftime("%Y%m%d")

# Init Databases store list
databases_list = []
system_database = ['mysql', 'infomation_schema', 'performance_schema']


start_time = time.time()

"""
Connect Mysql DB & Get All Databases
"""


conn = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWD)
cursor = conn.cursor()

try:
    cursor.execute("show databases")
    result = cursor.fetchall()

    for dbname in result:
        if dbname[0] in system_database:
            continue;
        databases_list.append(dbname[0])

except MySQLdb.Error, e:
    print "MySQLdb Error %d: %s" %(e.args[0], e.args[1])
    print "Sorry, Error! Error! Please try again ..."
finally:
    conn.close()
    cursor.close()


# MAIN PROGRAM START

print len(databases_list)

if len(databases_list) == 0:
    print "No Databases Need Backup, bye ~ bye"
    exit(1)



storage_path = DIRECTORY_BASE + CURRENT_POSITION

if not os.path.exists(storage_path):
    os.mkdir(storage_path)
    print "Wow~ Successfully created directory", storage_path


for dbname in databases_list:
    print dbname
    file_name = dbname + ".sql"

    execute_command = "mysqldump -h%s -u%s -p%s %s > %s" %(DB_HOST, DB_USER, DB_PASSWD, dbname, storage_path + '/' + file_name)

    if os.system(execute_command) == 0:
        print "%s backup is complete!" %dbname
    else:
        print "Sorry! %s is Backup Failed" %dbname


end_time = time.time()

print "Yeah! Successfully Backup All Databases"
print "Backup time is %s" %(time.clock())

running_time = start_time - end_time

print "System use time is %s" %running_time



