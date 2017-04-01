#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

import requests

from logger import Logger


class Zodgame():
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        self.website = 'http://www.zodgame.us'
        self.set_cookie()
        self.logger = Logger().set_logon('youiv')

    def set_cookie(self):
        cookies = {
            'TvTn_2132_saltkey': 'mcq9C0mI',
            'TvTn_2132_lastvisit': '1491052282',
            'TvTn_2132_sendmail': '1',
            'TvTn_2132_seccode': '10508.d2d3a2ed71d9782171',
            'TvTn_2132_ulastactivity': 'af4dV4geTp1I3XxdmoFvyIuBL26BqDzqB7OD8JcvGOhdkcIyD%2F%2FA',
            'TvTn_2132_auth': 'f423nh0gCJTQ84VC3PM00%2BrccG8THN%2Bmedbg157huuIhr%2BhRm7jIoOZxt5WSg3dxA%2BeFhbkgP9KImvYSR%2FNPx7GNHN4',
            'TvTn_2132_lastcheckfeed': '228826%7C1491057237',
            'TvTn_2132_lip': '45.77.23.58%2C1491055882',
            'TvTn_2132_myrepeat_rr': 'R0',
            'TvTn_2132_nofavfid': '1',
            'TvTn_2132_onlineusernum': '569',
            'TvTn_2132_sid': 'djZ87r',
            'TvTn_2132_checkpm': '1',
            'TvTn_2132_lastact': '1491057426%09misc.php%09patch',
        }
        for k,v in cookies.items():
            self.session.cookies.set(k,v)

    def checklogin(self):
        url = 'https://www.zodgame.us'
        res = self.session.get(url,timeout=5)
        if res.status_code == 200:

            return re.search(r'syaofox',res.text,re.S) is not None

    def sigh(self):
        url = 'https://www.zodgame.us/plugin.php?id=dsu_paulsign:sign'
        res = self.session.get(url, timeout=5)
        if res.status_code == 200:
            singh_info = re.search(r'<h1 class="mt">(您今天已经签到过了或者签到时间还未开始)</h1>.*?'
                                   r' , (您累计已签到:) <b>(\d+?)</b> 天</p>.*?'
                                   r'<p>(您上次签到时间:)<font color="#ff00cc">(.+?)</font> </p>.*?',
                                   res.text,re.S)
            if singh_info:
                self.logger.info('{} {}{} {}{}'.format(singh_info.group(1),singh_info.group(2),singh_info.group(3),singh_info.group(4),singh_info.group(5)))

    def run(self):
        try:
            self.logger.info('开始 zodgame.us')
            logined = self.checklogin()
            self.logger.info('登陆状态:{}'.format(logined))
            if logined:
                self.logger.info('登陆状态:{},开始签到'.format(logined))
                self.sigh()
            else:
                self.logger.info('登陆状态:{}'.format(logined))
            self.logger.info('--------------------')
        except Exception as e:
            self.logger.info('异常:{},'.format(e))

if __name__ == '__main__':
    zodgame = Zodgame()
    zodgame.run()