#!/usr/bin/python
# -*- coding=utf-8 -*-


import MySQLdb, os, time
import Log

import smtplib
from email.mime.text import MIMEText
# from email.header import Header

# import db_config
class Backup:

    """
        Custom Class Attribute
    """

    # DB connect object
    dbConnect = None

    # DB config object
    dbConfig = None

    # List , out of backup database
    dbSystem = ['mysql', 'information_schema', 'performance_schema']

    # Base Directory
    baseDirectory = None

    # stroagePath
    stroagePath = None

    logger = None

    mail_contents = ''



    def __init__(self, options = None):
        """
        获取初始化信息,配置文件
        :return:
        """
        if options == None:
            print "Exception AttributeError: Missing necessary config, Please try again ..."
            exit(1)

        self.dbConfig = options['db']

        self.logger = Log.Log()
        self.baseDirectory = options['baseDirectory']

    def getDatabase(self):
        """
        get all databases and return database list
        :return:
        """
        databases_list = []

        if self.dbConfig == None:
            self.log('ERROR', 'DbConfnig is empty')
            return False

        conn = MySQLdb.connect(self.dbConfig['host'], self.dbConfig['user'], self.dbConfig['password'])
        cursor = conn.cursor()

        try:
            cursor.execute("show databases")
            result = cursor.fetchall()

            for dbname in result:
                if dbname[0] in self.dbSystem:
                    continue
                databases_list.append(dbname[0])

        except MySQLdb.Error, e:
            error_msg = "MySQLdb Error %d: %s" %(e.args[0], e.args[1])
            self.log('ERROR', error_msg)
            return False
        finally:
            conn.close()
            cursor.close()

        self.log('INFO', 'Successfully Get Databases List')
        return databases_list

    def generateStorageDir(self):
        """
        generate sql file store absolutely directory in order to current date
        :return:
        """
        relative_dir = time.strftime("%Y%m%d")
        storage_path = self.baseDirectory + relative_dir

        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
            self.log('INFO', "Wow~ Successfully created directory %s" %storage_path)

        self.stroagePath = storage_path
        return storage_path


    def executeCommand (self, dbname):
        """
        exec mysqldump command
        :return:
        """
        file_name = self.stroagePath + '/' + dbname + '.sql'
        if os.path.exists(file_name):
            return True

        execute_command = "mysqldump --quick -h%s -u%s -p%s %s > %s" %(self.dbConfig['host'], self.dbConfig['user'], self.dbConfig['password'], dbname, file_name)
        if os.system(execute_command) == 0:
            return True
        else:
            return False


    def log(self, flag='INFO', message = None):
        if flag == 'INFO':
            self.logger.info(message)
        elif flag == 'ERROR':
            self.logger.error(message)
        elif flag == 'WARNING':
            self.logger.warning(message)
        elif flag == 'DEBUG':
            self.logger.debug(message)
        else:
            self.logger.info(message)

    def run(self):
        # 获取所有库信息
        databases = self.getDatabase()
        if databases == False:
            return False

        self.stroagePath = self.generateStorageDir()



        for dbname in databases:
            ts = time.time()
            res = self.executeCommand(dbname)
            if res:
                msg = '%s 备份成功! 耗时: %.2f秒' %(dbname, time.time() - ts)
            else:
                msg = "%s 备份失败! 耗时: %.2f秒" %(dbname, time.time() - ts)

            self.log("INFO", msg)
            self.mail_contents = self.mail_contents + '<br>' + msg
        return True

    def sendMail(self, receiver, title, body):

        host = 'mail.xxxx.cn'
        port = 25
        sender = 'a@xxxx.cn'
        pwd = '1233333'

        self.log("INFO", "%s - %s - %s" %(receiver, title, body))

        msg = MIMEText(body, 'html')
        msg['subject'] = title
        msg['from'] = sender
        msg['to'] = receiver

        s = smtplib.SMTP(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
