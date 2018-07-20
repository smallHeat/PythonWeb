# -*- coding:utf-8 -*-
from urls import *
from handler import *
import web

'''

	程序入口

'''

# 创建app对象
app = web.application(urls, globals())

#创建session对象
web.config.debug = False
web.config.session_parameters['timeout'] = 300, #24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['ignore_expiry'] = False

if web.config.get('_session') is None:
    print "初始化session...."
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={"status": 0})
    web.config._session = session
else:
    print "把已有session.......返回"
    session = web.config._session

def session_hook():
    print "注册session"
    print session
    web.ctx.session = session
    print web.ctx.session
app.add_processor(web.loadhook(session_hook))

# 程序入口
if __name__ == "__main__":
    app.run()