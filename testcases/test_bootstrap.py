# -*- coding: utf-8 -*-
# @Time    : 2019/4/26 11:50
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : test_bootstrap.py
# @Software: PyCharm

# test_bootstrap.py
import pytest
from configs.bxmat import *

@pytest.mark.usefixtures('test_cases')
class TestStarter(object):

    def test_start(self):
        pytest.skip('此为测试启动方法, 不执行')

if __name__ == "__main__":
    pytest.main(['-s', '-q','test_bootstrap.py','--testdir',*test_dirs,'--tf',*test_files])