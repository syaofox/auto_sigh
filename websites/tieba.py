#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import re
import requests

from logger import Logger


# tieba_cookie_str = 'BAIDUID=0B492F710013D8A05CB5AAA1B55AE168:FG=1; TIEBA_USERTYPE=097ce01c0dc964bbd47f323a; bdshare_firstime=1490971582480; BIDUPSID=0B492F710013D8A05CB5AAA1B55AE168; PSTM=1491059842; BDUSS=XQ1RkRWR2QyZjE3VjN-NjlYV0FVOHRaSjNQSmdJc29BYUZtMG9UTWxPYVdVUWRaSVFBQUFBJCQAAAAAAAAAAAEAAACV5mQjU3lhb0ZveAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJbE31iWxN9YW; H_PS_PSSID=22163_1451_21110_17001_21928_22176_22158; STOKEN=f3b9001e4bf87d4dd758b4c9f367fd5b2fef3e7d6e7303474ca87183e2875530; TIEBAUID=a5de5c0a7c11d664b23b4cff; wise_device=0'


class Tieba():
    def __init__(self,cookies=None):
        self.cookies = cookies
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        self.website = 'http://tieba.baidu.com'
        self.set_cookie()
        self.logger = Logger().set_logon('youiv')


    def set_cookie(self):

        #     {
        #     'BAIDUID=0B492F710013D8A05CB5AAA1B55AE168:FG': '1',
        #     'TIEBA_USERTYPE': '097ce01c0dc964bbd47f323a',
        #     'wise_device': '0',
        #     'bdshare_firstime': '1490971582480',
        #     'BIDUPSID': '0B492F710013D8A05CB5AAA1B55AE168',
        #     'PSTM': '1491059842',
        #     'BDUSS': 'XQ1RkRWR2QyZjE3VjN-NjlYV0FVOHRaSjNQSmdJc29BYUZtMG9UTWxPYVdVUWRaSVFBQUFBJCQAAAAAAAAAAAEAAACV5mQjU3lhb0ZveAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJbE31iWxN9YW',
        #     'H_PS_PSSID': '22163_1451_21110_17001_21928_22176_22158',
        #     'STOKEN': 'f3b9001e4bf87d4dd758b4c9f367fd5b2fef3e7d6e7303474ca87183e2875530',
        #     'TIEBAUID': 'a5de5c0a7c11d664b23b4cff',
        # }
        for k, v in self.cookies.items():
            self.session.cookies.set(k, v)

    def checklogin(self):
        url = 'https://tieba.baidu.com'
        res = self.session.get(url, timeout=5)
        if res.status_code == 200:
            if re.search(r'SyaoFox', res.text, re.S) is not None:
                re_ = re.search(r'<script>PageData\.tbs = "(.*?)"', res.text)
                if re_:
                    return re_.group(1)

    # def get_tbs(self):
    #     url = 'https://tieba.baidu.com'
    #     res = self.session.get(url, timeout=5)
    #     if res.status_code == 200:
    #         re.search(r'<script>PageData\.tbs = "(.*?)"',r)

    def sigh(self, tbs):
        url = 'https://tieba.baidu.com/tbmall/onekeySignin1'
        data = {
            'ie': 'utf-8',
            'tbs': tbs
        }

        res = self.session.post(url, data=data, timeout=5)

        if res.status_code == 200:
            result = json.loads(res.text)
            if result.get('error') == ' success':
                return True
            else:
                return False

    def run(self):
        try:
            self.logger.info('开始 tieba.com')
            tbs = self.checklogin()
            self.logger.info('登陆状态:{}'.format(tbs))
            if tbs:
                self.logger.info('登陆状态:{},开始签到'.format(tbs))
                if self.sigh(tbs):
                    self.logger.info('签到成功')
                else:
                    self.logger.info('已签到')
            else:
                self.logger.info('登陆状态:{}'.format(tbs))
            self.logger.info('--------------------')
        except Exception as e:
            self.logger.info('异常:{},'.format(e))


if __name__ == '__main__':
    tieba = Tieba()
    tieba.run()
