'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/2 12:50
@Software: PyCharm
@File    : doutula_demo.py
'''
import threading
from queue import Queue
import requests
from lxml import etree
from urllib import request
import os
import re

class Procuder(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 '
                      'QQBrowser/10.4.3469.400'
    }

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)


    def parse_page(self,url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        # print(text)
        html = etree.HTML(text)
        imgs = html.xpath(
            '//div[@class="page-content text-center"]//img[@class!="gif"]')
        for img in imgs:
            # print(etree.tostring(img))
            img_url = img.get("data-original")
            title = img.get("alt")
            title = re.sub(r'[\?？\.，。！\*!]', ' ', title)
            # splitext -> ext -> extension 扩展名
            suffix = os.path.splitext(img_url)[1]  # 分割后缀名
            filename = title + suffix
            file = 'image/'+filename
            self.img_queue.put((img_url,file))
            # print(img_url)
            # request.urlretrieve(img_url, 'images/' + filename)

class Consumer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 '
                      'QQBrowser/10.4.3469.400'
    }

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, file = self.img_queue.get()
            with open(file, 'wb') as f:
                # f.write(img_url)
                f.write(requests.get(img_url, headers=self.headers).content)
                print(file + "  下载完成！ ")

def main():
    page_queue = Queue(10)
    img_queue = Queue(100)
    for i in range(1, 10):
        url = "https://www.doutula.com/photo/list/?page=%d" % i
        # print(url)
        page_queue.put(url)


    for x in range(5):
        t1 = Procuder(page_queue,img_queue)
        t1.start()

    for x in  range(5):
        t2 = Consumer(page_queue,img_queue)
        t2.start()

if __name__ == '__main__':
    main()
