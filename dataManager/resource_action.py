#coding:utf8
import xlrd
from xlrd.sheet import Sheet,Cell
import os
from utils.log import logger
from datetime import datetime
from typing import Dict, Tuple, List

class ResourceHelper(object):
    '''
    处理文件相关
    '''
    def __init__(self):
        self.current_path=os.path.dirname(os.path.abspath("."))
        logger.info(f'ResourceHelper 当前路径：{self.current_path}')

    def get_reource_path(self,resource_filename) ->str:
        '''
        获取文件路径
        :param resource_filename: 输入resource_file下的文件名
        :return: 文件绝对路径
        '''
        return self.current_path + "\\resource_file\\"+resource_filename

    def read_excel(self, excel_name, sheet_name="Sheet1") ->list:
        '''
        读取excel文件
        :param excel_name: resource_file目录下的文件名
        :param sheet_name: excel文件内的sheet名称
        :return: 当前excel-sheet页中数据list=[row1 data ,row2 data,....]
        '''
        workbook=xlrd.open_workbook(self.get_reource_path(excel_name))
        # workbook = xlrd.open_workbook(excel_name)
        sheet1=workbook.sheet_by_name(sheet_name)
        row_all=sheet1.nrows
        all_data=[]
        for x in range(1,row_all):
            row_data=sheet1.row_values(x)
            all_data.append(row_data)
        return all_data

    def get_excel_date(self,excel_cell_data):
        '''
        将从excel中取到的日期数据转化成字符串，方便输入到输入框或者其他
        :param excel_cell_data: excel中日期 读取出来的 日期格式数据源
        :return:字符串的日期格式 年-月-日，待扩展更多格式
        '''
        __temp = xlrd.xldate_as_tuple(excel_cell_data, 0)
        return "{}-{}-{}".format(__temp[0], __temp[1], __temp[2])
    def get_excel_datetime(self,excel_cell_data,fmt = '%Y-%m-%d %H:%M:%S'):
        '''
        将从excel中取到的日期数据转化成字符串，方便输入到输入框或者其他
        :param excel_cell_data: excel中日期 读取出来的 日期格式数据源
        :param fmt: 日期格式，格式要求和datetime模块一致，默认 '%Y-%m-%d %H:%M:%S'
        :return:字符串的日期格式 年-月-日，待扩展更多格式
        '''
        __temp = xlrd.xldate_as_datetime(excel_cell_data, 0)
        return __temp.strftime(fmt)

    def filter_row_data(self,row_cell_list:List[Cell],datetime_handler:Dict[int,str]=None)->List:
        '''依据传入的 row_cell_list的数据，过滤数据，并返回list数据
            1、解决整型数据读取后变成小数
            2、解决日期时间读取后变成小数，默认格式：'%Y-%m-%d %H:%M:%S'
            3、依据datetime_handler 可以特殊格式化指定列的日期时间格式，没有输入则默认
            4、布尔类型的数据，读取转换为 ture和false
        :param row_cell_list: 传入需要过滤数据的行类型List[Cell]，通过sheet.row_slice(x)获取
        :param datetime_handler:列序号为key（从0开始），日期格式fmt为value的字典
        （如：{0:'%Y-%m-%d %H:%M:%S',2:'%Y-%m-%d'},表示第一列使用xx格式，第三列使用xx格式）
        :return: 返回一行的数据list={value1,value2...}
        以下为ctype类型：
            XL_CELL_EMPTY: 'empty',0
            XL_CELL_TEXT: 'text',1
            XL_CELL_NUMBER: 'number',2
            XL_CELL_DATE: 'xldate',3
            XL_CELL_BOOLEAN: 'bool',4
            XL_CELL_ERROR: 'error',5
            XL_CELL_BLANK: 'blank,6
        '''
        row_data = []
        for y in range(0, len(row_cell_list)):
            ctype = row_cell_list[y].ctype
            cell_value = row_cell_list[y].value
            if ctype == 2 and cell_value % 1 == 0.0:  # ctype为2且为浮点
                cell_value = int(cell_value)
            elif ctype == 3:
                fmt = '%Y-%m-%d %H:%M:%S'
                if y in datetime_handler.keys():
                    fmt = datetime_handler.get(y)
                cell_value = self.get_excel_datetime(cell_value, fmt)
            elif ctype == 4:
                cell_value = True if cell_value == 1 else False
            row_data.append(cell_value)
        return  row_data

    def filter_data(self,sheet:Sheet,datetime_handler:Dict[int,str]=None)->List[Dict[str,object]]:
        ''' 依据过滤传入的sheet中数据，并返回数据
            1、解决整型数据读取后变成小数
            2、解决日期时间读取后变成小数，默认格式：'%Y-%m-%d %H:%M:%S'
            3、依据datetime_handler 可以特殊格式化指定列的日期时间格式，没有输入则默认
            4、布尔类型的数据，读取转换为 ture和false
        :param sheet: 传入Sheet对象
        :param datetime_handler:列序号为key（从0开始），日期格式fmt为value的字典
        （如：{0:'%Y-%m-%d %H:%M:%S',2:'%Y-%m-%d'},表示第一列使用xx格式，第三列使用xx格式）
        :return: 当前excel-sheet页中数据list=[row1{param1:value1,param2:value2...},
        row2{param1:value1,param2:value2...},....]

        以下为ctype类型：
            XL_CELL_EMPTY: 'empty',0
            XL_CELL_TEXT: 'text',1
            XL_CELL_NUMBER: 'number',2
            XL_CELL_DATE: 'xldate',3
            XL_CELL_BOOLEAN: 'bool',4
            XL_CELL_ERROR: 'error',5
            XL_CELL_BLANK: 'blank,6
        '''
        row_all = sheet.nrows
        all_data = []
        # top_data = sheet.row_values(0)
        top_data = self.filter_row_data(sheet.row_slice(1),datetime_handler)
        for x in range(2, row_all):
            row_cell_list = sheet.row_slice(x)
            all_data.append(dict(zip(top_data, self.filter_row_data(row_cell_list,datetime_handler))))
        return all_data
    def read_param_excel(self, excel_name, sheet_name="Sheet1",datetime_handler:Dict[int,str]=None) ->List[Dict[str,object]]:
        '''
        读取excel文件,返回key-value形式数据,支持datetime读取
        :param excel_name: resource_file目录下的文件名
        :param sheet_name: excel文件内的sheet名称
        :param datetime_handler:列序号为key（从0开始），日期格式fmt为value的字典
        （如：{0:'%Y-%m-%d %H:%M:%S',2:'%Y-%m-%d'},表示第一列使用xx格式，第三列使用xx格式）
        :return: 当前excel-sheet页中数据list=[row1{param1:value1,param2:value2...},
        row2{param1:value1,param2:value2...},....]

        '''
        # workbook=xlrd.open_workbook(self.get_reource_path(excel_name))
        workbook = xlrd.open_workbook(excel_name)
        sheet1=workbook.sheet_by_name(sheet_name)
        return self.filter_data(sheet1,datetime_handler)
    def read_all_param_excel(self, excel_name,datetime_handler:Dict[int,str]=None) ->Dict[str,List[Dict[str,object]]]:
        '''
        读取excel文件,返回key-value形式数据,支持datetime读取
        :param excel_name: resource_file目录下的文件名
        :param sheet_name: excel文件内的sheet名称
        :param datetime_handler:列序号为key（从0开始），日期格式fmt为value的字典
        （如：{0:'%Y-%m-%d %H:%M:%S',2:'%Y-%m-%d'},表示第一列使用xx格式，第三列使用xx格式）
        :return: 当前excel 所有sheet页中数据dict={sheet1:[row1{param1:value1,param2:value2...},
        row2{param1:value1,param2:value2...},....],{sheet2:[],[],[],....}}

        '''
        # workbook=xlrd.open_workbook(self.get_reource_path(excel_name))
        workbook = xlrd.open_workbook(excel_name)
        sheets=workbook.sheets()
        excel_data={}
        for sheet in sheets:
            sheetdata=self.filter_data(sheet, datetime_handler)
            excel_data.setdefault(sheet.name,[]).extend(sheetdata)
        return excel_data

if __name__ == "__main__":
    dd={}
    dd[1]='%Y-%m-%d %H:%M:%S'
    dd[2] = '%Y-%m-%d'
    import pprint
    # aa=ResourceHelper().read_param_excel(r'D:\test\项目1\区块信息-1.xlsx',datetime_handler=dd)
    aa = ResourceHelper().read_all_param_excel(r'D:\pyworkspace\baseAPI\res\data\cases.xlsx', datetime_handler=dd)
    # pprint.pprint(aa)
    print(aa)