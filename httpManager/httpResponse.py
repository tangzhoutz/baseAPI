# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 9:15
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : httpResponse.py
# @Software: PyCharm

#TODO 返回的数据处理需要再优化
async def response_handler(response):
    res={}
    body=await response.text(encoding='utf-8')
    # print(response.url)
    res['code']=response.status
    res['headers']=dict(response.headers)
    res['body']=body
    print(response.request_info)
    return res
    # return await type(response.text(encoding='utf-8'))