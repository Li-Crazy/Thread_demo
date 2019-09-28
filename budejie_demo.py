'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/3 10:38
@Software: PyCharm
@File    : budejie_demo.py
'''
import requests
import threading
import csv
from lxml import etree
from queue import Queue

class BSSpider(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 "
                      "QQBrowser/10.4.3469.400"
    }

    def __init__(self, page_queue, joke_queue, *args, **kwargs):
        super(BSSpider,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.joke_queue = joke_queue
        self.base_domain = "http://www.budejie.com"

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            # print(url)
            self.parse_page(url)

    def parse_page(self,url):
        response = requests.get(url,headers=self.headers)
        text = response.text
        # print(text)
        html = etree.HTML(text)
        descs = html.xpath('//div[@class="j-r-list-c-desc"]')
        for desc in descs:
            link = self.base_domain + desc.xpath('.//a/@href')[0]
            jokes = desc.xpath('.//text()')
            joke = "\n".join(jokes).strip()
            self.joke_queue.put((joke,link))


class BSWriter(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 "
                      "QQBrowser/10.4.3469.400"
    }
    def __init__(self, writer,gLock, joke_queue, *args, **kwargs):
        super(BSWriter,self).__init__(*args,**kwargs)
        self.writer = writer
        self.joke_queue = joke_queue
        self.gLock = gLock

    def run(self):
        while True:
            try:
                joke_info = self.joke_queue.get(timeout=20)
                joke,link = joke_info
                self.gLock.acquire()
                self.writer.writerow((joke,link))
                self.gLock.release()
            except:
                break

def main():
    page_queue = Queue(10)
    joke_queue = Queue(500)
    gLock = threading.Lock()
    fp = open('baisibudejie.csv','a',newline='',encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('content','link'))

    for i in range(1, 11):
        url = "http://www.budejie.com/text/%d" % i
        page_queue.put(url)

    for i in range(5):
        t1 = BSSpider(page_queue,joke_queue)
        t1.start()

    for i in range(5):
        t2 = BSWriter(writer,gLock,joke_queue)
        t2.start()

if __name__ == '__main__':
    main()
