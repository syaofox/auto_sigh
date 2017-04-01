#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep

import re
import requests

class Jokespider:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4'})
        self.urls = set()
        self.oldurls = set()

    def get_url(self):
        url = self.urls.pop()
        self.oldurls.add(url)
        return url

    def has_url(self):
        return len(self.urls) > 0

    def add_url(self,url):
        if not url :return
        if url not in self.urls and url not in self.oldurls:
            self.urls.add(url)

    def down_page(self,url,param=None):
        res = self.session.get(url,params=param,timeout=5)
        if res.status_code == 200:
            return res.text

    def parse_page(self,html_text):
        if html_text:
            try:
                url = re.search(r'id="comment-more".*?href="(.*?)".*?浏览下一个，笑话更精彩~',html_text,re.S).group(1)
                joke_txt = re.search(r'<div class="joke-text">(.*?)</div>', html_text, re.S).group(1) #.strip().replace('<p>','').replace('</p>','\n').replace('       ','')
                joke_txt = re.sub(r'&.*?;','',joke_txt)
                joke_txt = re.sub(r'\s', '', joke_txt)
                joke_txt = re.sub(r'<p>', '', joke_txt)
                joke_txt = re.sub(r'</p>', '\n', joke_txt)
                return joke_txt,url
            except Exception:
                pass

    def crawl(self):
        self.add_url('http://m.zol.com.cn/xiaohua/detail40/39904.html')
        while True:
            try:
                if self.has_url():
                    url =self.get_url()
                    res = self.down_page(url)
                    html_txt, new_url = self.parse_page(res)
                    self.add_url(new_url)
                    if html_txt:
                        yield html_txt
            except Exception:
                pass
            # sleep(1)

if __name__ == '__main__':
    jokeSpider = Jokespider()

    print(next(jokeSpider.crawl()))



