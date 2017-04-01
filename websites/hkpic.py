#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from time import sleep,time
from urllib.parse import urljoin

import re
import requests

from joke_spider import Jokespider
from logger import Logger


class HkpicAutosigh:
    def __init__(self, id, password):
        self.password = password
        self.id = id
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        self.website = 'http://hkbbcc.net/'
        self.hash = ''
        self.logger = Logger().set_logon('hkpic')
        self.jokeSpider = Jokespider()

    def check_logon(self):
        rs = self.session.get(self.website, timeout=5)
        sleep(1)
        if rs.status_code == 200:

            input = re.search(r'SyaoFox', rs.text, re.S)

            if input:
                # self.logger.info('未登陆{}'.format(self.website))
                # self.hash = self.get_hash()
                return True

            else:

                return False

    def logon(self):

        data = {
            'fastloginfield': 'username',
            'username': self.id,
            'password': self.password,
            'quickforward': 'yes',
            'handlekey': 'ls'

        }
        # self.logger.info('登陆{}'.format(self.website))

        rs = self.session.post(urljoin(self.website,
                                       '/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'),
                               data=data, timeout=5)
        result = re.search(r'登錄失敗', rs.text)
        sleep(1)
        return result is None

    def sigh(self):
        rs = self.session.get(urljoin(self.website, '/plugin.php?id=dsu_paulsign:sign'), timeout=5)
        sleep(1)
        if rs.status_code == 200:
            today_sigh = re.search(r'您今天已經簽到過了或者簽到時間還未開始', rs.text)
            if today_sigh:
                self.logger.info('今日已签到')
                days = re.search(r'<p><font color="#FF0000"><b>SyaoFox</b></font> , 您累計已簽到: <b>(\d+)</b> 天</p>',
                                 rs.text)
                if days:
                    self.logger.info('累计签到:{}天'.format(days.group(1)))
            else:
                self.logger.info('未签到，开始签到')
                if self.hash == '':
                    self.hash = self.get_hash()
                if self.hash != '':
                    url = urljoin(self.website, '/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1')
                    data = ({
                        'formhash': self.hash,
                        'qdxq': 'nu'
                    })
                    sigh_rs = self.session.post(url, data=data, timeout=5)
                    sleep(1)
                    if sigh_rs.status_code == 200:
                        self.logger.info('签到成功')
                else:
                    self.logger.info('has为空')

    def run(self):
        try:
            self.logger.info('开始 hkbbcc.net')
            logined = self.check_logon()
            self.logger.info('登陆状态:{}'.format(logined))
            if not logined:
                self.logger.info('开始登陆')
                logined = self.logon()
            if logined:
                self.logger.info('登陆状态:{},开始签到'.format(logined))
                self.sigh()
            self.logger.info('--------------------')
        except Exception as e:
            self.logger.info('异常:{},'.format(e))

    def get_post_info(self, url):
        rs = self.session.get(url, timeout=5)
        sleep(1)
        if rs:
            try:
                re_r = re.search(r'name="formhash" value="(.*?)" /', rs.text)

                formhash = re_r.group(1)
                re_r = re.search(r'var fid = parseInt\(\'(\d+?)\'\), tid = parseInt\(\'(\d+?)\'\);</script>', rs.text)

                fid = re_r.group(1)
                tid = re_r.group(2)

                return formhash, fid, tid
            except Exception:
                pass

    def post_reply(self,url):
        page = re.search('thread-\d+-(\d)+-\d+.html',url).group(1)
        try:
            formhash, fid, tid = self.get_post_info(url)
            post_url = 'http://hkbbcc.net/forum.php'
            if page and formhash and post_url:
                params = {
                    'mod': 'post',
                    'action': 'reply',
                    'fid': fid,
                    'tid': tid,
                    'extra': 'page={}'.format(page),
                    'replysubmit': 'yes',
                    'infloat': 'yes',
                    'handlekey': 'fastpost',
                    'inajax': '1',
                }

                message = next(self.jokeSpider.crawl())
                if message:
                    data = {
                        'message':message,
                        'posttime': '{}'.format(time()),
                        'formhash': formhash,
                        'usesig': '1',
                        'subject': '  ',
                    }

                    res = self.session.post(post_url,data=data,params= params)
                    if res.status_code == 200:
                        self.logger.info('发表回复:{},'.format(message))
        except Exception as e:
            self.logger.info('异常:{},'.format(e))



    def get_hash(self):
        rs = self.session.get(self.website, timeout=5)
        sleep(1)
        if rs.status_code == 200:
            has = re.search(r'formhash=(.*?)">退出</a>', rs.text)
            if has:
                return has.group(1)
            else:
                return ''


if __name__ == '__main__':
    hkpic = HkpicAutosigh('syaofox', 'Xsbyczz060610')
    hkpic.run()
    # sleep(5)
    # while True:
    #     hkpic.post_reply('http://hkbbcc.net/thread-4414984-1-1.html')
    #     times = random.randint(60,120)
    #     sleep(times)

    # spider = Jokespider()
    #
    # for x in range(1000):
    #     print(next(spider.crawl()))
    #     sleep(1)
