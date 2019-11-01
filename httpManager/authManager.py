# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 11:07
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : authManager.py
# @Software: PyCharm
import requests
import time
from configs import bxmat
import re


def get_auth_cookies(project_name):
    domain = bxmat.url.get(project_name)
    if project_name=='project2' and domain:
        # cookies=None
        with requests.session() as s:
            response1=s.request('get', domain)
            token_re=r'name="__RequestVerificationToken" type="hidden" value="(.+?)"'
            pattern_token=re.compile(token_re)
            result=pattern_token.search(response1.text)
            data={'UserName':'guanliyuan','Password':'00000000'}
            data['__RequestVerificationToken']=result.groups(0)
            # print(response1.cookies)
            with s.request('post',''.join([domain, '/Account/Login1?ReturnUrl=%2F']),data=data) as response:
                pass
            # print(s.cookies)
            # cookies=dict(s.cookies)
            return s.cookies

if __name__=='__main__':

    start=time.time()
    b=get_auth_cookies('project2')
    end=time.time()
    print(end-start)
    print(b)
