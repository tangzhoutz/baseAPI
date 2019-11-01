# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 14:27
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : conftest.py
# @Software: PyCharm
import pytest
from services.api_test_service import ApiTestService
from configs.bxmat import test_dirs
from configs.bxmat import test_files
def pytest_addoption(parser):
    parser.addoption(
        "--testdir", nargs='*',action="store", default=test_dirs, help="请输入测试用例目录，输入--tf后此参数无效"
    )
    parser.addoption(
        "--te", action="store", default="", help="my option: 请输入分布式执行参数，默认为空，参考--tx"
    )
    parser.addoption(
        "--tf", nargs='*', action="store",default=test_files, help="请输入测试用例文件yml，输入后--rootdir参数无效"
    )

@pytest.fixture(scope='session')
def test_cases(request):
    """
    测试用例生成处理
    :param request:
    :return:
    """
    case_dirs = request.config.getoption("--testdir")
    # print(case_dirs)
    test_files = request.config.getoption("--tf")
    # TODO 后续补充分布式部署使用
    # env = request.configs.getoption("--te")
    ats=ApiTestService(case_dirs,test_files)
    api_test_results=ats.execute_api_test()
    ats.execute_pytest(api_test_results)
