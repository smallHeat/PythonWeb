#-*- coding:utf-8 -*-
import web
from DBUtils import db
import json
import mytools
'''

    @content url信息处理

'''
# 需要每次启动app都清空sessions文件夹

# 创建render对象
render = web.template.render("templates") # 使用同目录的templates作为模板目录

# 创建db对象
db = db.DB()

# 首页处理 这里处理登录后的页面
class index:
    def GET(self,name):
        if web.ctx.session.status == 0:
            web.seeother("/login")
        else:
            userid = web.ctx.session.userid # 这里不把user信息放到session中，增加存取速度
            # 根据userid 去查找user信息
            list_user = db.select("select * from user where id=?",userid)
            user_dict = mytools.dbType2Stand(list_user[0]) # 这里做个转换
            return render.index(user_dict) # 这里需要传入参数，这里采用dict数据类型做传递参数

# 登录 后期可以做个session缓存，可选择记住密码
class login:
    def GET(self):
        return render.login()

# 处理前端登录的请求
class loginHandle:
    def POST(self):
        # 返回json
        returnDict = {'status':-1}

        # 获取参数
        data = mytools.u2str(web.input())

        # 先判断是否为空
        if data.username != "" and data.password != "":
            # 如果不为空，则进行查询
            list = db.select("select * from login where username=? and password=?", data.username, data.password)

            # 先判断长度
            if len(list) > 0:
                # 再次校验，保证可靠性
                if list[0]['username'] == data.username and list[0]['password'] == data.password:
                    # 成功了，需要把参数放到session中
                    web.ctx.session.status = 1
                    web.ctx.session.userid = list[0]['id'] # 把用户信息放到session中
                    returnDict['status'] = 0 # 成功了，返回成功状态码

        return json.dumps(returnDict)

# 忘记密码
class forPasswdHandle():
    def POST(self):
        # 定义一个dict
        returnDict = {"status":-1}

        # 接收参数
        data = mytools.u2str(web.input()) # 得到参数并将unicode字符串，方便参数取用

        # 判断用户名 和 超级密码
        if data.username_forget != "" and data.super_password_forget != "" and data.new_password != "" \
             and data.confirm_password != "":
            # 根据用户名 和 超级密码去查询
            list = db.select("select * from login where username=? and super_pass=?", data.username_forget, data.super_password_forget)

            # 判断查询出来的结果dict的长度是否为0，如果为0，则失败了
            if len(list) > 0:
                # 说明是用户名和超级密码是正确的，可以修改密码了
                result = db.update("update login set password=? where username=? and super_pass=?", data.new_password, data.username_forget, data.super_password_forget)
                # 如果result 为-1，说明失败了,否则成功
                if result > -1:
                    returnDict['status'] = 0 # 返回成功状态码

        # 如果有为空的，就返回,这里已经初始了状态码,所以不用处理

        # 并且返回json字符串
        return json.dumps(returnDict)

# 注册处理
class registHandle:
    def POST(self):
        result = {} # ajax请求返回内容
        data = web.input() # data = web.data()# 得到原始数据
        data = mytools.u2str(data)

        if data.username_regist != "" and data.password_regist != "" and data.password2_regist != "" \
            and data.super_password_regist != "" and data.password_regist == data.password2_regist \
            and data.password2_regist != data.super_password_regist:
            # 这里需要验重, 根据用户名去查询
            dict = db.select("select * from login where username=?", data.username_regist)
            print dict
            if len(dict) == 0: # 没有重复
                # 这里进行注册
                # 第一步，先往login表中插入数据
                result_int = db.update("insert into login(username,password,super_pass) values(?,?,?)", data.username_regist, data.password_regist, data.super_password_regist)
                # 得到插入数据的id
                if result_int != -1:
                    result_tuple = db.select("select * from login where username=?", data.username_regist)
                    result_id = result_tuple[0]['id']
                    # 插入数据到user表中,id是插入login表生成的id,name是随机的一串字符串
                    result_int = db.update("insert into user(id, name) values(?,?)", int(result_id), mytools.myuuid())

                    # 返回状态码
                    result['status'] = 0 # 0代表成功
                else: # 插入数据库报错了，直接返回失败码
                    result['status'] = -1
                # 根据uuid自动生成一串字符串作为用户名，往user中插入数据
            else: # 这里代表重复了,已经存在这个用户了
                result['status'] = -2 # 重复返回-2
        else:
            # 失败了
            result['status'] = -1 # 失败返回-1
        return json.dumps(result)

class list:
    def GET(self):
        list = ["nono",'none','good','12346']
        return str(list)#render.list(list)