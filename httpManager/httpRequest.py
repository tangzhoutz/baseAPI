from aiohttp import ClientSession
import os
from dataManager.yamlManager import yaml_load
from utils.bxmTool import *
from configs import bxmat
from httpManager.httpResponse import response_handler
from aiohttp.formdata import FormData
import aiofiles
import asyncio
from httpManager.authManager import get_auth_cookies

async def http(session,domain, *args, **kwargs):
    """
    TODO 补充一下参数和返回值格式说明
    http请求处理器
    :param session: ClientSession对象
    :param domain: 服务地址
    :param args:
    :param kwargs:
    :return:
    """
    method, api = args
    arguments = kwargs.get('data') or kwargs.get('params') or kwargs.get('json') or {}

    # kwargs中加入token
    # TODO 实现getheader 通用方法
    # 已经实现了
    # kwargs.setdefault('headers', {}).update({'token': bxmat.token})
    contentType=kwargs.setdefault('headers', {}).setdefault('Content-Type','')
    #TODO 补充文件上传的处理
    if contentType.startswith('multipart/'):
        formData = FormData()
        data=kwargs.get('data') or {}
        if isinstance(data,dict):
            for k,v in data.items():
                if os.path.isfile(v):
                    formData.add_field(k,
                                        await aiofiles.open(v, 'rb'),
                                        filename=os.path.basename(v))
                                        # content_type=contentType)
                else :
                    formData.add_field(k,str(v))
                    # print('111')
                pass
        kwargs['data']=formData
    # 拼接服务地址和api
    url = ''.join([domain, api])
    # print(kwargs['data'].__dict__)
    # print()
    # async with ClientSession() as session:
    #     async with session.request(method, url, **kwargs) as response:
    #         res = await response_handler(response)
    #         return {
    #             'response': res,
    #             'url': url,
    #             'arguments': arguments
    #         }
    # async with ClientSession() as session:
    async with session.request(method, url, **kwargs) as response:
        res = await response_handler(response)
        return {
            'response': res,
            'url': url,
            'arguments': arguments
        }

async def one_http(case_dir='', case_name='', semaphore=None, session=None):
    """
    一个yaml文件测试用例执行的全过程(一个yaml文件)，包括读取.yml测试用例，执行http请求，返回请求结果
    :param case_dir:
    :param case_name:
    :param semaphore:控制并发量
    :param session: ClientSession对象
    :return:
    """
    # 控制并发量
    async with semaphore:
        # TODO 暂时使用此方法获取项目名
        # project_name = case_name.split(os.sep)[-3]
        project_name=bxmat.test_project_name
        domain = bxmat.url.get(project_name)
        test_case = await yaml_load(dir=case_dir, file=case_name)
        # result = BXMDict({
        #     'case_dir': os.path.dirname(case_name),
        #     'api': test_cases.args[1].replace('/', '_'),
        # })
        test_case_result = BXMDict({
            'case_dir': os.path.dirname(case_name),
            'api': test_case.args[1],
        })

        for index, each_data in enumerate(test_case.kwargs):
            step_name = each_data.pop('caseName')
            each_data['headers']=test_case.headers
            r = await http(session,domain, *test_case.args, **each_data)
            r.update({'case_name': step_name})
            test_case_result.setdefault('responses', BXMList()).append({
                'response': r,
                'validator': test_case.validator[index]
            })
        return test_case_result


async def all_http(semaphore, test_cases):
    '''
    一份所有测试用例执行的全过程
    :param semaphore: 控制并发量
    :param test_cases:
    :return:
    '''

    async with ClientSession(cookies=get_auth_cookies(bxmat.test_project_name)) as session:#给所有的请求，创建同一个session
        tasks = [asyncio.ensure_future(one_http(case_name=test_case, semaphore=semaphore, session=session)) for test_case in test_cases]
        # await asyncio.wait(tasks)
        return await asyncio.gather(*tasks)
        # # TODO 后续实现BXMDict
        # test_cases_results = BXMDict()
        # # res=[]
        # for task in tasks:
        #     data = task.result()
        #     # TODO 后续实现BXMList
        #     test_cases_results.setdefault(data.pop('case_dir'), BXMList()).append(data)
        # return test_cases_results
