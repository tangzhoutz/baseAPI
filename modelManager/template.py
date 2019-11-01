# -*- coding: utf-8 -*-
# @Time    : 2019/4/26 15:14
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : template.py
# @Software: PyCharm
TEST_CASES_DATA='test_cases_data'
IMPORT_META_CLASS='from apiManager.case_meta_class import CaseMetaClass'
META_CLASS_NAME='CaseMetaClass'

TEST_CASE_CONTENT = """
import allure

from apiManager.case_meta_class import CaseMetaClass


@allure.feature('{}接口测试({}项目)')
class Test{}API(object, metaclass=CaseMetaClass):

    test_cases_data = {}
"""
RESPONSE_NAME='response'
VALIDATA_NAME='validata'
TEST_CASE_FUNCTION_EXPRESS = """
def {}(self, response, validata):
    with allure.step(response.pop('case_name')):
        validator(response,validata)"""

