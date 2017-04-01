#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def get_cookies(cookie_str):
    if not cookie_str:return
    lst = re.findall('(.*?)=(.*?);',cookie_str)
    result = {}
    for each in lst:
        result[each[0].strip()] = each[1].strip()

    return result



if __name__ == '__main__':
    cookie_str = 'BAIDUID=0B492F710013D8A05CB5AAA1B55AE168:FG=1; TIEBA_USERTYPE=097ce01c0dc964bbd47f323a; bdshare_firstime=1490971582480; BIDUPSID=0B492F710013D8A05CB5AAA1B55AE168; PSTM=1491059842; BDUSS=XQ1RkRWR2QyZjE3VjN-NjlYV0FVOHRaSjNQSmdJc29BYUZtMG9UTWxPYVdVUWRaSVFBQUFBJCQAAAAAAAAAAAEAAACV5mQjU3lhb0ZveAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJbE31iWxN9YW; H_PS_PSSID=22163_1451_21110_17001_21928_22176_22158; STOKEN=f3b9001e4bf87d4dd758b4c9f367fd5b2fef3e7d6e7303474ca87183e2875530; TIEBAUID=a5de5c0a7c11d664b23b4cff; wise_device=0'
    print(get_cookies(cookie_str))