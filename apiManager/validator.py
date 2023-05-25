# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 16:48
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : validator.py
# @Software: PyCharm
# TODO 后续需要完善公共的校验方法
def validator(response,validata):
    # code=validata['code']['successed']
    from pprint import pprint
    pprint(response)
    pprint(validata)
    if isinstance(validata,dict) and validata.get('code'):
        real_code=response.get('response').get('code')
        expect_code=validata.get('code')

        if expect_code.get('successed'):
            assert str(expect_code.get('successed'))==str(real_code)
        elif expect_code.get('unsuccessed'):
            assert str(expect_code.get('unsuccessed')) != str(real_code)
    elif isinstance(validata,dict) and validata.get('data'):
        pass
        # if validata
    # assert False