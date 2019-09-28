'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/5/2 12:50
@Software: PyCharm
@File    : doutula_demo.py
'''
import requests
from lxml import etree
from urllib import request
import os
import re


def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 '
                      'QQBrowser/10.4.3469.400'
    }
    response = requests.get(url, headers=headers)
    text = response.text
    # print(text)
    html = etree.HTML(text)
    imgs = html.xpath(
        '//div[@class="page-content text-center"]//img[@class!="gif"]')
    for img in imgs:
        # print(etree.tostring(img))
        img_url = img.get("data-original")
        title = img.get("alt")
        title = re.sub(r'[\?？\.，。！!]', ' ', title)
        # splitext -> ext -> extension 扩展名
        suffix = os.path.splitext(img_url)[1]  # 分割后缀名
        filename = title + suffix
        file = 'images/'+filename
        # print(img_url)
        # request.urlretrieve(img_url, 'images/' + filename)
        with open(file,'wb') as f:
            # f.write(img_url)
            f.write(requests.get(img_url, headers=headers).content)

def main():
    for i in range(1, 10):
        url = "https://www.doutula.com/photo/list/?page=%d" % i
        # print(url)
        parse_page(url)
        break

if __name__ == '__main__':
    main()
