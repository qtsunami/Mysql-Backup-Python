#!/usr/bin/python
#-*- coding=utf-8 -*-

import logging


class Log:

    logger = None
    logPath = 'log/mysql-full-volume-backup.log'

    def __init__(self, options=None):
        """
        设置Logger 写入路径及日志级别
        :return:
        """
        if options is not None:
            self.logPath = options['logPath']

        FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.logger = logging.basicConfig(filename=self.logPath, format=FORMAT)

        self.logger = logging.getLogger('mysql-full-volume-backup')
        self.logger.setLevel(logging.INFO)

        """
        打印到终端
        """
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.INFO)
        #
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # ch.setFormatter(formatter)

        # self.logger.addHandler(ch)

    def debug(self, message=None):
        self.logger.debug(message)

    def warning(self, message=None):
        self.logger.error(message)

    def info(self, message=None):
        self.logger.info(message)

    def error(self, message=None):
        self.logger.error(message)
