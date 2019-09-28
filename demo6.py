'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/2 10:25
@Software: PyCharm
@File    : demo6.py
'''
from queue import Queue
import time
import threading

#Queue线程安全队列
q = Queue(4)#初始化Queue（maxsize），创建一个先进先出队列，共有四个
q.put(1)#放入数据
q.put(2)

print(q.get())#从队列中取出最先放入的数据
print(q.qsize())#返回队列大小
print(q.empty())#判断队列是否为空
print(q.full())#判断队列是否为满

def set_value(q):
    index = 0
    while True:
        q.put(index)#block参数默认为True，队列满了则一直阻塞在此处
        index += 1
        time.sleep(2)

def get_value(q):
    while True:
        print(q.get(block=True))#block参数默认为True，获取不到值则一直阻塞在此处

def main():
    q = Queue(4)
    t1 = threading.Thread(target=set_value,args=[q])
    t2 = threading.Thread(target=get_value,args=[q])

    t1.start()
    t2.start()

if __name__ == '__main__':
    main()
