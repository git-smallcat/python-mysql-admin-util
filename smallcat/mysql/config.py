# --encoding=utf8--
'''
Created on 2013-8-27

@author: smallcat
'''
DATABASE={
          'default':{
                     #用户名
                     'user':'',
                     #密码
                     'password':'',
                     #数据库ip
                     'host':'127.0.0.1',
                     #数据库端口
                     'port':3306,
                     #数据库名称
                     'database':'',
                     #是否使用unicode编码
                     'use_unicode':True,
                     #字符集
                     'charset':'utf8',
                     #自动提交
                     'autocommit':False,
                     #数据类型是否为mysql数据类型
                     'raw':False
         },
          
         '106db':{
                     #用户名
                     'user':'root',
                     #密码
                     'password':'123456',
                     #数据库ip
                     'host':'192.168.7.106',
                     #数据库端口
                     'port':3306,
                     #数据库名称
                     'database':'test',
                     #是否使用unicode编码
                     'use_unicode':True,
                     #字符集
                     'charset':'utf8',
                     #自动提交
                     'autocommit':False,
                     #数据类型是否为mysql数据类型
                     'raw':True
         } 
}