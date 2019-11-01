# -*- coding: utf-8 -*-
# @Project : Automation 
# @Time    : 2018/10/9 15:56
# @Author  : 
# @File    : work_path.py
# @Software: PyCharm
import os
from configs import bxmat
#AUTO_PATH 是Automation的目录
AUTO_PATH=os.path.dirname(os.path.dirname(__file__))
LOG_PATH=os.path.join(AUTO_PATH,'res/logs')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
TOOLS_PATH=os.path.join(AUTO_PATH,'res/tools')
#用于拼接日志文件名称
PROJECT_NAME=bxmat.test_project_name
IMGS_PATH=os.path.join(AUTO_PATH,'res/imgs',PROJECT_NAME)
if not os.path.exists(IMGS_PATH):
    os.makedirs(IMGS_PATH)
TEST_CASES_PATH=os.path.join(AUTO_PATH,'testcases')
TEST_DATA_PATH=os.path.join(AUTO_PATH,'res/data')