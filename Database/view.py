# -*- coding: utf-8 -*-
'''
# Created on Feb-22-20 21:42
# view.py
# @author: ss
主要实现veiw模块的数据库接口
'''

import sys 
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from Database.util import op_mysql, md5
from Database.vote import getVoteData
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np  
import random

def getVoteActivities(usr):
    '''
    # 功能：从launch表中返回usr发起的投票记录
    # 接受参数：usr
    # 返回参数：[(title, captcha)]
    '''
    usr = md5(usr)
    sql = "select title, captcha from launch where usr = '%s'" % usr
    flag, res = op_mysql(sql)
    if flag == False:
        print(False)
        return []
    data = []
    for x in res:
        data.append([x[0], x[1]])
    return data

def delVoteActivity(captcha):
    '''
    # 功能：在launch, votedata, voterecords表captcha的相关记录
    # 接受参数：captcha
    # 返回参数：True / False
    '''
    sql = "delete from votedata where captcha = '%s'" % captcha
    flag, e = op_mysql(sql)
    if flag == False:
        print(e)
        return False
    sql = "delete from voterecords where captcha = '%s'" % captcha
    flag, e = op_mysql(sql)
    if flag == False:
        print(e)
        return False
    sql = "delete from launch where captcha='%s'" % captcha
    flag, e = op_mysql(sql)
    if flag == False:
        print(e)
        return False 
    return True 

def showVoteResult(captcha, total, prikey):
    '''
    # 功能：展示投票captcha记录对应选项的投票情况
    # 接受参数：
    # 返回参数：
    '''
    data = getVoteData(captcha)
    choices = []
    tags = []
    for x in data:
        choices.append(x[0])
        tags.append(x[1])
    total = prikey.decrypt_int(total)
    cnt = []
    for i in range(len(tags)):
        c = 0
        while total % tags[i] == 0:
            c = c + 1
            total = total // tags[i]
        cnt.append(c)
    res = []
    for i in range(len(tags)):
        res.append([choices[i], cnt[i]])
    return res 

def drawResult(res):
    '''
    # 功能：讲投票结果画图展示
    # 接受参数：
    # 返回参数：
    '''
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False     
    # 生成画布
    plt.figure(figsize=(15, 10), dpi=45)
    plt.xlabel('选项', fontsize = 30)
    plt.ylabel('票数', fontsize = 30)
    # 横坐标名字
    x_name = []
    # 纵坐标数值
    y = []
    colors = ['b','r','g', 'y','c','m', 'k',]
    color = []
    for x in res:
        x_name.append(x[0])
        y.append(x[1])
        color.append(colors[random.randint(0, len(colors) - 1)])
    
    x = range(len(x_name))
    plt.bar(x, y, width = 0.5, color=color)
    plt.xticks(x, x_name)
    plt.tick_params(labelsize = 30) #刻度字体大小
    y_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    # plt.ylim(0, 110)
    plt.show()

if __name__ == "__main__":
    print('view')
    # print(getVoteActivities(usr='ss'))
    # print(delVoteActivity(captcha='c3d509ebd011c4428abad04c1f171ac0'))
    from HE.ElGamal import load_key
    prikey = load_key('./key/private_key_1024.txt', 1)
    total = (73006748275733636218048020563930510078205641539569890643694208683861027340726992334498703790974548043230490037981988123164203440268887688554220395053771620301180901966961733308086226907694824920391711711745104503213700285255514034043268458926383056924128882016307643694746808808628037534348312797433840387504,51788387409976820595063099221728719586902581829729401265359212965595520568156833861654024307622665835082124502996207283884294332205777020984097432945087364300983088401416689472543789226422183908571330805825970243497901837696057839686866529828639704838019526810188499451150024742215167963446710436819881221761)
    res = showVoteResult('c3d509ebd011c4428abad04c1f171ac0', total, prikey)
    print(res)
    drawResult(res)