# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 17:28
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : testdata_action.py
# @Software: PyCharm
import os
from configs.base_path import TEST_DATA_PATH
from dataManager.resource_action import ResourceHelper
import copy

def __get_all_excel_data():
    files = [os.path.join(TEST_DATA_PATH, file) for file in os.listdir(TEST_DATA_PATH) if
             file.endswith('.xlsx') or file.endswith('.xls')]
    files_data={}
    resourceHelper=ResourceHelper()
    for file in files:
        try:
            file_data=resourceHelper.read_all_param_excel(file)
            for sheet_name,data in file_data.items():
                files_data.setdefault(sheet_name,[]).extend(data)
        except Exception as e:
            print('用例文件《%s》打开失败！' %file)
    return files_data
files_data = __get_all_excel_data()

def get_case_data(sheet_name='cases'):
    return files_data.get(sheet_name)

def __get_all_key_excel_data():
    files_data
    files_key_data={}
    for sheet_name,sheet_data in files_data.items():

        for row_data in sheet_data:
            # print(row_data)
            files_key_data.setdefault(row_data.get('case_id'),[]).append(row_data)
    return files_key_data
files_key_data=__get_all_key_excel_data()
from pprint import pprint
pprint(files_key_data)