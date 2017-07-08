#!/usr/bin/python
#-*- coding=utf-8 -*-

import sys, time
import ConfigParser

import Backup

argument = sys.argv[:]

if len(argument) <= 1:
    print "Missing necessary parameters named --db-type, Please use ex, `python run.py db`"
    exit(1)

useDb = argument[1]

cp = ConfigParser.ConfigParser()
cp.read('./config.conf')

dbList = cp.sections()

if useDb not in dbList:
    print "Please use correct db item in %s" %dbList
    exit(1)


options = {
    'db': {
        'host': cp.get(useDb, 'host'),
        'user': cp.get(useDb, 'user'),
        'password': cp.get(useDb, 'password')
    },
    'baseDirectory':'/home/aaaa/test/backup/'
}
startTime = time.time()

backup = Backup.Backup(options)
backup.log("INFO", "========================== START ========================================")

backup.run()

endTime = time.time()

backup.log("INFO", "========================== END ========================================")

runningTime = endTime - startTime


backup.log("INFO", "running time: %.2f" %runningTime)

mailContent = backup.mail_contents + "<br><br>数据库Host: %s 备份成功, 本次备份耗时: %.2f秒" %(options['db']['host'], runningTime)

backup.sendMail('a@example.com', 'MySQL 数据库备份', mailContent)




