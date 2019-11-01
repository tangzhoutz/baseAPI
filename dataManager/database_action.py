# -*- coding: utf-8 -*-
# @Project : POM_demo 
# @Time    : 2018/5/29 17:36
# @Author  : 
# @File    : database_action.py
# @Software: PyCharm Community Edition
import psycopg2
import dataset
from dataset.table import Table
from utils.log import logger

class PostgreSQL_Connect():
    def __init__(self,database,user,password,host,port='5432'):
        self.database=database
        self.user=user
        self.password=password
        self.host=host
        self.port=port
        try:
            logger.info(f'尝试连接数据库：库：{self.database},用户：{self.user},密码：{self.password},host:{self.host},port:{self.port}')
            self.conn = psycopg2.connect(database=self.database,
                                    user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.port)
            logger.info('connect success!')
            print('connect success!')
        except psycopg2.DatabaseError as e:
            logger.error(e)
            exit(e)
        except Exception as e:
            logger.error(e)
            exit(e)

    def executesql(self,sql) ->list:
        logger.info(f'执行sql：{sql}')
        try:
            __cur=self.conn.cursor()
            __cur.execute(sql)
            __results=__cur.fetchall()
            return __results
        except Exception as e:
            logger.error(e)

    def close_connection(self):
        self.conn.close()
        print('connection closed!')
        logger.info('connection closed!')

class Database_Connet():
    def __init__(self,url):
        '''
        :param url:
        # connecting to a SQLite database
        db = dataset.connect('sqlite:///mydatabase.db')
        # connecting to a MySQL database with user and password
        db = dataset.connect('mysql://user:password@localhost/mydatabase')
        MySQL-Python
            mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
        pymysql
            mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
        MySQL-Connector
            mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
        # connecting to a PostgreSQL database
        db = dataset.connect('postgresql://scott:tiger@localhost:5432/mydatabase')
        使用方式和sqlalchemy一致，需要安装对应库
        '''
        try:
            self.db=dataset.connect(url,row_type=dict)
        except Exception as e:
            logger.error(e)
            exit(e)

    def query(self,sql)->dataset.util.ResultIter:
        try:
            result = self.db.query(sql)
            return result
        except Exception as e:
            logger.error(e)
            exit(e)
    def executesql(self,sql)->dataset.util.ResultIter:
        self.db.begin()
        try:
            result=self.db.query(sql)
            self.db.commit()
            return result
        except Exception as e:
            print(e)
            self.db.rollback()
            logger.error(e)
            exit(e)
    def __getitem__(self, table_name)->Table:
        '''重载了下标获取的方法，并标注类型，方便识别自动提示。'''
        return self.db[table_name]
# if __name__ == "__main__":
#     # pp=PostgreSQL_Connect(database="wisdom_education_service_pre", user="postgres",
#     #     password="aorise", host="10.16.4.57", port="5432")
#     # print(pp.executesql('select code,cname from inf_class'))
#     # pp.close_connection()
#
#     sql="INSERT INTO userinfo VALUES ('admin2', '123456', 1, 'ROLE_ADMIN');"
    # ds=Database_Connet('mysql://root:aorise@10.16.4.57:3306/test?charset=utf8')
    # ds = Database_Connet('mysql+mysqlconnector://root:123456@localhost:3306/test_med?charset=utf8')
    # results=ds.executesql('select * from login_cases')
    # for r in results:
    #     print(r)
    # import MySQLdb as mdb
    #
    # conn = mdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='test', charset='utf8')
    # print(conn.query('select * from myspittle'))

    # from sqlalchemy import create_engine
    #
    # # 创建引擎
    # engine = create_engine("mysql://root:123456@localhost:3306/test",encoding='utf8')
    # # 执行sql语句
    # # engine.execute("INSERT INTO user (name) VALUES ('dadadadad')")
    #
    # result = engine.execute(sql)
    # # res = result.fetchall()
    # print(result)