#-*- coding:utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import config

# 数据库工具类
# 获取连接和游标
class myConnection(object):
    def __init__(self):
        self.__connection = None

    # 初始化连接
    def __init_connect(self):
        if self.__connection == None:
            self.__connection = MySQLdb.Connect(host=config.HOST,port=config.PORT,user=config.USER,
                                                passwd=config.PASSWD,db=config.DB,charset=config.CHARSET,
                                                cursorclass=MySQLdb.cursors.DictCursor) # 得到连接

    # 获取连接
    def getconn(self):
        if self.__connection == None:
            self.__init_connect()
        return self.__connection

    # 关闭连接
    def close(self):
        if self.__connection != None:
            self.cursor.close()
            self.__connection.close()

    # 对象信息
    def __str__(self):
        return myConnection.__name__ + str(self.__params)