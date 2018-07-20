#-*- coding:utf-8 -*-
import web
'''

    @content url信息处理

'''

# 创建render对象
render = web.template.render("templates") # 使用同目录的templates作为模板目录

# 首页处理
class index:
    def GET(self,name):
        if web.ctx.session.status == 0:
            web.seeother("/login")
        return name

# 登录
class login:
    def GET(self):
        return render.login()

class list:
    def GET(self):
        list = ["nono",'none','good','12346']
        return str(list)#render.list(list)