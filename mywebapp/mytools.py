#-*- coding:utf-8 -*-
import os
import random
from config import sex,label
CHARACTER_SELF = "qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP"
# 随机产生长度为n的字符串
def randomPart1(part_str, n):
    str = ""
    for i in range(n):
        str += part_str[random.randint(0,len(part_str) - 1)]
    return str

# n代表偶数位是字母还是数字 0代表字母 1代表数字
def randomPart3(num, n):
    str_temp = ""
    for i in range(num):
        temp = str(random.randint(0, 9))
        if i % 2 == n:
            str_temp += CHARACTER_SELF[random.randint(0, len(CHARACTER_SELF) - 1)]
        else:
            str_temp += temp
    return str_temp

# 第四部分
def randomPart4(n):
    RANDOM_STR = CHARACTER_SELF + "0123456789" # 共62个
    return randomPart1(RANDOM_STR, n)

# 产生一串随机字符串
def myuuid():
    # 总共由 16 个字符和3个连接符_组成
    #第一部分4个纯字母 第二部分纯数字 第三部分字母数字混合 第四部门 在0-9加上52个字母中随机
    part = randomPart1(CHARACTER_SELF, 4) +\
           "_" + str(random.randint(1000, 9999)) +\
           "_" + randomPart3(4, random.randint(0, 1)) +\
           "_" + randomPart4(4)
    return part

# 把unicode编码的转成str
def u2str(data):
    for k in data:
        data[k] = str(data[k])
    return data

# 将数据库中的数据转成显示语言
def dbType2Stand(dict):
    if dict['userdesc'] == '':
        dict['userdesc'] = '这个人很懒，什么都没留下......'
    dict['userlabel_class'] = label.userlabel_class[int(dict['userlabel'])] # 获取样式
    dict['sex'] = sex.SEX[int(dict['sex'])] # 性别转化
    dict['userlabel'] = label.userlabels[int(dict['userlabel'])]  #用户标签转化
    dict['skilllabel'] = label.skilllabels[int(dict['skilllabel'])]  # 技术标签转化
    dict['jobtype'] = label.jobtype[int(dict['jobtype'])]  # 技术标签转化
    return dict