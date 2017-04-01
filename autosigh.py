#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep

import os

from logger import Logger
from tool import get_cookies
from websites.hkpic import HkpicAutosigh
from websites.soul_plus import SoulPlus
from websites.tieba import Tieba
from websites.youiv import Youiv
from websites.zodgame import Zodgame

my_username = os.getenv('my_username')
my_password = os.getenv('my_password')
# tieba_cookie_str = repr(os.getenv('tieba_cookie_str'))
# zod_cookie_str =  repr(os.getenv('zod_cookie_str'))
tieba_cookie_str = 'BAIDUID=0B492F710013D8A05CB5AAA1B55AE168:FG=1; TIEBA_USERTYPE=097ce01c0dc964bbd47f323a; bdshare_firstime=1490971582480; BIDUPSID=0B492F710013D8A05CB5AAA1B55AE168; PSTM=1491059842; BDUSS=XQ1RkRWR2QyZjE3VjN-NjlYV0FVOHRaSjNQSmdJc29BYUZtMG9UTWxPYVdVUWRaSVFBQUFBJCQAAAAAAAAAAAEAAACV5mQjU3lhb0ZveAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJbE31iWxN9YW; H_PS_PSSID=22163_1451_21110_17001_21928_22176_22158; STOKEN=f3b9001e4bf87d4dd758b4c9f367fd5b2fef3e7d6e7303474ca87183e2875530; TIEBAUID=a5de5c0a7c11d664b23b4cff; wise_device=0'
zod_cookie_str = 'TvTn_2132_saltkey=a2RjrjAy; TvTn_2132_lastvisit=1491055712; TvTn_2132_seccode=11144.d87699b675ca9ae422; TvTn_2132_ulastactivity=45dcEPl9bglefpcG0hTUxjIiLr67ygay%2FCbmmPU%2FOn04NML8BWoi; TvTn_2132_auth=2f1a%2BKdOj7T%2Fi06JS%2FlhvjI5yv4yOhkczI8OakiAC%2FMXHUpOYQ69t6F0rWR7SxWPl4cVksOQYKKbPzLbWpMejyh59Zk; TvTn_2132_lastcheckfeed=228826%7C1491059361; TvTn_2132_myrepeat_rr=R0; TvTn_2132_nofavfid=1; TvTn_2132_lip=45.77.23.58%2C1491062989; TvTn_2132_onlineusernum=570; TvTn_2132_sid=iWw4lz; TvTn_2132_sendmail=1; TvTn_2132_lastact=1491064148%09home.php%09spacecp'
if __name__ == '__main__':

    # print(tieba_cookie_str)
    # print(get_cookies(tieba_cookie_str))

    hkpic = HkpicAutosigh(my_username, my_password)
    soulplus = SoulPlus(my_username, my_password)
    youiv = Youiv(my_username, my_password)
    zodgame = Zodgame(get_cookies(zod_cookie_str))
    tieba = Tieba(get_cookies(tieba_cookie_str))

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
        print(count)
        # logger.info(str(count))
        sleep(1)
