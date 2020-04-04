#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: public_sqlFormat.py
Author: ronnyzh
Date: 2020-03-01 4:56
Revision: $Revision$
Description: $Description$
"""
import re


class FormatSql(object):
    """sql语句格式化"""
    PARAMERTS_REG = re.compile(r':([_0-9]*[_A-z]+[_0-9]*[_A-z]*)')

    def __init__(self, tableName: str, **kwargs):
        self.tableName = tableName  # 表名
        self.kwargs = kwargs  # 字典参数
        self.columnNames = kwargs.get('columnNames', [])  # 语句中的列
        self.formatKeyNum = 0  # 格式化的key位数
        self.formatDict = {}
        self.whereStr = ''
        self.orderStr = ''
        self.pageNumber = 0
        self.ageSize = 10
        whereParams = kwargs.get('whereParams', {})  # 语句条件
        if 'data' in whereParams:
            whereData = whereParams.get('data')
            joinStr = whereParams.get('joinStr', 'AND')
            sign = whereParams.get('sign', '=')
            tmpWhereStr = self.getWhereStr_ByDatas(whereDatas=whereData, joinStr=joinStr, sign=sign)
            self.setWhereStr(tmpWhereStr)

    def getWhereStr_ByDatas(self, whereDatas, joinStr='AND', sign='='):
        """获取条件语句，AS： `id` = :value_1 AND `name` = :value_2"""
        whereStr = ''
        for _key, _value in whereDatas.items():
            str_ = self.insertWhereData(key=_key, value=_value, sign=sign)
            whereStr += '%s %s ' % (str_, joinStr)
        whereStr = whereStr.strip().strip(joinStr).strip()
        return whereStr

    def insertWhereData(self, key, value, sign='='):
        """获取单个条件语句， AS： `id` = :value_1 AND"""
        tmpValueName = self.getNextTmpValueName()
        if isinstance(value, str):
            value = value.replace("'", "\\'").replace('"', '\\"')
        elif isinstance(value, (tuple, list)) and sign == 'in':
            value = tuple(value)
        self.formatDict[tmpValueName] = value
        return "`%s` %s :%s" % (key, sign, tmpValueName)

    def getNextTmpValueName(self, incr=1):
        """对条件语句中value + 1， AS： value_1"""
        self.formatKeyNum += incr
        return 'value_%s' % (self.formatKeyNum)

    def setWhereStr(self, whereStr):
        """设置条件语句属性"""
        self.whereStr = whereStr

    def addWhereStr(self, whereStr, joinStr='AND'):
        """拼接旧新条件语句"""
        if self.whereStr:
            self.whereStr += ' %s %s' % (joinStr, whereStr)
        else:
            self.whereStr += ' %s' % whereStr

    def joinWhereStr(self, joinStr='AND', *args):
        """返回新条件语句"""
        whereStr = ''
        for _arg in args:
            whereStr += '(%s) %s ' % (_arg, joinStr)
        whereStr = whereStr.strip().strip(joinStr).strip()
        return whereStr

    def fiterSqlStr(self):
        """获取sql完整语句"""
        sqlStr = ''
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr

    def tryGetAllSql(self):
        """获取sql完整语句，但是此处只是预览"""
        sqlStr = self.fiterSqlStr()  # 子类重写fiterSqlStr方法
        for _key, _value in self.formatDict.items():
            if isinstance(_value, str):
                _value = "'%s'" % _value
            sqlStr = sqlStr.replace('%%(%s)s' % _key, str(_value))
        return sqlStr

    def getSqlStrAndArgs(self):
        """获取sql语句和值字典"""
        return self.fiterSqlStr(), self.formatDict


class FormatSql_Select(FormatSql):
    """sql查询格式化"""

    def getTableSql(self):
        """获取查询列的语句"""
        columnNames = self.kwargs.get('columnNames')
        if columnNames:
            keysStr = '`,`'.join(columnNames)
            tableSql = 'SELECT `%s` FROM %s' % (keysStr, self.tableName)
        else:
            tableSql = 'SELECT * FROM %s' % (self.tableName)
        return tableSql

    def doJoinTable(self):
        """获取左联/右联的语句"""
        joinType = self.kwargs.get('joinType', 'JOIN')
        joinTableName = self.kwargs.get('joinTableName', '')
        onStr = self.kwargs.get('onStr', '')
        if not joinTableName:
            return ''
        if onStr:
            joinTableStr = '%s %s ON %s' % (joinType, joinTableName, onStr)
        else:
            joinTableStr = '%s %s' % (joinType, joinTableName)
        return joinTableStr

    def doOrderBy(self):
        """获取排序的语句"""
        orderBy = self.kwargs.get('orderBy', '')
        orderType = self.kwargs.get('orderType', 'DESC')
        if not orderBy:
            return ''
        return 'ORDER BY `%s` %s' % (orderBy, orderType)

    def doPaging(self):
        """获取分页语句"""
        pageNumber = self.kwargs.get('pageNumber')
        pageSize = self.kwargs.get('pageSize')
        if not pageNumber and not pageSize:
            return ''
        return 'limit %s , %s' % (pageNumber, pageSize)

    def fiterSqlStr(self):
        """拼接整个查询语句， AS： "SELECT `id` from table where id=%(value_1)s ORDER BY `create_time` DESC """
        sqlStr = self.getTableSql()  # 获取查询列的语句
        joinSql = self.doJoinTable()  # 获取左联/右联的语句
        pageSql = self.doPaging()  # 分页语句
        if joinSql:
            sqlStr += ' ' + joinSql
        if self.whereStr:
            sqlStr += ' WHERE ' + self.whereStr
        orderStr = self.doOrderBy()
        if orderStr:
            sqlStr += ' ' + orderStr
        if pageSql:
            sqlStr += ' ' + pageSql
        sqlStr = sqlStr.replace('  ', ' ')
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


class FormatSql_Insert(FormatSql):
    """sql插入格式化"""

    def __init__(self, **kwargs):
        super(FormatSql_Insert, self).__init__(**kwargs)
        self.datasDict = kwargs.get('datasDict', {})

    def fiterSqlStr(self):
        """获取整个插入语句， AS： """
        keyStr = []
        valueStr = []
        for _key, _value in self.datasDict.items():
            tmpValueName = self.getNextTmpValueName()
            self.formatDict[tmpValueName] = _value
            keyStr.append(_key)
            valueStr.append(':%s' % tmpValueName)
        sqlStr = 'INSERT INTO %s (`%s`) VALUES (%s)' % (self.tableName, '`,`'.join(keyStr), ','.join(valueStr))
        sqlStr = sqlStr.replace('  ', ' ')
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


class FormatSql_Update(FormatSql):
    """sql更新格式化"""

    def __init__(self, **kwargs):
        super(FormatSql_Update, self).__init__(**kwargs)
        self.datasDict = kwargs.get('datasDict', {})

    def getSetDataStr(self):
        setDataStr = self.getWhereStr_ByDatas(self.datasDict, joinStr=',')
        return setDataStr

    def fiterSqlStr(self):
        setData = self.getSetDataStr()
        sqlStr = 'UPDATE %s SET %s' % (self.tableName, setData)
        if self.whereStr:
            sqlStr += ' WHERE ' + self.whereStr
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


class FormatSql_Delete(FormatSql):
    """sql删除格式化"""

    def fiterSqlStr(self):
        sqlStr = 'DELETE FROM %s' % (self.tableName)
        if self.whereStr:
            sqlStr += ' WHERE ' + self.whereStr
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


# if __name__ == '__main__':
#     from public.public_func import *
#     from event.model_asyn_mysql import *
#     from configs import CONFIGS
#     from public.public_logger import *
#     import asyncio
#     from event.model_mysql import *
#
#     mysql_logger = getHandlerLogger(fileLabel='mysql', loggerLabel='mysql', level=logging.DEBUG,
#                                     handler_types=[Handler_Class.RotatingFile])
#     async_mysqlDb = Async_Mysql(CONFIGS['async_mysql'], logger=mysql_logger)
#     usual_mysqlDb = Usual_Mysql(CONFIGS['mysql'])
#
#     method = 'select'
#     data = {'account': 'TST_TEST02000', 'encryption': 'encryption', 'agentId': 'TST0200',
#             'create_time': 1528102481, 'update_time': 1598102481, 'is_deleted': 0}
#
#
#     def getSql_match_player(method, data):
#         datasDict = dictParseValue(parserObj={
#             'account': {'type': str, 'isMust': True},
#             'encryption': {'type': str, 'isMust': True},
#             'agentId': {'type': str, 'isMust': True},
#             'create_time': {'type': int, 'isMust': True},
#             'update_time': {'type': int, 'isMust': True},
#             'is_deleted': {'type': int, 'isMust': True},
#         }, onlyParseKey=True, **data)
#         if method == 'select':
#             sqlCls = FormatSql_Select(
#                 **dict(
#                     tableName='user',
#                     whereParams={
#                         'data': {},
#                     },
#                     columnNames=['id', 'account'],
#                     orderBy='create_time',
#                 )
#             )
#             a1 = sqlCls.getWhereStr_ByDatas({'create_time': 100000}, joinStr='AND', sign='>=')
#             a2 = sqlCls.getWhereStr_ByDatas({'create_time': 152810248100}, joinStr='AND', sign='<=')
#             a4 = sqlCls.joinWhereStr("AND", a1, a2)
#             sqlCls.addWhereStr(a4)
#             return sqlCls.getSqlStrAndArgs()
#
#         elif method == 'insert':
#             sqlCls = FormatSql_Insert(**dict(
#                 tableName='user',
#                 datasDict=datasDict,
#             ))
#             return sqlCls.getSqlStrAndArgs()
#         elif method == 'update':
#             sqlCls = FormatSql_Update(**dict(
#                 tableName='user',
#                 datasDict=datasDict,
#                 whereParams={
#                     'data': {'id': 200},
#                 },
#             ))
#             return sqlCls.getSqlStrAndArgs()
#
#
#     sqlStr, sqlArgs = getSql_match_player(method=method, data=data)
#     if sqlStr:
#         async def doMysqlJob():
#             await async_mysqlDb.createPool_async()
#             mysql_logger.info(u'%s %s' % (sqlStr, sqlArgs))
#             return await async_mysqlDb.select(sqlStr, sqlArgs)
#
#         loop = asyncio.get_event_loop()
#         res = loop.run_until_complete(doMysqlJob())
#         print('res', res)
