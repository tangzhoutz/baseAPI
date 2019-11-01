# -*- coding: utf-8 -*-
# @Time    : 2019/4/26 16:39
# @Author  : zhou.tang
# @Email   : tangzhoutz@foxmail.com
# @File    : swagger_yaml_builder.py
# @Software: PyCharm
import re
import os
import sys
import copy
from configs.base_path import TEST_CASES_PATH
from pprint import pprint
from requests import Session
from ruamel import yaml
from enum import Enum
import shutil
from configs import bxmat


class SwaggerType(Enum):
    STRING='string'
    NUMBER='number'
    INTEGER='integer'
    BOOLEAN='boolean'
    OBJECT='object'
    ARRAY='array'
    FILE='file'
class SwaggerIn(Enum):
    PATH='path'
    QUERY='query'
    HEADER='header'
    COOKIE='cookie'
    BODY='body'
    FORM='form'
    FORMDATA='formData'
class ContentType(Enum):
    JSON='application/json'
    TEXT_JSON='text/json'
    XML='application/xml'
    TEXT_XML='text/xml'
    X_WWW_FORM_URLENCODED='application/x-www-form-urlencoded'
    # multipart/form-data
    MULTIPART='multipart/'
SwaggerTypeList=[x.value for x in SwaggerType]

template ="""
args:
  - {method}
  - {api}
kwargs:
  -
    caseName: {caseName}
    {data_or_params}:
        {data}
validator:
  -
    json:
      successed: True
"""

# TODO 优化目录信息等
def auto_gen_cases(swagger_url, project_name):
    """
    根据swagger返回的json数据自动生成yml测试用例模板
    :param swagger_url:
    :param project_name:
    :return:
    """
    res = Session().request('get', swagger_url).json()
    data = res.get('paths')

    workspace = os.getcwd()

    project_ = os.path.join(workspace, project_name)

    if not os.path.exists(project_):
        os.mkdir(project_)

    for k, v in data.items():
        pa_res = re.split(r'[/]+', k)
        dir, *file = pa_res[1:]

        if file:
            file = ''.join([x.title() for x in file])
        else:
            file = dir

        file += '.yml'

        dirs = os.path.join(project_, dir)

        if not os.path.exists(dirs):
            os.mkdir(dirs)

        os.chdir(dirs)

        if len(v) > 1:
            v = {'post': v.get('post')}
        for _k, _v in v.items():
            method = _k
            api = k
            caseName = _v.get('description')
            # TODO 目前写了params get和 data （a=xxx&b=xxx）格式，后续补充json
            data_or_params = 'params' if method == 'get' else 'data'
            parameters = _v.get('parameters')

            data_s = ''
            try:
                for each in parameters:
                    data_s += each.get('name')
                    data_s += ': \n'
                    data_s += ' ' * 8
            except TypeError:
                data_s += '{}'

        file_ = os.path.join(dirs, file)

        with open(file_, 'w', encoding='utf-8') as fw:
            fw.write(template.format(
                method=method,
                api=api,
                caseName=caseName,
                data_or_params=data_or_params,
                data=data_s
            ))

        os.chdir(project_)

def auto_gen_cases2(swagger_url, project_name):
    """
    根据swagger返回的json数据自动生成yml测试用例模板
    :param swagger_url:
    :param project_name:
    :return:
    """
    res = Session().request('get', swagger_url).json()
    data = res.get('paths')

    workspace = TEST_CASES_PATH

    project_ = os.path.join(workspace, project_name)

    # if not os.path.exists(project_):
    #     os.mkdir(project_)

    for k, v in data.items():
        pa_res = re.split(r'[/]+', k)
        dir, *file = pa_res[1:]

        if file:
            file = ''.join([x.title() for x in file])
        else:
            file = dir

        file += '.yml'

        dirs = os.path.join(project_, dir)

        # if not os.path.exists(dirs):
        #     os.mkdir(dirs)

        os.chdir(dirs)

        if len(v) > 1:
            v = {'post': v.get('post')}
        for _k, _v in v.items():
            method = _k
            api = k
            caseName = _v.get('description')
            # TODO 目前写了params get和 data （a=xxx&b=xxx）格式，后续补充json
            data_or_params = 'params' if method == 'get' else 'data'
            parameters = _v.get('parameters')

            data_s = ''
            try:
                for each in parameters:
                    data_s += each.get('name')
                    data_s += ': \n'
                    data_s += ' ' * 8
            except TypeError:
                data_s += '{}'

        file_ = os.path.join(dirs, file)

        with open(file_, 'w', encoding='utf-8') as fw:
            fw.write(template.format(
                method=method,
                api=api,
                caseName=caseName,
                data_or_params=data_or_params,
                data=data_s
            ))

        os.chdir(project_)

def parse_swagger(url):
    '''
    解析swagger返回的json数据，将数据转为以下格式
    INTERFACES=[{'api':api,'method':method，'summary':summary,'parameters':parameters},{}...]
    :param url:
    :return: INTERFACES=[{'api':api,'method':method},...]
    '''
    INTERFACES=[]
    # session = HTMLSession()
    # r = session.get(url)
    datas=Session().request('get', url).json()
    print(datas)
    # print(datas['tags'])
    # tags=datas['tags']
    paths=datas.get('paths')
    defins=datas.get('definitions')
    # print(defins)
    #获取define
    def parse_define(define_path):
        '''
        :param d:
        :param define_path:
        :return:
        '''
        try:
            _pathss=define_path.split('/')[2:]
            # print(_pathss)
            _value=defins
            for x in _pathss:
                _value=_value.get(x)
            return _value
        except Exception as e:
            return define_path

    def get_ref(param_define):
        '''
        递归处理json数据，处理ref关联
        :param param_define:
        :return:
        '''
        if isinstance(param_define, dict):

            for param_k in list(param_define):
                param_v=param_define.get(param_k)
                # get_ref(param_k,param_v,result)
                get_ref(param_v)
                if param_k == '$ref':
                    paramters = parse_define(param_v)
                    # 如果获取到对应参数定义，则获取properties
                    if paramters:
                        para_ex = paramters.get('properties')
                        print('↓↓参数示例：{}'.format(para_ex))
                        # result['para_eg'] = para_ex
                        print(param_define)
                        # result.update({p_k:para_ex})
                        param_define.update(para_ex)
                        del(param_define[param_k])
                        if isinstance(para_ex, dict):
                            # get_ref(p_k, para_ex, result.get(p_k))
                            get_ref(para_ex)

        else:
            return
    #解析tags
    # for x in tags:
    #     for key,value in x.items():
    #         print('tags:{},{}'.format(key,value),end=' ')
    #     print('')
    #解析paths
    nums=1

    for key,value in paths.items():
        APIS=[]
        print('----'*10)
        print(nums)
        print('api url=',key)
        methodss=0
        for k,v in value.items():
            APIS.append({})
            APIS[methodss]['api'] = key
            print('method方法:',k)
            APIS[methodss]['method']=k
            print('对应的tag（大标题）:',v['tags'])
            APIS[methodss]['tags']=v['tags']
            APIS[methodss]['consumes'] = v.get('consumes') or []
            # print('api 注释：',v['summary'])
            # APIS[methodss]['summary']=v['summary']
            APIS[methodss]['para_eg']=[]
            APIS[methodss]['responses']=[]
            if v.get('parameters'):
                #有这个键则显示
                print('api参数：',v['parameters'])
                APIS[methodss]['parameters']=v['parameters']
                for p in v['parameters']:
                    #TODO 暂时写死response 因为swagger里面大多没有写完整的response判断信息
                    APIS[methodss]['responses'].append({'code':{'successed':'200'}})
                    result = {}
                    print('↓api参数详细说明：参数类型：{},必填：{}，参数名：{}，参数描述：{}'.format(p.get('in'),p.get('required'),p.get('name'),p.get('description')))
                    # param_define=p.get('schema') if p.get('schema') else p
                    param_define=copy.deepcopy(p)

                    if isinstance(param_define,dict):
                        # m_param_define = param_define.copy()
                    # if isinstance(p, dict):
                    #     m_param_define = p.copy()
                    # result=p.get('schema').copy()
                    # print("aaaa{}".format(result))
                        get_ref(param_define)

                        APIS[methodss]['para_eg'].append(param_define)
                        print("hahhahahahha{}".format(param_define))
                        # pprint(APIS)
                    # if isinstance(param_define,dict):
                    #     for param_k,param_v in param_define.items():
                    #         if param_k=='$ref':
                    #             paramters=parse_define(param_v)
                    #             #如果获取到对应参数定义，则获取properties
                    #             if paramters:
                    #                 para_ex=paramters.get('properties')
                    #                 print('↓↓参数示例：{}'.format(para_ex))
                    #                 APIS[methodss]['para_eg']=para_ex
                    #                 for pr_key,pr_value in para_ex.items():
                    #                     if pr_value.get('items'):
                    #                         print('↓↓↓参数示例详解：',pr_key,pr_value['type'],parse_define(pr_value.get('items').get('$ref')))

                                            # APIS[methodss]['para_eg_detail']=pr_key
                                # print('参数示例：{}'.format(paramters.get('properties')))
            methodss+=1
        INTERFACES.append(APIS)
        nums+=1
    print('----' * 10)
    print(f'接口数：{nums-1}')
    return INTERFACES
    # return result

def parase_swagger_interfaces(INTERFACES):
    '''
    再次解析从swagger获取到的接口数据
    INTERFACES=[{'api':api,'method':method},...]
    :param INTERFACES=parse_swagger(url)
    :return:按tags排序的接口数据列表，用于写入yaml 示例EXCEL_DATA_LIST=[[api,method,tags,summary,paras],[],...]
    '''

    YAML_DATA_DICT = {}
    # M_INTERFACES=INTERFACES.copy()
    def filter_params2(pr,pr_k):
        '''
        递归处理post和get数据，处理枚举enum 数组 array ，以及普通类型
        :param pr:
        :param pr_k:
        :return:
        '''
        paras=pr.get(pr_k)
        if isinstance(paras, dict):
            for param_k in list(paras):
                param_v=paras.get(param_k)

                filter_params2( paras, param_k)
                # if param_k == 'enum':
                #     # pr={}
                #     pr.update({pr_k: str(param_v)})
                # elif param_k=='items' and paras.get('type') and paras.get('type')=='array':
                #     # paras.clear()
                #     print(param_v)
                #     print(pr_k)
                #     pr.pop(pr_k)
                #     pr.setdefault(pr_k,[]).append(param_v)
                #     pprint(pr)
                #     filter_params2(pr, pr_k)
            if paras.get('enum') and paras.get('type') in SwaggerTypeList:
                pr.update({pr_k: str(paras.get('enum'))})
            elif paras.get('items') and paras.get('type') and paras.get('type') == SwaggerType.ARRAY.value:
                # paras.clear()
                pr.pop(pr_k)
                pr.setdefault(pr_k, []).append(paras.get('items'))
                # pprint(pr)
                filter_params2(pr, pr_k)
            elif paras.get('type') and paras.get('type') == SwaggerType.FILE.value:
                pr.update({pr_k: str(paras)})
            elif paras.get('type') and paras.get('type') in SwaggerTypeList:
                pr.update({pr_k: str(paras)})



                    # paras.update(param_v)

        else:
            return
    def filter_params(pr, pr_k):
        '''
        处理数据，依据第一层的in类型，处理并返回post()数据（body、form、formData）和get数据（query）
        :param pr:
        :param pr_k:
        :return:
        '''
        #TODO 新增json 和 data区分。补充文件处理。
        json_d={}
        post_d = {}
        get_d = {}
        paras=pr.get(pr_k)
        # if len(paras)==1:
        #     pr.update({pr_k:paras[0]})

        for para in paras:
            if para.get('in') and para.get('in')==SwaggerIn.QUERY.value:
                tmp=para.pop('name')
                get_d.update({tmp:para})
                # get_d.append(para)
            elif para.get('in') and para.get('in')==SwaggerIn.BODY.value :
                if para.get('schema'):
                    post_d=para.get('schema')
                else:
                    post_d=para
            elif para.get('in') and para.get('in') in(SwaggerIn.FORM.value,SwaggerIn.FORMDATA.value):
                tmp = para.pop('name')
                post_d.update({tmp: para})
        return post_d,get_d

    def isContentType(consumes,contentType):
        for consume in consumes:
            if consume.startswith(contentType):
                return consume
        return False


    for x in INTERFACES:
        for y in x:
            y = copy.deepcopy(y)
            print('---' * 10)
            print(y['api'])
            print(y['method'])
            print(y['tags'][0])
            # print(y['summary'])
            #
            data = {}
            kwarg={}
            headers=bxmat.default_headers
            contentType={}
            api = y['api']
            method = y['method']
            tags = y['tags'][0]
            # summary = y['summary']
            paras = 'None'
            consumes=y['consumes']
            if y.get('para_eg'):
                post_d,get_d=filter_params(y,'para_eg')
                y['post_d']=post_d
                y['get_d']=get_d
                filter_params2(y, 'post_d')
                filter_params2(y, 'get_d')
                post_d=y['post_d']
                get_d=y['get_d']
            elif y.get('parameters'):
                para_eg = {}
                for d in y.get('parameters'):
                    if d.get('description'):
                        para_eg[d['name']] = d['description']
                    else:
                        para_eg[d['name']] = d['type']
                print(para_eg)
                paras = para_eg
            kwarg.setdefault('caseName',api[1:].replace('/','_').replace('{','').replace('}','')+'_'+method)
            if get_d:
                kwarg['params'] = get_d
            if post_d:
                if isContentType(consumes,ContentType.JSON.value) or isContentType(consumes,ContentType.TEXT_JSON.value) :
                    contentType=(isContentType(consumes,ContentType.JSON.value) or isContentType(consumes,ContentType.TEXT_JSON.value))+';charset=UTF-8'
                    kwarg['json'] = post_d
                elif isContentType(consumes,ContentType.X_WWW_FORM_URLENCODED.value):
                    contentType=isContentType(consumes,ContentType.X_WWW_FORM_URLENCODED.value)+';charset=UTF-8'
                    kwarg['data'] = post_d
                elif isContentType(consumes,ContentType.MULTIPART.value):
                    contentType=isContentType(consumes, ContentType.MULTIPART.value)
                    kwarg['data'] = post_d
                else:
                    kwarg['data'] = post_d
            # TODO 暂时写死response 因为swagger里面大多没有写完整的response判断信息
            response=bxmat.default_expect_response
            # headers['Accept-Encoding']='gzip, deflate'
            # headers['Accept-Language']='zh-CN,zh;q=0.9'
            # headers['Connection']='keep-alive'
            # headers['Accept']='application/json, text/javascript, */*'
            if contentType:
                headers['Content-Type']=contentType
            data.setdefault('args', []).extend([method,api])
            data.setdefault('headers',headers)
            data.setdefault('kwargs',[]).append(kwarg)
            data.setdefault('validator', []).append(response)

            YAML_DATA_DICT.setdefault(tags, []).append(data)
            print('---' * 10)

    # return EXCEL_DATA_LIST
    return YAML_DATA_DICT

from configs.base_path import TEST_CASES_PATH
def write_yml(project_name,YAML_DATA_DICT,model=0):
    '''

    :param project_name:
    :param YAML_DATA_DICT:
    :param model: 模式选择，
    0、直接全量更新，覆盖写文件，会替换掉已有文件，（不会删除多余文件），为默认值;
    1、直接全量更新，覆盖写文件，会替换掉已有文件，并且删除多余文件(只清理yaml文件);
    2、直接全量更新，覆盖写文件，会替换掉已有文件，并且删除多余文件(清理所有文件);
    3、为增量更新，不会覆盖已有文件，只新增多出的接口；
    4、为完全增量更新，新增多出文件的同时删除多余的文件(只清理yaml文件)；
    5、为完全增量更新，新增多出文件的同时删除多余的文件(只清理所有文件)；
    :return:
    '''
    PROJECT_PATH=os.path.join(TEST_CASES_PATH, project_name)
    if not os.path.isdir(PROJECT_PATH):
        os.mkdir(PROJECT_PATH)
    for tag,datas in YAML_DATA_DICT.items():
        tag_path=os.path.join(PROJECT_PATH,tag)
        if not os.path.isdir(tag_path):
            os.mkdir(tag_path)
        os.chdir(tag_path)
        oldfiles=os.listdir(tag_path)
        newfiles=[]
        for data in datas:
            filename=data.get('args')[1].replace('/','_').replace('{','').replace('}','')+'_'+data.get('args')[0]
            filename=filename[1:]+'.yml'
            newfiles.append(filename)
            # 模式3 4 5时，不覆盖已有文件
            if model in (3,4,5) and filename in oldfiles:
                continue
            with open(filename, "w", encoding="utf-8") as f:
                yaml.dump(data, f, Dumper=yaml.RoundTripDumper)
        #模式1和2时，清理多余的文件
        if model in (1,2,4,5):
            isYaml=False
            if model in (2,5):
                isYaml=True
            for oldfile in oldfiles:
                isYaml = isYaml or oldfile.endswith('.yml')
                if not oldfile in newfiles and isYaml:
                    if os.path.isdir(oldfile):
                        shutil.rmtree(oldfile)
                    if os.path.isfile(oldfile):
                        os.remove(oldfile)
    pass



if __name__ == "__main__":


    INTERFACES=parse_swagger('https://petstore.swagger.io/v2/swagger.json')
    # INTERFACES = parse_swagger('http://40.73.115.31/DTSAPI/swagger/docs/v1')
    EXCEL_DATA_LIST=parase_swagger_interfaces(INTERFACES)

    # pprint(EXCEL_DATA_LIST)
    write_yml('project2',EXCEL_DATA_LIST,0)


    # each={'a':[{'b':1,'c':2},{'b':11,'c':33}]}
    # test_data = [tuple(x.values()) for x in each.get('a')]
    # pprint(test_data)
    # print(SwaggerType)
    # for a in SwaggerType:
    #     print(a.value)
    # a=[x.value for x in SwaggerType]
    # print(a)