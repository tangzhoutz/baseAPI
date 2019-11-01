# -*- coding: utf-8 -*-
# @Time    : 2019/4/26 15:08
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : case_meta_class.py
# @Software: PyCharm
import builtins,types,pytest,allure
from modelManager.template import TEST_CASE_FUNCTION_EXPRESS
from apiManager.validator import validator


class CaseMetaClass(type):
    """
    根据接口调用的结果自动生成测试用例
    """

    def __new__(cls, name, bases, attrs):
        test_cases_data = attrs.pop('test_cases_data')
        for each in test_cases_data:
            api = each.pop('api')
            function_name = 'test' + api.replace('/', '_')
            test_data = [tuple(x.values()) for x in each.get('responses')]
            # print('aaaa'+str(test_data))
            function = gen_function(TEST_CASE_FUNCTION_EXPRESS.format(function_name),
                                    namespace={'validator': validator, 'allure': allure})
            # 集成allure
            story_function = allure.story('{}'.format(api))(function)
            attrs[function_name] = pytest.mark.parametrize('response,validata', test_data)(story_function)

        return super().__new__(cls, name, bases, attrs)

def gen_function(function_express, namespace={}):
    """
    动态生成函数对象, 函数作用域默认设置为builtins.__dict__，并合并namespace的变量
    :param function_express: 函数表达式，示例 'def foobar(): return "foobar"'
    :return:
    """
    builtins.__dict__.update(namespace)
    module_code = compile(function_express, '', 'exec')
    function_code = [c for c in module_code.co_consts if isinstance(c, types.CodeType)][0]
    return types.FunctionType(function_code, builtins.__dict__)

