# -*- coding: utf-8 -*-
# @Project : upupup 
# @Time    : 2018/9/18 16:43
# @Author  : 
# @File    : logs.py
# @Software: PyCharm
import logging.handlers
from logging import *
import datetime
import os
from configs.base_path import LOG_PATH,PROJECT_NAME
# from autobase import HTMLTestRunner_cn
from functools import wraps
fmt_detail='%(asctime)s - pid:%(thread)d-%(threadName)s:%(thread)d - %(filename)s[func:%(funcName)s:%(lineno)d] - %(levelname)s - %(message)s'
fmt_sample='%(asctime)s - %(filename)s[func:%(funcName)s:%(lineno)d] - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt_sample)

logger = logging.getLogger(__name__)
# logger=Log(__name__)
logger.setLevel(level = logging.DEBUG)
# handler = logging.FileHandler("logs/news.log",encoding='utf-8')
handler =logging.handlers.TimedRotatingFileHandler(
    os.path.join(LOG_PATH,f"{PROJECT_NAME}.log"),
    encoding='utf-8',
    when='midnight',
    interval=1,
    backupCount=7,
    atTime=datetime.time(0, 0, 0, 0)
)
# formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

#
# 创建一个StreamHandler,用于输出到控制台，
# 一定要定向到 HTMLTestRunner_cn.stdout_redirector或者 HTMLTestRunner_cn.stderr_redirector
# ch = logging.StreamHandler(HTMLTestRunner_cn.stdout_redirector)
# ch.setLevel(logging.DEBUG)
# ch.setFormatter(formatter)
# logger.addHandler(ch)

def logger_func(fn):
    #wraps使得__name__和func_doc能够获得函数原有的docstring和函数名而不是装饰器相关的
    @wraps(fn)
    def _wapper(*args,**kwargs):
        logger.info(f"[record_func]:{fn.__name__}(),para:{args},kwpara:{kwargs}.run...")
        func = fn(*args,**kwargs)
        logger.info(f"[record_func]:{fn.__name__}(),return:{func}. done...")
        return func
    return _wapper