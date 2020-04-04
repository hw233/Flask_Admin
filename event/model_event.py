#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: event.py
Author: ronnyzh
Date: 2020-02-24 22:29
Revision: $Revision$
Description: $Description$
"""

from flask import request
from flask import session
from flask import render_template
from flask import jsonify
from flask import make_response
from functools import wraps
from datetime import datetime
from define.define_consts import *
from define.define_redis_key import *
from public.public_logger import getHandlerLogger, Handler_Class
from public.public_func import *
import redis
import json
import logging
import os
import types
import re


class EventClass(object):
    """
    事件驱动
    """

    @staticmethod
    def doResponse(cls):
        """
        接收一个类, 返回访问路由对应的类型方法（GET/POST)
        """
        @wraps(cls)
        def wrapper(*args, **kwargs):
            request_method = request.method.upper()
            eventFunc = cls(*args, **kwargs)
            if request_method == 'GET':
                return eventFunc.get()
            if request_method == 'POST':
                return eventFunc.post()
        return wrapper

    @classmethod
    def checkArgv(cls, parserObj=None, *args, **kwargs):
        def control(func, *args, **kwarg):
            """
            检查参数
            """
            @wraps(func)
            def __console(*ag, **kw):
                if isinstance(parserObj, dict):
                    flag, response = cls.parseArgs(parserObj, *ag, **kw)
                    if not flag:
                        return jsonify(response)
                    return func(*ag, **response)
                return func(*ag, **kw)
            return __console
        return control

    @staticmethod
    def parseArgs(parserObj=None, *args, **kwargs):
        arguments = {}
        for _key, _value in parserObj.items():
            if isinstance(_value, dict):
                _type = _value.get('type', str)
                _isEmpty = _value.get('isEmpty', False)
                _isName = _value.get('isName', _key)
                _value = request.values.get(_key, '').strip()
                _value = str(_value)
                defaultMap = {
                    int: _value.isdigit(),
                    str: isinstance(_value, str),
                    float: re.match('\d+\.\d+', _value),
                    bool: _value in ['0', '1', 'True', 'False', 0, 1, True, False],
                }
                if not _isEmpty and not _value:
                    return False, {'code': BaseRequestHandler.State_Msg, 'msg': f'{_isName}不能为空'}

                if defaultMap.get(_type):
                    arguments[_key] = _value
                else:
                    return False, {'code': BaseRequestHandler.State_Msg, 'msg': f'{_isName}参数值非法'}
            else:
                return False, {'code': BaseRequestHandler.State_Msg, 'msg': 'parserObj参数值非法'}
        return True, arguments


class BaseRequestHandler(object):
    """
    父类
    """
    State_Msg = -1
    State_Load = 0
    State_OpenMsg = 1

    def __init__(self, *args, **kwargs):
        """
        设置默认属性
        """
        self.lang = getLang()
        self.curTime = datetime.now()
        self.session = session
        self.redis = redis
        self.info = {
            'ADMIN_PATH': ADMIN_PATH,
            'STATIC_PATH': STATIC_PATH,
            'curDateTime': self.curTime.strftime('%Y-%m-%d %H:%M:%S'),
            'curDate': self.curTime.strftime('%Y-%m-%d'),
        }
        self.logger = getHandlerLogger(fileLabel='%s' % self.info.get('curDate'), handler_type=Handler_Class.HourFile,
                                       level=logging.INFO, when='M')

    def finish(self, parseArg=None):
        """
        返回json数据
        """
        if isinstance(parseArg, dict):
            return jsonify(parseArg)
        else:
            return 'TypeError: "value" is not Type(dict)'

    def render(self, parseArg=None):
        """
        返回html模板
        """
        kwargs = {'lang': self.lang, 'info': self.info, 'session': self.session}
        if isinstance(parseArg, dict):
            if 'tpl' not in parseArg:
                return 'KeyError: "tpl" is not in Key'
            kwargs['template_name_or_list'] = parseArg['tpl']
        if isinstance(parseArg, str):
            parseArg = {'template_name_or_list': parseArg}
        kwargs.update(parseArg)
        return make_response(render_template(**kwargs), 200)

    def pathJoin(self, *paths):
        return os.path.join(self.info.get('ADMIN_PATH'), *paths)
