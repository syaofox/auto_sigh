#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep

import os

from logger import Logger
from websites.hkpic import HkpicAutosigh
from websites.soul_plus import SoulPlus
from websites.tieba import Tieba
from websites.youiv import Youiv
from websites.zodgame import Zodgame

my_username = os.getenv('my_username')
my_password = os.getenv('my_password')

if __name__ == '__main__':

    hkpic = HkpicAutosigh(my_username, my_password)
    soulplus = SoulPlus(my_username, my_password)
    youiv = Youiv(my_username, my_password)
    zodgame = Zodgame()
    tieba = Tieba()

    count = 0
    logger = Logger().set_logon('runner')
    while True:
        if count >= 1800:
            count = 0
        if count == 0:
            hkpic.run()
            soulplus.run()
            youiv.run()
            zodgame.run()
            tieba.run()

        count += 1
        # logger.info(str(count))
        sleep(1)
