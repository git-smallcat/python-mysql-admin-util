'''
Created on 2013-9-2

@author: smallcat

1.change user id
ac_user 
has the same id
has the same account
has the same name
''' 

import smallcat.mysql.config as dbconfig
from smallcat.mysql.dbbase_api import connect,query,insert,delete,update

import2DBName='test';
exportFromDBName='testa';
dumplicateUserDBName = 'test1';

def initDbConnect():
    dbconfig_106 = dbconfig.DATABASE.get('106db')
    dbconfig_106['database']=import2DBName
    import2DB = connect(dbconfig_106)
    
    dbconfig_106['database']=exportFromDBName
    exportFromDB = connect(dbconfig_106)
    
    dbconfig_106['database']=dumplicateUserDBName
    dumplicateUserDB = connect(dbconfig_106)
    return (import2DB,exportFromDB,dumplicateUserDB)

def closeDbConnect(cnxs):
    for cnx in cnxs:
        try:
            cnx.close()
        except Exception:
            pass
    
def splitUserData():
    sql = '''
    select id,name,account_id from ac_user
    ''';
    (import2DB,exportFromDB,dumplicateUserDB)=(None,None,None)
    allError = ''
    try:
        (import2DB,exportFromDB,dumplicateUserDB) = initDbConnect()
        import2DB_Max_id = selectMaxUserID(import2DB)
        exportFromDB_Max_id = selectMaxUserID(exportFromDB)
        if exportFromDB_Max_id > import2DB_Max_id:
            print '''错误，用作被导入的数据库应包含最大的用户ID\r\n
                                    使用select max(id) from ac_user ;确认每个库的最大用户id
            '''
            return
        cursor = query(import2DB, sql)
        result = cursor.fetchone()
        #     print result,result[1].decode('gbk')
        while result is not None:
            try:
                resultName=existName(exportFromDB,result[1])
                resultAccount=existAccount(exportFromDB, result[2])
                if resultAccount is not None:
                    lastrowid = storeDumplicateAccount(dumplicateUserDB, exportFromDBName, result[0])
                    if(lastrowid>=0):
                        delSrcDumplicateUser(exportFromDB, result[0])                
                else:
                    if resultName is not None:
                        lastrowid = storeDumplicateName(dumplicateUserDB, exportFromDBName, result[0])
                        if(lastrowid>0):
                            delSrcDumplicateUser(exportFromDB, result[0])
                       
                    
            except Exception,e:
                allError+=result[0]
                print e
            result = cursor.fetchone()
        print allError
        cursor.close()
    finally:
        closeDbConnect((import2DB,exportFromDB,dumplicateUserDB))

def increaseAllSplitUserID():
    (cnx,cnx2,cnxTemp)=(None,None,None)
    try:
        (cnx,cnx2,cnxTemp) = initDbConnect()
        destMaxID = selectMaxUserID(cnx)
        srcMinID = selectMinUserID(cnx2)
        addend = int(destMaxID[0])-int(srcMinID[0]) + 1
        print addend
        #increaseUserID(cnx2, 'ac_user', addend)
        #increaseUserID(cnxTemp, 'ac_user_dup_account', addend)
        increaseUserID(cnxTemp, 'ac_user_dup_name', addend)
    finally:
        closeDbConnect((cnx,cnx2,cnxTemp))

def selectMaxUserID(cnx):
    sql = '''
    select max(id) from ac_user
    '''
    cursor = query(cnx, sql)
    result= cursor.fetchone()
    cursor.close()
    return result

def selectMinUserID(cnx):
    sql = '''
    select min(id) from ac_user
    '''
    cursor = query(cnx, sql)
    result= cursor.fetchone()
    cursor.close()
    return result

def increaseUserID(cnx,table,addend):
    sql='''
    update '''+table+''' set id = id+%s
    '''
    update(cnx, sql,addend)
    

def existAccount(cnx,account):
    sql = '''    
    select * from ac_user where account_id = %s
    ''';
    cursor = query(cnx,sql,account)
    result = cursor.fetchone()
#     if result is not None:
#         print result[0].decode('gbk'),result," account"
    cursor.close()
    return result
    
def existName(cnx,name):
    sql='''
    select * from ac_user where name = %s
    '''
    cursor = query(cnx,sql,name)
    result = cursor.fetchone()
#     if result is not None:
#         print name,name.decode('gbk'),result[0],result[0].decode('gbk'),result," name"
    cursor.close()
    return result
    
def storeDumplicateName(cnxDest,srcDb,role_id):
    sql='''
    insert into ac_user_dup_name
        select * from '''+srcDb+'''.ac_user where id = %s
    '''
    return insert(cnxDest, sql,role_id)

def storeDumplicateAccount(cnxDest,srcDb,role_id):
    sql='''
    insert into ac_user_dup_account
        select * from '''+srcDb+'''.ac_user where id = %s
    '''
    return insert(cnxDest, sql,role_id)

def delSrcDumplicateUser(cnx,role_id):
    sql='delete from ac_user where id = %s'
    return delete(cnx, sql,role_id)


if __name__ =='__main__':
#     splitUserData()
    increaseAllSplitUserID()
#     dbconfig_106 = dbconfig.DATABASE.get('106db')
#     dbconfig_106['database']=dumplicateUserDBName
#     cnx = connect(dbconfig_106)
#     sql='''
#     insert into test1.ac_user
#         select * from testa.ac_user where id <14090045;
#     ''';
#     print insert(cnx, sql)