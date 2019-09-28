'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/1 20:21
@Software: PyCharm
@File    : demo2.py
'''
import threading
import time

class CodingThread(threading.Thread):#继承Thread类
    def run(self):#调用Thread类自动运行run函数
        for x in range(3):
            print("正在编码：%s" % x)
            time.sleep(1)

class DrawingThread(threading.Thread):
    def run(self):
        for x in range(3):
            print("正在绘图：%s" % threading.current_thread())  # 返回当前线程名字
            time.sleep(1)

def thread_main():
    first = CodingThread()
    second = DrawingThread()

    first.start()
    second.start()

if __name__ == '__main__':
    thread_main()