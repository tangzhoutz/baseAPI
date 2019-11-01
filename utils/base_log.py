# -*- coding: utf-8 -*-
# @Project : WebAutomatic-vis 
# @Time    : 2018/12/13 15:44
# @Author  : zsr
# @File    : base_log.py
# @Software: PyCharm
#TODO：需要把外层引用内层的logger拆离出来。(base_page 引用了prj_log.)
import logging.handlers
import datetime
from functools import wraps
class GetLogger():
    def __init__(self,log_file):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.DEBUG)
        handler = logging.handlers.TimedRotatingFileHandler(
            log_file,
            encoding='utf-8',
            when='midnight',
            interval=1,
            backupCount=7,
            atTime=datetime.time(0, 0, 0, 0)
        )
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    def info(self,lg):
        self.logger.info(lg)
    def critical(self,lg):
        self.logger.critical(lg)
    def debug(self,lg):
        self.logger.debug(lg)
    def error(self,lg):
        self.logger.error(lg)
    def logger_func(self,fn):
        @wraps(fn)
        def _wapper(*args, **kwargs):
            self.logger.info(f"[record_func]:{fn.__name__}(),para:{args},kwpara:{kwargs},run...")
            func = fn(*args, **kwargs)
            self.logger.info(f"[record_func]:{fn.__name__}() done...")
            return func
        return _wapper
