# -*- coding: utf-8 -*-
# @Project : PyCharm
# @Time    : 2019/3/15 9:21
# @Author  : tangzhou
# @File    : test_case_api.py
# @Software: PyCharm Community Edition
# @Contact : 505200187@qq.com
# @desc    :
import os
import re
import asyncio
from utils.bxmTool import *
from httpManager.httpRequest import all_http
from configs import bxmat
from modelManager.template import TEST_CASE_CONTENT


# 用例目录路径模式 projectspce/testcases/{projectname}/{modelname}/XXXX.yaml
def create_test_cases(case_dirs=[], test_files=[]):
    cases=BXMList()
    if test_files:
        for test_file in test_files:
            if is_yml_file(test_file):
                cases.append(test_file)
    else:
        for case_dir in case_dirs:
            if os.path.isdir(case_dir):
                for root, dirs, files in os.walk(case_dir):
                    if re.match(r'\w+', root) and (not ('.' in root or '__' in root)):
                        if files and has_yml_file(files):
                            cases.extend([os.path.join(root, file) for file in files if file.endswith('.yml')])
    return cases

def test_impl(test_cases):
    """
    事件循环主函数，负责所有接口请求的执行,接口测试
    :param test_cases:
    :return:
    """
    loop = asyncio.get_event_loop()
    # TODO 需要实现bxmat 方法，暂时写死。
    semaphore = asyncio.Semaphore(bxmat.semaphore)
    # 需要处理的任务
    # tasks = [asyncio.ensure_future(one(case_name=test_case, semaphore=semaphore)) for test_case in test_cases]
    # tasks = [asyncio.ensure_future(main(10,test_cases))]
    # tasks=all(semaphore, test_cases)
    # 将协程注册到事件循环，并启动事件循环
    try:
        # loop.run_until_complete(asyncio.gather(*tasks))
        datas=loop.run_until_complete(all_http(semaphore, test_cases))
        # loop.run_until_complete(asyncio.wait(tasks))
    finally:
        loop.close()
    # TODO 后续实现BXMDict
    test_cases_results = BXMDict()
    # for task in tasks:
    for data in datas:
        # data = task.result()
        # TODO 后续实现BXMList
        test_cases_results.setdefault(data.pop('case_dir'), BXMList()).append(data)
    return test_cases_results
    # return tasks[0].result()


def create_test_case_files(case_dirs=[], test_files=[], api_test_results=None):

    test_cases_files = BXMList()
    if test_files:
        for test_file in test_files:
            if is_yml_file(test_file):
                root=os.path.dirname(test_file)
                case_name = get_case_name(test_file)
                # project_name = get_project_name(test_file)
                project_name = bxmat.test_project_name
                test_case_file = get_test_case_file(test_file,case_name)
                if test_case_file not in test_cases_files:
                    write_test_case_file(test_case_file, case_name, project_name, api_test_results.get(root))
                    test_cases_files.append(test_case_file)

    else:
        for case_dir in case_dirs:
            if os.path.isdir(case_dir):
                for root, dirs, files in os.walk(case_dir):
                    if re.match(r'\w+', root) and (not ('.' in root or '__' in root)):
                        if files and has_yml_file(files):
                            case_name = get_case_name(root)
                            # project_name = get_project_name(root)
                            project_name = bxmat.test_project_name
                            test_case_file = get_test_case_file(root,case_name)
                            write_test_case_file(test_case_file, case_name, project_name, api_test_results.get(root))
                            test_cases_files.append(test_case_file)


    return test_cases_files



def write_test_case_file(file_name, case_name, project_name, case_data):


    # print(TEST_CASE_CONTENT.format(case_name, project_name, case_name.title(), case_data))
    print(case_data)
    with open(file_name, 'w', encoding='utf-8') as fw:
        fw.write(TEST_CASE_CONTENT.format(case_name, project_name, case_name.title(), case_data))
    pass
def del_test_case_file(files):
    for file in files:
        os.remove(file)
def has_yml_file(files):
    for file in files:
        if file.endswith('.yml'):
            return True
    return False
def is_yml_file(file):
    if not (file and os.path.isfile(file) and file.endswith('.yml')):
        return False
    return True
def get_case_name(test_file_or_dir):
    if not test_file_or_dir:
        return False
    if os.path.isfile(test_file_or_dir):
        return os.path.basename(os.path.dirname(test_file_or_dir))
    if os.path.isdir(test_file_or_dir):
        return os.path.basename(test_file_or_dir)

def get_project_name(test_file_or_dir):
    if not test_file_or_dir:
        return False
    if os.path.isfile(test_file_or_dir):
        return os.path.basename(os.path.dirname(os.path.dirname(test_file_or_dir)))
    if os.path.isdir(test_file_or_dir):
        return os.path.basename(os.path.dirname(test_file_or_dir))

def get_test_case_file(test_file_or_dir,case_name):
    if not test_file_or_dir:
        return False
    if os.path.isfile(test_file_or_dir):
        return os.path.join(os.path.dirname(test_file_or_dir), 'test_{}.py'.format(case_name))
    if os.path.isdir(test_file_or_dir):
        return os.path.join(test_file_or_dir, 'test_{}.py'.format(case_name))
if __name__ == "__main__":
    # testdata=BXMDict()

    # data = test_impl(create_test_data(r'D:\pyworkspace\python1\testcases'))
    # print(data)
    # test_cases_files = create_test_case_files(case_dir=r'D:\pyworkspace\python1\testcases', test_result=data)
    # print(test_cases_files)
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--tf', nargs='*', action="store", default=[], help="my option: 请输入测试用例文件 和 --")
    parser.add_argument('--te', nargs='*', action="store", default=[], help="my option: 请输入测试用例文件 和 --")
    parser.add_argument("--rootdir", nargs='*',action="store", default=[r'D:\pyworkspace\baseAPI\testcases'], help="请输入测试用例目录，输入--tf后此参数无效")
    print(parser.parse_args(r'--rootdir D:\pyworkspace\baseAPI\testcases'.split()))

