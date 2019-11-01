# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 16:11
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : api_test_service.py
# @Software: PyCharm
from apiManager.test_case_api import *
import pytest
class ApiTestService(object):
    def __init__(self,case_dirs=[],test_files=[]):
        self.case_dirs=case_dirs
        self.test_files=test_files

    def execute_api_test(self):
        return test_impl(create_test_cases(self.case_dirs, self.test_files))

    def execute_pytest(self,api_test_results):
        test_cases_files = create_test_case_files(case_dirs=self.case_dirs,
                                                  test_files=self.test_files,
                                                  api_test_results=api_test_results)
        # print(test_cases_files)
        if self.test_files:
            py_files = test_cases_files
        else:
            py_files = self.case_dirs
        # print(py_files)
        # pytest.main([
        #     '-v',
        #     test_cases_files,
        #     '--alluredir',
        #     'report',
        #     # '--tx',
        #     # env,
        #     '--capture',
        #     'no',
        #     '--disable-warnings',
        # ])
        pytest.main(['-v', *py_files, '--ignore', 'test_bootstrap.py', '--html', '../res/report/report.html',
                     '--disable-warnings'])
        #
        del_test_case_file(test_cases_files)

