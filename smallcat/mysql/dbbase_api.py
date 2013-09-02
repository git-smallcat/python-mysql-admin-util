# --encoding=utf8--
import mysql.connector

def connect(config):
    cnx =None
    try:
        cnx = mysql.connector.connect(**config)        
    except mysql.connector.Error as e:
        print('connect fails![]'.format(e))
    return cnx

def query(cnx,sql,*param):
    cursor = cnx.cursor(True)
    cursor.execute(sql,param)
    return cursor

def insert(cnx,sql,*param):
    cursor =cnx.cursor()
    cursor.execute(sql,param)
    cursor.close()
    return cursor.lastrowid

def update(cnx,sql,*param):
    cursor =cnx.cursor()
    cursor.execute(sql,param)
    cursor.close()

def delete(cnx,sql,*param):
    cursor = cnx.cursor()
    cursor.execute(sql,param)
    cursor.close()
