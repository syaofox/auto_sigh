#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep, time

import re
import requests

from logger import Logger


class SoulPlus:
    def __init__(self, id, password):
        self.password = password
        self.id = id
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        self.websit = 'http://bbs.soul-plus.net/index.php'
        self.hash = ''
        self.logger = Logger().set_logon('soul-plus')

    def check_login(self):
        rs = self.session.get(self.websit,timeout=5)
        sleep(1)
        if rs.status_code == 200:
            return re.search(r'<input.*?class="input gray".*?value="登 录".*?>', rs.text, re.S) is None

    def login(self):
        data = {
            'jumpurl:http': '//bbs.soul-plus.net/index.php?',
            'step': '2',
            'cktime': time(),
            'lgt': '0',
            'pwuser': self.id,
            'pwpwd': self.password,

        }

        rs = self.session.post('http://bbs.soul-plus.net/login.php', data=data,timeout=5)
        sleep(1)
        if rs.status_code == 200:
            result = re.search(r'您已经顺利登录', rs.text)
            return result is not None

    def sigh(self):

        rs = self.session.get('http://bbs.soul-plus.net/plugin.php?H_name-tasks.html',timeout=5)
        sleep(1)
        if rs.status_code == 200:
            week = re.search(r'奖励 : SP币 7 G.*?上次领取未超过 (\d+?) 小时', rs.text, re.S)
            if week:
                self.logger.info('周任务还需{}小时'.format(week.group(1)))
            day = re.search(r'奖励 : SP币 2 G.*?上次领取未超过 (\d+?) 小时', rs.text, re.S)
            if day:
                self.logger.info('日常任务还需{}小时'.format(day.group(1)))

        url = 'http://bbs.soul-plus.net/plugin.php?H_name=tasks&action=ajax&actions=job&cid={}'

        dayid = re.search(r'奖励 : SP币 2 G.*?onclick="startjob\(\'(\d+?)\'\);".*?title="按这申请此任务"', rs.text, re.S)
        if dayid:
            rs = self.session.get(url.format(dayid.group(1)),timeout=5)
            sleep(1)

        weekid = re.search(r'奖励 : SP币 7 G.*?onclick="startjob\(\'(\d+?)\'\);".*?title="按这申请此任务"', rs.text, re.S)
        if weekid:
            rs = self.session.get(url.format(weekid.group(1)),timeout=5)
            sleep(1)

        finish_url = 'http://bbs.soul-plus.net/plugin.php?H_name=tasks&action=ajax&actions=job2&cid={}'
        rs = self.session.get('http://bbs.soul-plus.net/plugin.php?H_name-tasks-actions-newtasks.html.html',timeout=5)
        sleep(1)
        if rs.status_code == 200:
            dayid = re.search(r'奖励 : SP币 2 G.*?onclick="startjob\(\'(\d+?)\'\);".*?title="领取此奖励"', rs.text, re.S)
            if dayid:
                rs = self.session.get(finish_url.format(dayid.group(1)),timeout=5)
                sleep(1)
                if rs.status_code == 200:
                    if re.search('已经完成', rs.text):
                        self.logger.info(
                            '领取日常奖励成功')  # <?xml version="1.0" encoding="utf-8"?><ajax><![CDATA[success	你[日常]已经完成!	15]]></ajax>

            weekid = re.search(r'奖励 : SP币 7 G.*?onclick="startjob\(\'(\d+?)\'\);".*?title="领取此奖励"', rs.text, re.S)
            if weekid:
                rs = self.session.get(finish_url.format(weekid.group(1)),timeout=5)
                sleep(1)
                if rs.status_code == 200:
                    if re.search('已经完成', rs.text):
                        self.logger.info('领取周常奖励成功')
                    sleep(1)

    def run(self):
        try:
            self.logger.info('开始bbs.soul-plus.net')
            logined = self.check_login()
            self.logger.info('登陆状态:{}'.format(logined))

            if not logined:
                self.logger.info('开始登陆')
                logined = self.login()
            if logined:
                self.logger.info('登陆状态:{},开始签到'.format(logined))
                self.sigh()
            self.logger.info('--------------------')
        except Exception as e:
            self.logger.info('异常:{},'.format(e))


if __name__ == '__main__':
    soulPlus = SoulPlus('syaofox', 'Xsbyczz060610')
    soulPlus.run()
