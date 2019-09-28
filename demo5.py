'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/2 8:46
@Software: PyCharm
@File    : demo5.py
'''
import threading
import time
import random

#Condition版本的生产者与消费者模式

gmoney = 1000#定义全局变量
gCondition = threading.Condition()#threading.Condition()在没有数据的情况下处于阻塞等待状态
gTotalTimes = 10
gTimes = 0

class Producer(threading.Thread):
    def run(self):
        global gmoney
        global gTimes
        while True:
            money = random.randint(100,1000)
            gCondition.acquire()
            if gTimes >= gTotalTimes:
                gCondition.release()
                break
            gmoney += money
            print("%s生产了%d元钱，剩余%d元钱" %(threading.current_thread(),money,gmoney))
            gTimes += 1
            gCondition.notify_all()
            #notify#通知某个处于等待状态的线程，默认第一个，需要在release之前调用
            #notify_all#通知所有处于等待状态的线程，需要在release之前调用
            gCondition.release()
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        global gmoney
        while True:
            money = random.randint(100,1000)
            gCondition.acquire()
            while gmoney < money:
                if gTimes >= gTotalTimes:
                    gCondition.release()
                    return
                print("%s准备消费%d元钱，剩余%d元钱，不足！" % (threading.current_thread(), money, gmoney))
                gCondition.wait()#wait#让当前线程处于等待状态，并将锁释放
            gmoney -= money
            print("%s消费了%d元钱，剩余%d元钱" %(threading.current_thread(),money,gmoney))
            gCondition.release()
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