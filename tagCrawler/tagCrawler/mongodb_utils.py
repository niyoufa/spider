#-*- coding: utf-8 -*-
import pymongo
import pdb

# 定义连接池
CONNECTION_POOL = []
MIN_CONNECTION = 10
MAX_CONNECTION = 50
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017

# 初始化连接池
def initConnectionPool():
    """
    作者 : 倪有发  2015-01-21 12:54
    备注 : 初始化mongodb的连接池，
    参数 :
    最后修改 : XXX -- : --
    """
    if len(CONNECTION_POOL) < MAX_CONNECTION :
        client = pymongo.MongoClient(MONGO_HOST,int(MONGO_PORT))
        CONNECTION_POOL.append(client)
        initConnectionPool()
    else:
        print "初始化连接池完毕，当前连接数"+str(MIN_CONNECTION)+","

# 建立连接的函数
def getConnection():
    """
    作者 : 倪有发  2015-01-21 12:54
    备注 : 获取mongodb的连接，
    参数 :
    最后修改 : XXX -- : --
    """
    if len(CONNECTION_POOL) == 0:
        initConnectionPool()

    # 从连接池中取得连接
    conn = CONNECTION_POOL.pop()
    return conn

# 回收连接到连接池
def closeConnection(conn):
    """
    作者 : 倪有发  2015-01-21 12:54
    备注 : 释放mongodb的连接到连接池，
    参数 :
    最后修改 : XXX -- : --
    """
    if len(CONNECTION_POOL) < MAX_CONNECTION:
        CONNECTION_POOL.append(conn)

# 配置数据库信息
def configDB(db_name,table_name):
    # 获取操作mongo的连接
    conn = getConnection()

    # 查询数据库
    db = conn.db_name
    table = db.table_name

    return conn,table

# 保存用户信息的接口
def saveUserInfo(user):
    """
    作者 : 倪有发  2015-01-21 12:54
    备注 : 保存用户的信息，
    参数 :
    最后修改 : XXX -- : --
    """
    # 配置查询数据库
    conn,userinfo = configDB('teamup','USER')
    usersha1 = user["usersha1"]
    # 查询记录的数量
    count =userinfo.find({'usersha1':usersha1}).count()
    if count :
        userinfo.update({'usersha1':usersha1},{'$set':user})
    else:
        userinfo.save(user)

    # 释放连接到连接池
    closeConnection(conn)

# 获取用户信息的接口
def getUserInfo(usersha1):
    """
    作者 : 倪有发  2015-01-21 12:54
    备注 : 查询用户的信息，
    参数 :
    最后修改 : XXX -- : --
    """
    # 配置查询数据库
    conn,userinfo = configDB('teamup','USER')
    user =userinfo.find_one({'usersha1':usersha1})
    # 释放连接到连接池
    closeConnection(conn)

    return user

# 删除用户的信息
def deleteUserInfo(usersha1):
    """
    作者 : 倪有发  2015-01-21 12:54
    备注 : 查询用户的信息，
    参数 :
    最后修改 : XXX -- : --
    """
    # 配置查询数据库
    conn,userinfo = configDB('teamup','USER')
    userinfo.remove({'usersha1':usersha1})
    # 释放连接到连接池
    closeConnection(conn)