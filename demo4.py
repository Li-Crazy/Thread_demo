'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/1 21:38
@Software: PyCharm
@File    : demo4.py
'''
import threading
import time
import random

#Lock版本的生产者与消费者模式

gmoney = 1000#定义全局变量
gLock = threading.Lock()#定义全局共享锁
gTotalTimes = 10
gTimes = 0

class Producer(threading.Thread):
    def run(self):
        global gmoney
        global gTimes
        while True:
            money = random.randint(100,1000)
            gLock.acquire()
            if gTimes >= gTotalTimes:
                gLock.release()
                break
            gmoney += money
            print("%s生产了%d元钱，剩余%d元钱" %(threading.current_thread(),money,gmoney))
            gTimes += 1
            gLock.release()
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        global gmoney
        while True:
            money = random.randint(100,1000)
            gLock.acquire()
            if gmoney >= money:
                gmoney -= money
                print("%s消费了%d元钱，剩余%d元钱" %(threading.current_thread(),money,gmoney))
            else:
                if gTimes >= gTotalTimes:
                    gLock.release()
                    break
                print("%s准备消费%d元钱，剩余%d元钱，不足！" % (
                threading.current_thread(), money, gmoney))

            gLock.release()
            time.sleep(1)

def main():
    for x in range(3):
        t2 = Consumer(name="消费者线程：%d" %x)
        t2.start()

    for x in range(5):#5个生产者
        t1 = Producer(name="生产者线程：%d" %x)
        t1.start()


if __name__ == '__main__':
    main()