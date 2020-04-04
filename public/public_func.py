#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: public_func.py
Author: ronnyzh
Date: 2020-02-24 23:34
Revision: $Revision$
Description: $Description$
"""

from define.define_consts import *
from lang.lang import getLangInst
from collections import OrderedDict
import hashlib
import json
import time
import traceback
import urllib.parse
from datetime import datetime, date
from functools import wraps
import platform
import copy


def getLang():
    """获取语言包"""
    return getLangInst()


class dict_to_obj(dict):
    """返回一个字典对象"""

    def __getattr__(self, name):
        return self.get(name)


class orderedDict_to_obj(dict):
    """返回一个排序字典对象"""

    def __getattr__(self, name):
        return self.get(name)


def dictList_to_obj(dictList: list, isOrder=False) -> list:
    """返回一个字典对象列表，OrderedDict if isOrder else dict"""
    objs = []
    for _dict in dictList:
        objs.append(orderedDict_to_obj(_dict) if isOrder else dict_to_obj(_dict))
    return objs


def getNowStamp(millisecond=False) -> int:
    """返回时间戳"""
    precision = 1
    if millisecond:
        precision = 1000
    return int(time.time() * precision)


def timeStampTo_Second(timeStamp) -> int:
    """返回前十位时间戳"""
    timeStamp = int(str(timeStamp)[:10])
    return timeStamp


def toJsStr(msg):
    return urllib.parse.quote(msg)


def listStrToInt(strList: list, isSorted=False, *args, **kwargs) -> list:
    """接收一个字符串数字列表，返回数字列表, 可进行排序"""
    result = list(map(int, strList))
    if isSorted:
        return sorted(result, *args, **kwargs)
    return result


def get_nowtime() -> str:
    """返回当前日期: %Y-%m-%d %H:%M:%S"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def md5_encode(str):
    return hashlib.md5(str.encode(encoding='utf-8')).hexdigest()


def getSessionId(account):
    hash = hashlib.md5()
    hash.update(str(getNowStamp()).encode(encoding='utf-8'))
    hash.update(account.encode(encoding='utf-8'))
    return hash.hexdigest()


def decorator(*func):
    """同时被多个方法装饰"""

    def deco(f):
        for fun in reversed(func):
            f = fun(f)
        return f

    return deco


class CJsonEncoder(json.JSONEncoder):
    """python转json,支持datetime等格式"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super(CJsonEncoder, self).default(obj)


def pretty_dict(obj: dict, indent=' ') -> str:
    """返回美观性字符串字典"""

    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            # 如果是字符串则拼上""
            if isinstance(k, str):
                k = '"%s"' % k
            if isinstance(v, str):
                v = '"%s"' % v
            # 如果是字典则递归
            if isinstance(v, dict):
                v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
            # case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:  # 开头,拼左花括号
                if len(obj) == 1:
                    yield '{%s: %s}' % (k, v)
                else:
                    yield '{%s: %s,\n' % (k, v)
            elif i == len(obj) - 1:  # 结尾,拼右花括号
                yield '%s%s: %s}' % (indent, k, v)
            else:  # 中间
                yield '%s%s: %s,\n' % (indent, k, v)
    return ''.join(_pretty(obj, indent))

# 一般用于mysql语句, 条件语句
def dictParseValue(parserObj: dict, onlyParseKey=True, **kwargs) -> dict:
    """根据parserObj定义， 接收kwargs， 返回字典"""
    arguments = {}
    if not onlyParseKey:
        arguments = copy.deepcopy(kwargs)
    defaultMap = {
        int: 0,
        str: '',
        float: 0.0,
    }
    defaultFiter = [None, '', 0, 0.0, ' ']
    for _key, _value in parserObj.items():
        filter = copy.deepcopy(defaultFiter)  # 过滤器,如果不是必需,会过滤按条件删除key
        isMust = False  # 是否必需的,true时,key一定会有,无传入值会设置默认值

        if isinstance(_value, dict):
            val_type = _value.get('type', str)
            defaultVal = _value.get('default', defaultMap.get(val_type, None))
            filter = _value.get('filter', filter)
            isMust = _value.get('isMust', isMust)
        else:
            val_type = _value
            defaultVal = defaultMap.get(val_type, None)
        try:
            if isMust:
                theKeyVal = kwargs.get(_key, defaultVal)
                try:
                    theKeyVal = val_type(theKeyVal)
                except Exception as err:
                    print('[Error][dictParseValue] <%s> cant not to [%s]' % (theKeyVal, val_type))
                    traceback.print_exc()
                    theKeyVal = defaultVal
            else:
                if _key not in kwargs:
                    continue
                try:
                    theKeyVal = val_type(kwargs[_key])
                    if filter:
                        if isinstance(filter, list):
                            if theKeyVal in filter:
                                continue
                        elif callable(filter):
                            if filter(theKeyVal):
                                continue
                except Exception as err:
                    traceback.print_exc()
                    continue
            arguments[_key] = theKeyVal
        except Exception as err:
            traceback.print_exc()
            continue
    return arguments


def getCurSystem() -> int:
    """返回当前操作系统类型, Windows: 1, Linux: 2, other: 0"""
    system_None = 0
    system_Windows = 1
    system_Linux = 2
    if platform.system() == 'Windows':
        return system_Windows
    elif platform.system() == 'Linux':
        return system_Linux
    else:
        return system_None
