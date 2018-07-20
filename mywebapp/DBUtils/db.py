#-*- coding:utf-8 -*-
from myConnection import myConnection
# 数据库底层操作接口
# 连接数据库的
# 全局变量
# 创建引擎
# 执行语句修饰器
def execute_all(f):
    def fn(self, sql, *args):
        # 判断sql中有没有?
        if "?" in sql:
            sql = getRealSql(find("?",sql), args)
        return f(self, sql)
    return fn

# 根据指定字符拆分字符串并返回列表
def find(char, str):
    list = [] # 返回拆分后字符串列表
    str_temp = str
    if char in str_temp: # 判断在字符串里面是否存在。不存在就不用执行了
        list = str_temp.split("?")
    return list

# 将sql的?替换成对应的参数 list.insert(index,item)
def getRealSql(strs, args):
    print strs,args
    length = len(args)
    while length > 0:
        length -= 1
        item = args[length]
        if isinstance(item,str):
            item = "'" + item + "'"
        strs.insert(length + 1, str(item))
    return "".join(strs)

# db类
class DB:
    def __init__(self):
        self.conn = None
        self.__initProp()

    def __initProp(self):
        if self.conn == None:
            args = self.__readProp("db.properties")  # 读取配置文件信息
            myConn = myConnection(args) # 获取连接
            self.conn = myConn.getconn()
            self.cursor = self.conn.cursor()

    # 关闭
    def clearup(self):
        try:
            if self.conn != None:
                self.conn.close()
        except Exception as e:
            print "关闭失败"
            print e

    #select
    # 返回list list里面是字典
    @execute_all
    def select(self, sql, *args):
        # 这里执行查询语句
        # 判断 是否以select开头
        list = []
        if sql.strip()[0:6] == "select":
            try:
                self.cursor.execute(sql)
                rs = self.cursor.fetchall()# 得到结果集
                for t in rs:
                    dict = {"id":t[0],"username":t[1],"password":t[2]}
                    list.append(dict)
            except Exception as e:
                print e
        else:
            print "sql语句格式不正确......is not select Statement..."
        return list

    # 返回影响的行数
    @execute_all
    def update(self, sql, *args):
        # 这里返回count影响的行数
        count = -1
        startStr = sql.strip()[0:6] # 获取sql的前面关键字
        # 判断是否是insert、delete、update语句
        if startStr == "insert" or startStr == "delete" or startStr == "update":
            try:
                self.conn.autocommit(False)
                self.cursor.execute(sql) # 执行sql
                self.conn.commit() # 提交事务
                count = self.cursor.rowcount  # 获取sql影响的行数
            except Exception as e:
                print e # 打印错误信息
                self.conn.rollback() # 回滚数据
        else:
            print "sql语句格式不正确......"
        return count

    # 获取配置文件参数，并转化成参数
    def __readProp(self, filepath):
        dict = {}
        try:
            with open(filepath, 'r') as f:
                for line in f.readlines():
                    if '#' in line :
                        continue
                    list = line.strip().split("=")
                    key = list[0]
                    value = list[1]
                    if key == "port":
                        value = int(value)
                    dict[key] = value
        except Exception as e:
            print "读取文件异常,请检查文件是否存在"
            print e
        return dict