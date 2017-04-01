#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep
from urllib.parse import urljoin

import re
import requests

from logger import Logger


class Youiv():
    def __init__(self, id, password):
        self.password = password
        self.id = id
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        self.website = 'http://youiv.tv'
        self.hash = ''
        self.logger = Logger().set_logon('youiv')

    def gethas(self):
        self.session.headers.update({'Referer': self.website})

        res = self.session.get(urljoin(self.website, 'member.php'), params={'mod': 'logging', 'action': 'login'},timeout=5)
        sleep(1)
        if res.status_code == 200:
            action = re.search(
                r'<form method="post".*?action=".*?loginhash=(.*?)">.*?<div class="c cl">.*?name="formhash" value="(.*?)"',
                res.text, re.S)
            if action:
                return action.group(1), action.group(2)

    def checklogin(self):
        res = self.session.get(self.website,timeout=5)
        sleep(1)
        if res.status_code == 200:
            return re.search(r'syaofox', res.text, re.S) is not None

    def login(self, loginhash, formhash):
        if not loginhash or not formhash:
            return False
        self.session.headers.update({'Referer': 'http://youiv.tv/member.php?mod=logging&action=login',
                                     'Host': 'youiv.tv',
                                     'Origin': self.website})
        res = self.session.post(urljoin(self.website, 'member.php'),
                                params={
                                    'mod': 'logging',
                                    'action': 'login',
                                    'loginsubmit': 'yes',
                                    'loginhash': formhash,
                                    'inajax': '1',
                                },
                                data={
                                    'formhash': loginhash,
                                    'referer': self.website,
                                    'username': self.id,
                                    'password': self.password,
                                    'questionid': '0',
                                    'answer': '',
                                },timeout=5
                                )
        sleep(1)
        if res.status_code == 200:
            result = re.search(r'欢迎您回来', res.text)
            return result is not None

    def sigh(self):
        url = 'http://youiv.tv/plugin.php?id=dsu_amupper:ppering&infloat=yes&handlekey=pper&inajax=1&ajaxtarget=fwin_content_pper'
        res = self.session.get(url,timeout=5)
        sleep(1)
        if res.status_code == 200:
            sigh_url = re.search(
                r'onclick="showWindow\(\'dsu_amupper\', \'(.*?)\'\);hideWindow\(\'pper\'\);return false;"><span>马上签到',
                res.text, re.S)
            if sigh_url:
                url = urljoin(self.website, sigh_url.group(1))
                res = self.session.get(url,timeout=5)
                sleep(1)
                if res.status_code == 200:
                    res = re.search(r'<div id="messagetext".*?<p>(.*)</p>', res.text)
                    if res:
                        return True
                    else:
                        self.logger.info('今日已经签到过了')
            else:
                self.logger.info('今日已经签到过了')



    def run(self):
        try:
            self.logger.info('开始 youiv.net')
            logined = self.checklogin()
            self.logger.info('登陆状态:{}'.format(logined))
            if not logined:
                loginhash, formhash = self.gethas()
                self.logger.info('开始登陆')
                logined = self.login(loginhash, formhash)
            if logined:
                self.logger.info('登陆状态:{},开始签到'.format(logined))
                self.sigh()
            self.logger.info('--------------------')
        except Exception as e:
            self.logger.info('异常:{},'.format(e))

if __name__ == '__main__':
    youiv = Youiv('syaofox', 'Xsbyczz060610')
    youiv.run()
