# -*- coding: utf-8 -*-
'''
# Created on Feb-21-20 21:28
# vote.py
# @author: ss
参与投票模块数据库接口函数实现
'''

import sys 
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from Database.util import op_mysql, md5

def getVoteData(captcha):
    '''
    # 功能：在votedata表中返回captcha记录对应(choice, tag)
    # 接受参数：captcha
    # 返回参数：[[choice(str), tag(int)]...]
    '''
    sql = "select choice, tag from votedata where captcha = '%s'" % (captcha)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return []
    data = []
    for x in res:
        data.append([x[0], x[1]])
    return data

def checkUsrRecord(captcha, usr):
    '''
    # 功能：在voterecords表中检查(cpatcha, usr)对应记录是否存在
    # 接受参数：
    # 返回参数：
    1 记录存在
    0 数据库端出错
    -1 记录不存在
    '''
    usr = md5(usr)
    sql = "select votenum from voterecords where captcha='%s' and usr='%s'" % (captcha, usr)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return 0
    elif len(res) == 0:
        return -1
    return 1

def insertUsrRecord(captcha, usr, votenum):
    '''
    # 功能：在voterecords表中插入一条记录
    # 接受参数：
    # 返回参数：True / False
    '''
    usr = md5(usr)
    sql = "insert into voterecords (captcha, usr, votenum) values ('{}', '{}', {})".format(captcha, usr, votenum)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
    return flag

def getVotenum(captcha, usr, votelimit):
    '''
    # 功能：在voterecords表中获取cpatcha和usr相对应的votenum
    # 接受参数：cpatcha, usr, votelimit(int)
    # 返回参数：votenum(int)
    -1 数据库端错误
    or votenum
    '''
    flag = checkUsrRecord(captcha, usr)
    if flag == 0:
        return -1
    elif flag == -1:
        flag = insertUsrRecord(captcha, usr, votelimit)
        if flag == True:
            return votelimit
        else:
            return -1
    usr = md5(usr)
    sql = "select votenum from voterecords where captcha='%s' and usr='%s'" % (captcha, usr)
    flag, res = op_mysql(sql)
    if flag == 0:
        print(res)
        return -1
    for x in res:
        return x[0]

def updataUsrRecord(captcha, usr, votenum):
    '''
    # 功能：更新voterecords表中的某活动用户投票数量
    # 接受参数：
    # 返回参数：True / False
    '''
    usr = md5(usr)
    sql = """update voterecords set votenum = {} where captcha = '{}' and usr = '{}'""".format(votenum, captcha, usr)   
    flag, res = op_mysql(sql)
    if flag == False:
        print(flag)
    return flag

if __name__ == "__main__":
    print('vote')
    print(updataUsrRecord(captcha='c3d509ebd011c4428abad04c1f171ac0', usr='ss', votenum=3))