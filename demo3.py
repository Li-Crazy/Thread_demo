'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/1 20:34
@Software: PyCharm
@File    : demo3.py
'''
import threading
import time

#多线程共享全局变量,线程执行顺序是无序的，可能会造成数据错误，加锁可解决该问题
VALUE = 0#定义全局变量
gLock = threading.Lock()#创建一个锁

def add_value():
    global VALUE#声明全局变量
    gLock.acquire()#加锁,对修改全局变量的地方加锁进行限制，访问全局变量的地方则不进行限制
    for i in range(1000000):
        VALUE += 1
    gLock.release()#解锁
    print("Value:%d" %VALUE)

def main():
    for x in range(2):
        t = threading.Thread(target=add_value)
        t.start()

if __name__ == '__main__':
    main()
