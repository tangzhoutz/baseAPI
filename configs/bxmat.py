
# ----------------------------------------------------------------------------------------------------------------------
# 测试相关参数
# ----------------------------------------------------------------------------------------------------------------------
# 测试用例所属文件夹，精确到项目
test_dirs=[r'D:\pyworkspace\baseAPI\testcases']
# D:\pyworkspace\baseAPI\testcases\project2\pet\pet_petId_uploadImage_post.yml
# test_files=[r'D:\pyworkspace\baseAPI\testcases\project3\Account\Account_post.yml']
# 指定测试文件列表
test_files=[r'D:\pyworkspace\baseAPI\testcases\project2\pet\pet_petId_uploadImage_post.yml',
            r'D:\pyworkspace\baseAPI\testcases\project2\pet\pet_petId_post.yml']
# test_files=[r'D:\pyworkspace\baseAPI\testcases\project2\pet\pet_post.yml']

#当前测试项目名
test_project_name='project2'

# bxmat.url.get(project_name)
# TODO 考虑实现为不同项目不同host，也可以是不同用例不同host 从指定配置文件读取。这样调用url.get(project_name)
# 项目对应的host地址
url={'project1':'http://40.73.115.31/','project2':'http://tt-qas.unidms.com/','project3':'http://tt-qas.unidms.com/'}
#
# TODO 考虑实现为从指定文件获取常量数据，文件名作为一级key，文件内参数作为二级。这样调用default_values.get(K).get(k)
default_values={"filename1":{'datakey1':'data1'}}

# ----------------------------------------------------------------------------------------------------------------------
# 控制参数
# ----------------------------------------------------------------------------------------------------------------------


# TODO 考虑实现为从配置文件读取，最大并发数。bxmat.semaphore
semaphore=20

# ----------------------------------------------------------------------------------------------------------------------
# 默认值数据--写入yaml文件或excel
# ----------------------------------------------------------------------------------------------------------------------
# 默认请求头的值，写入yaml的时候使用
default_headers={'Accept-Encoding':'gzip, deflate',
                 'Accept-Language': 'zh-CN,zh;q=0.9',
                 'Connection':'keep-alive',
                 'Accept': 'application/json, text/javascript, */*',
                 'Content-Type':'application/json'}
# 默认的预期结果的值，写入yaml的时候使用
default_expect_response={'code':{'successed':'200'}}