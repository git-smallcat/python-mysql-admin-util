'''
Created on 2013-9-2

@author: smallcat
'''
from dbbase_api import query,connect
import config as dbconfig

def showStatus(cnx,key):
    cursor = query(cnx, "show status like %s",key)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def showVariable(cnx,key):
    cursor = query(cnx, "show variables like %s",key)
    rows = cursor.fetchall()
    cursor.close()
    return rows

if __name__ =='__main__':
    cnx = connect(dbconfig.DATABASE.get('106db'))
    cursor= query(cnx, 'select now() from dual')
    row=cursor.fetchone()    
    print row
    cursor.close()
    
    rows = showStatus(cnx, '%binlog%')
    for row in rows:
        print row
    
    variables = showVariable(cnx, '%binlog%')
    for variable in variables:
        print variable
    print '--------------------------all-------------------------------------'
    allVar =showVariable(cnx, '%')
    for variable in allVar:
        print variable
    cnx.close()