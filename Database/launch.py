# -*- coding: utf-8 -*-
'''
# Created on Feb-21-20 17:02
# launch.py
# @author: ss
投票发起模块数据库接口实现
'''


import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from Database.util import op_mysql, md5
from HE.util import isPrime

def check_captcha(captcha):
    '''
    # 功能：检查captcha活动是否记录在launch之中
    # 接受参数：captcha
    # 返回参数：
    1 launch中不存在该记录
    0 数据库端错误
    -1 已经创建过相同的活动
    '''
    sql = "select captcha from launch where captcha = '%s'" % (captcha)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return 0
    elif len(res):
        return -1
    return 1

def insert_launch(usr, title, captcha, votelimit, total):
    '''
    功能：往lauch表中插入一条活动记录
    接受参数：
    usr: 创建者
    title: 活动标题
    capthca: 邀请码(唯一)
    votelimit(int): 个人投票有效票数 
    total(text)
    返回参数：
    1 插入成功
    0 数据库端错误
    -1 验证码不唯一, 已经创建过相同的活动
    '''
    flag = check_captcha(captcha)
    if flag == 0:
        return 0  # 数据库端错误
    elif flag == -1:
        return -1 # 验证码不唯一, 已经创建过相同的活动
    usr = md5(usr)
    sql = "insert into launch(usr, title, captcha, votelimit, total) values('{}', '{}', '{}', {}, '{}')".format(usr, title, captcha, votelimit, total)
    flag, e = op_mysql(sql)
    if flag == False:
        print(e)
        return 0 #数据库端错误
    else :
        return 1 #插入成功

def del_launch(captcha):
    '''
    功能：在lauch表中删除一条活动记录
    接受参数：
    capthca: 邀请码(唯一)
    返回参数：
    1 删除成功
    0 数据库端错误
    '''
    sql = "delete from launch where captcha='%s'" % (captcha)
    flag, e = op_mysql(sql)
    if flag == False:
        print(e)
        return 0
    else:
        return 1

def insert_votedata(captcha, choice, tag):
    '''
    # 功能：往votedata插入邀请码为captcha的候选数据
    # 接受参数：
    capthca(str): 验证码
    choice(str)： 候选人
    tag(int): 素数标记 
    # 返回参数：
    1 成功插入
    0 数据库端错误
    -1 tag不是素数
    '''
    if isPrime(tag) == False:
        return -1
    sql = "insert into votedata(captcha, choice, tag) values('{}', '{}', {})".format(captcha, choice, tag)
    flag, e = op_mysql(sql)
    if flag == False:
        print(e)
        return 0 
    else:
        return 1

def getVoteContent(captcha):
    '''
    # 功能：寻找captcha活动记录对应的title, votelimit
    # 接受参数：captcha
    # 返回参数：[] / [title(str), votelimit(int)]
    '''
    sql = "select title, votelimit from launch where captcha = '%s'" % (captcha)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
        return []
    data = []
    for x in res:
        data.append(x[0])
        data.append(x[1])
        break
    return data

def getTotal(captcha):
    '''
    # 功能：获取记录captcha的投票总数密文
    # 接受参数：captcha
    # 返回参数：text(int, int) / False
    '''
    sql = "select total from launch where captcha = '%s'" % captcha
    flag, res = op_mysql(sql)
    if flag == False:
        print(e)
        return False
    data = []
    for x in res:
        for y in x:
            y = y.split(',')
            return (int(y[0]), int(y[1]))

def updateTotal(captcha, pubkey, C2):
    '''
    # 功能：更新记录captcha对应的投票总数
    # 接受参数：captcha(邀请码), pubkey(公钥), C2(int)
    # 返回参数：
    '''
    C1 = getTotal(captcha)
    C = pubkey.evaluate_int(C1, C2)
    C = str(C[0]) + ',' + str(C[1])
    sql = "update launch set total = '{}' where captcha = '{}'".format(C, captcha)
    flag, res = op_mysql(sql)
    if flag == False:
        print(res)
    return flag

if __name__ == "__main__":
    text="105679570314070008906695576860036774644997616293187458824057821722575735579576383209647157648542846337835732676760723515938768988782576095488730151238682179861265072640172421465599166008633732190210360139781485224354329173518981264532032282680302660287143056649983633040755213407904146422250202492399542205913,28867790528411234454795469069036503185705893650262977031048807700387658344324896177178915235522981196708068853214935124857198173561240688698087256554953690177238542326039706423441690313495526728302964790019718704124366546305904418546249950987768241490619076014415418159539477100242654556432903574784777131061"

    print('launch')
    # print(insert_launch('ss', 'test', '714d7578a8785d637b44688e50df34f6'))
    # print(insert_votedata('714d7578a8785d637b44688e50df34f6', 'ss', 2))
    # print(check_captcha('e8378b63b19fb0a7e7afea2e4b7b6ba'))
    # print(getVoteContent('e8378b63b19fb0a7e7afea2e4b7b6ba6'))
    # print(getTotal('c3d509ebd011c4428abad04c1f171ac0'))
    from HE.ElGamal import load_key
    pubkey = load_key('./key/public_key_1024.txt', 0)
    prikey = load_key('./key/private_key_1024.txt', 1)
    C2 = pubkey.encrypt_int(1)
    print(updateTotal('c3d509ebd011c4428abad04c1f171ac0', pubkey, C2))
    C = getTotal('c3d509ebd011c4428abad04c1f171ac0')
    print(prikey.decrypt_int(C))