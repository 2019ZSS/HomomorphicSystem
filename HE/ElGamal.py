# -*- coding: utf-8 -*-
'''
# Created on Feb-22-20 12:30
# ElGamal.py
# @author: ss
# 说明: 实现了ElGamal加密算法
'''

import sys 
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
import random
import time 
from HE.util import generateLargePrime, isPrime, get_pri_root, powmod, getinv

class ElGamalPublicKey(object):
    '''
    ElGamal加密算法
    q 是奇素数
    g 是q的原根
    h = g ^ x % q
    # encrypt_int:
    # evaluate_int:
    '''
    def __init__(self, q, g, h):
        self.q = q 
        self.g = g
        self.h = h

    def __repr__(self):
        return 'PublicKey({}, {}, {})'.format(self.q, self.g, self.h)

    def encrypt_int(self, m):
        '''
        # 功能：
        # 接受参数：m加密明文
        # 返回参数：密文C(c1, c2)
        '''
        y = random.randint(1, self.q - 1)
        c1 = powmod(self.g, y, self.q)
        s = powmod(self.h, y, self.q)
        c2 = m * s % self.q
        return (c1, c2)
    
    def evaluate_int(self, C1, C2):
        '''
        # 功能：实现两个密文间的同态乘法
        # 接受参数：C1(c1, c2)
        # 返回参数：C(c1, c2)
        '''
        return (C1[0] * C2[0] % self.q, C1[1] * C2[1] % self.q)

class ElGamalPrivateKey(object):
    '''
    x集合于(1, q - 1)
    '''
    def __init__(self, q, x):
        self.q = q 
        self.x = x 

    def __repr__(self):
        return 'PrivateKey({}, {})'.format(self.q, self.x)
    
    def decrypt_int(self, C):
        '''
        # 功能：
        # 接受参数：
        # 返回参数：
        '''
        s = powmod(C[0], self.x, self.q)
        invs = powmod(s, self.q - 2, self.q)
        m = C[1] * invs % self.q 
        return m

def keyGen(keysize=1024):
    '''
    # 功能：生成keysize比特的密钥
    # 接受参数：keysize
    # 返回参数：(q, g, h), (q, x)
    q 是奇素数
    g 是q的原根
    h = g ^ x % q
    x 集合于(1, q - 1)
    公钥:(q, g, h)
    私钥: (q, x)
    '''
    num = random.randint(2, 3)
    start = time.time()
    def generate_q():
        while True:
            q = 1
            fac = [2]
            if num == 2:
                fac.append(generateLargePrime(keysize // 2 - 1))
                fac.append(generateLargePrime(keysize // 2))
            else:
                fac.append(generateLargePrime(keysize // 4 - 1))
                fac.append(generateLargePrime(keysize // 4))
                fac.append(generateLargePrime(keysize // 2))
            for x in fac:
                q = q * x
            q = q + 1 
            if isPrime(q) == True:
                return (q, fac)
    (q, fac) = generate_q()
    g = get_pri_root(fac, q)
    x = random.randint(1, q - 1)
    h = powmod(g, x, q)
    end = time.time()
    print('密钥生成耗时: {}s'.format(end - start))
    return (ElGamalPublicKey(q, g, h), ElGamalPrivateKey(q, x))

def save_key(key, filename, mode=0):
    '''
    # 功能：保存ElGamal算法算法所需要的密钥
    # 接受参数：key是对应的公钥或者私钥类, filename(密钥文件名), mode为0代表公钥类 1是私钥
    # 返回参数：True(保存成功) / False(保存失败)
    '''
    try:
        if mode != 1:
            mode == 0
        with open(filename, 'w', encoding='utf-8') as f:
            if mode == 0:
                content = str(key.q) + ',' + str(key.g) + ',' + str(key.h)
                f.write(content)
                return True 
            elif mode == 1:
                content = str(key.q) + ',' + str(key.x)
                f.write(content)
                return True 
            return False
    except Exception as e:
        print(e)
        return False

def load_key(filename, mode = 0):
    '''
    # 功能：加载ElGamal算法所需要的密钥
    # 接受参数：filename(密钥文件名), mode为0代表加载的为公钥, mode为1代表加载为私钥
    # 返回参数：成功打开则返回pubkey(q, g, h) / prikey(q, x) 失败为False
    '''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read(-1).split(',')
            for i in range(len(data)):
                data[i] = int(data[i])
            if mode == 1:
                (q, x) = data[0], data[1]
                return ElGamalPrivateKey(q, x)
            else:
                (q, g, h) = data[0], data[1], data[2]
                return ElGamalPublicKey(q, g, h)
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    keysize = 2048
    pubname = './key/public_key_' + str(keysize) + '.txt'
    priname = './key/private_key_' + str(keysize) + '.txt'

    pubkey, prikey = keyGen(keysize=keysize)
    ok = save_key(pubkey, pubname, 0)
    print(ok)
    ok = save_key(prikey, priname, 1)
    print(ok)

    pubkey = load_key(pubname, 0)
    prikey = load_key(priname, 1)

    num1 = 2**100
    num2 = 3
    C1 = pubkey.encrypt_int(num1)
    C2 = pubkey.encrypt_int(num2)
    ans = prikey.decrypt_int(pubkey.evaluate_int(C1, C2))
    print(ans == num1 * num2)