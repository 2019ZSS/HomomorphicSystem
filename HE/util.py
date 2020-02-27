# -*- coding: utf-8 -*-
'''
# Created on Feb-19-20 11:56
# util.py
# @author: ss
'''

'''
一些相关的数学函数
'''

import random
import math

def rabinMiller(num):
	s = num - 1
	t = 0
	while s % 2 == 0:
		s //= 2
		t += 1
	for trials in range(5):
		a = random.randrange(2,num-1)
		v = pow(a,s,num)
		if v!=1:
			i = 0
			while v!=(num-1):
				if i == t-1:
					return False
				else:
					i += 1
					v = (v**2)%num
	return True

lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
def isPrime(num):
	if num < 2:
		return False

	if num in lowPrimes:
		return True
	for prime in lowPrimes:
		if num % prime==0:
			return False

	return rabinMiller(num)


def powmod(a, b, mod):
    '''
    快速幂取模
    '''
    res = 1
    while b > 0:
        if (b & 1):
            res = res * a % mod
        a = a * a % mod
        b = b >> 1
    return res


def exgcd(a, b):
    '''
    扩展gcd
    '''
    if b == 0:
        return (a, 1, 0)
    else :
        (d, y, x) = exgcd(b, a % b)
        y -= x * (a // b)
        return (d, x, y)
 

def excrt(r, m, n):
    '''
    扩展中国剩余定理
    ''' 
    mo = m[0]
    re = r[0]
    for i in range(1, n):
        (d, x, y) = exgcd(mo, m[i])
        if ((r[i] - re) % d) != 0:
            return (0, re, mo)
        x = (r[i] - re) // d * x % (m[i] // d)
        re += x * mo
        mo = (mo // d) * m[i]
        re = re % mo
    re = (re + mo) % mo
    return (1, re, mo)


def getinv(a, b):
    '''
    求整数a关于b的逆元, 
    应满足(a, b) = 1
    '''
    d, x, y = exgcd(a, b)
    if d > 1:
        raise ValueError('The numbers a and b are not mutually prime')
    return (x % b + b) % b

def get_pri_root(fac, p):
    '''
    # 功能：求奇素数p的原根
    # 接受参数：fac列表元素, 包含p-1的所有素因子
    # 返回参数：p的原根g
    '''
    n = p - 1
    g = 2
    def check(g):
        for x in fac:
            if powmod(g, n // x, p) == 1:
                return False
        return True 
    while check(g) == False:
        g = g + 1
    return g

'''
# 功能：
# 接受参数：生成keysize长度的密钥
# 返回参数：
'''
def generateLargePrime(keysize=2048):
	while True:
		num = random.randrange(2**(keysize-1), 2**keysize)
		if isPrime(num):
			return num

def createcross(n=2):
    base = 2
    while base < n:
        base = base * 2
    
    A = [[1, 1],
         [1, -1]]
    
    def trans(A):
        data = []
        for x in A:
            data.append(sum([x, x], []))
        l = len(A)
        A_ = []
        for i in range(l):
            A_.append([])
            for j in range(l):
                A_[i].append(A[i][j] * -1)
        for i in range(l):
            data.append(sum([A[i], A_[i]], []))
        return data

    while len(A) < base:
        A = trans(A)
    
    random.shuffle(A)
    data = []
    for i in range(n):
        data.append(A[i])
    return data

def create_primes(num=2):
    '''
    从2开始生成num个连续的素数的列表
    [2, 3, 5, ...]
    '''
    primes = []
    x = 2
    while len(primes) < num:
        if isPrime(x) == True:
            primes.append(x)
        x = x + 1
    return primes

if __name__ == "__main__":
    # num = 9
    # data = createcross(n=num)
    # for i in range(num):
    #     for j in range(num):
    #         tmp = 0
    #         for k in range(len(data[i])):
    #             tmp += data[i][k] * data[j][k]
    #         tmp = tmp // len(data[i])
    #         print(i, j, tmp)
    # primes = create_primes(9)
    # print(primes)
    p = 2 * 3 * 5 * 7 + 1
    g = get_pri_root([2, 3, 5, 7], p)
    res = []
    for i in range(1, p):
        res.append(powmod(g, i, p))
    l = len(res)
    res = set(res)
    if l == len(res):
        print(g)
    # p = generateLargePrime()
    # p = str(p)
    # print(len(p))