# -*- coding: utf-8 -*-
'''
# Created on Feb-18-20 22:26
# FHE.py
# @author: ss
'''

'''
实现支持部分加密函数的全态加密
'''

import random
import util

module_list = [21487, 82559, 70481, 28579, 59957, 87299]
def testKey(prikey, pubkey, n):
    for i in range(1000):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        add = x + y
        mul = x * y
        x = Encryption(x, pubkey, n)
        y = Encryption(y, pubkey, n)
        _add = Decrypt(x + y, prikey, n)
        _mul = Decrypt(x * y, prikey, n)
        # print(add, mul, _add, _mul)
        if (add != _add) or (mul != _mul):
            return False
    return True

def _keyGen(lamda=64, down=100, up=10000):
    '''
    lamda: 参数
    '''
    p = lamda
    prikey_len = lamda * 2 + random.randint(1, lamda)
    pubkey_len = lamda * 3 + random.randint(1, lamda)
    
    prikey = random.randrange(2**(prikey_len-1) + 1, 2**prikey_len)
    while prikey % 2 == 0:
        prikey = random.randrange(2**(prikey_len-1) + 1, 2**prikey_len)

    pubkeynum = pubkey_len + lamda
    pubkey = []
    c = 2**pubkey_len
    d = 2**lamda

    n = random.randrange(down, up)
    while util.isPrime(n) == False:
        n = random.randrange(down, up)

    pubkey = []
    for i in range(0, pubkeynum):
        q = random.randrange(0, c // prikey)
        r = random.randrange(0, d)
        pubkey.append(prikey * q + n * r)
    
    return (prikey, pubkey, n)

def KeyGen(lamda=64, down=100, up=10000):
    '''
    lamda: 参数
    '''
    while True:
        prikey, pubkey, n = _keyGen(lamda, down, up)
        if testKey(prikey, pubkey, n) == True: 
            return (prikey, pubkey, n)

def save_key(filename, key):    
    try:
        # if not isinstance(key, int):
        #     raise ValueError('Expected int type plaintext but got: %s' % type(key))
        with open(filename, 'w', encoding='utf-8') as f:
            if not isinstance(key, int):
                s = str(key[0])
                for i in range(1, len(key)):
                    s = s + ' ' + str(key[i])
                f.write(s)
            else:
                f.write(str(key))
    except Exception as e:
        print(e)

# 加载密钥
def load_key(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            x = f.read(-1).split(' ')
            for i in range(len(x)):
                x[i] = int(x[i])
            if len(x) == 1:
                return x[0]
            else:
                return x
    except Exception as e:
        print(e)


def Encryption(m, pubkey, n):
    '''
    m: 明文整数
    pubkkey: 公钥
    n: 明文空间模数(n > m)
    '''
    if m >= n:
        raise ValueError('m must less than n!')
    r = random.randint(1, 9)
    num = len(pubkey) #使用的公钥数量随机
    tmp = [x for x in pubkey]
    random.shuffle(tmp)
    res = 0
    for i in range(num):
        res = res + tmp[i]
        # res = res + pubkey[i]
    c = m + n * r + res
    return c

def Decrypt(c, prikey, n):
    return (c % prikey) % n

if __name__ == "__main__":
    # lamda = 64
    # prikey, pubkey, n = KeyGen(lamda, down=10000, up=100000)
    # save_key('./key/prikey.txt', prikey)
    # save_key('./key/pubkey.txt', pubkey)
    # save_key('./key/module.txt', n)

    prikey = load_key('./key/prikey.txt')
    pubkey = load_key('./key/pubkey.txt')
    n = load_key('./key/module.txt')
    num = 10
    data = util.createcross(num)
    inv_len =  util.getinv(len(data[0]), n)
    enc_inv_len = Encryption(inv_len, pubkey, n)

    for i in range(num):
        for j in range(len(data[i])):
            data[i][j] = Encryption(data[i][j], pubkey, n)
    
    # d = [Encryption(0, pubkey, n) for i in range(len(data))]
    print(n)
    # x = Encryption(-1, pubkey, n)
    # y = Encryption(-1, pubkey, n)
    # z = Encryption(1, pubkey, n)
    # print(util.getinv(2, n))
    # # d = Encryption(util.getinv(2, n), pubkey, n)
    # print(Decrypt((x * y + z * z), prikey, n))
    # print(2 * util.getinv(2, n) % n)

    d = [Encryption(0, pubkey, n) for i in range(len(data))]
    for t in range(10):
        for i in range(num):
            for j in range(num):
                tmp = 0
                for k in range(len(data[i])):
                    tmp = tmp + data[i][k] * data[j][k] 
                d[i] = d[i] + tmp 
    d = [Decrypt(d[i], prikey, n) for i in range(len(data))]
    print(d)