# -*- coding: utf-8 -*-
# @Project : PyCharm
# @Time    : 2019/3/15 9:17
# @Author  : tangzhou
# @File    : yamlManager.py
# @Software: PyCharm Community Edition
# @Contact : 505200187@qq.com
# @desc    :
import os
import yaml
import re
import aiofiles
from utils.bxmTool import *
from configs import bxmat


async def yaml_load(dir='', file=''):
    """
    异步读取yaml文件，并转义其中的特殊值
    :param file:
    :return:
    """
    if dir:
        file = os.path.join(dir, file)
    async with aiofiles.open(file, 'r', encoding='utf-8', errors='ignore') as f:
        data = await f.read()

    data = yaml.safe_load(data)

    # 匹配函数调用形式的语法
    # ${function(xxxx)} 调用函数
    pattern_function = re.compile(r'^\${([A-Za-z_]+\w*\(.*\))}$')
    # ${varname} 常量 或者表达式等对象。
    pattern_function2 = re.compile(r'^\${(.*)}$')
    # 匹配取默认值的语法
    # $(a:b)，匹配默认值
    pattern_function3 = re.compile(r'^\$\((.*)\)$')

    def my_iter(data):
        """
        递归测试用例，根据不同数据类型做相应处理，将模板语法转化为正常值
        :param data:
        :return:
        """
        if isinstance(data, (list, tuple)):
            for index, _data in enumerate(data):
                data[index] = my_iter(_data) or _data
        elif isinstance(data, dict):
            for k, v in data.items():
                data[k] = my_iter(v) or v
        elif isinstance(data, (str, bytes)):
            m = pattern_function.match(data)
            if not m:
                m = pattern_function2.match(data)
            if m:
                return eval(m.group(1))
            if not m:
                m = pattern_function3.match(data)
            if m:
                K, k = m.group(1).split(':')
                return bxmat.default_values.get(K).get(k)

            return data


    def filter_data(data):
        '''
        处理get参数中的 None bool等数据类型（request get参数 只能接收int和string）
        :param data:
        :return:
        '''
        def filter_params(data):
            '''
            递归测试用例中params参数，处理get参数中的 None bool等数据类型（request get参数 只能接收int和string）
            :param data:
            :return:
            '''

            if isinstance(data, (list, tuple)):
                for index, _data in enumerate(data):
                    data[index] = filter_params(_data) or _data
            elif isinstance(data, dict):
                for k, v in data.items():
                    data[k] = filter_params(v) or v
            elif isinstance(data, (bool)):
                if data:
                    return 'True'
                return 'False'
            elif data == None:
                return 'null'
        if data.get('kwargs') and isinstance(data.get('kwargs'), (list, tuple)):
            kwargs=data.get('kwargs')
            for index,kwarg in enumerate(kwargs):
                if isinstance(kwarg, dict) and kwarg.get('params'):
                    filter_params(data.get('kwargs')[index].get('params'))


    my_iter(data)
    filter_data(data)
    # TODO 确认返回值格式BXMDict 实现
    return BXMDict(data)
if __name__ == "__main__":
    import asyncio
    import requests

    import json
    a=json.loads('{"a":"b"}')
    print(type(a))
    print(a)
    task1 = asyncio.ensure_future(yaml_load('.','../httpimpl/test.yml'))
    loop = asyncio.get_event_loop()
    test_case = loop.run_until_complete(task1)
    loop.close()
    print(test_case)
    for index, each_data in enumerate(test_case.kwargs):
        step_name = each_data.pop('caseName')
        print(index)
        print(test_case.validator[index])

