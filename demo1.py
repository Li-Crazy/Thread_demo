'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/1 17:05
@Software: PyCharm
@File    : demo1.py
'''
import time
import threading

#传统方式
def coding():
    for x in range(3):
        print("正在编码：%s" %x)
        time.sleep(1)

def drawing():
    for x in range(3):
        print("正在绘图：%s" %threading.current_thread())#返回当前线程名字
        time.sleep(1)

def main():
    t1 = time.clock()
    coding()
    drawing()
    t2 = time.clock()
    print(t2-t1)

#采用多线程

def thread_main():
    first = threading.Thread(target=coding)
    second = threading.Thread(target=drawing)

    first.start()
    second.start()

    print(threading.enumerate())#threading.enumerate() 返回正在运行的线程列表

if __name__ == '__main__':
    main()
    thread_main()