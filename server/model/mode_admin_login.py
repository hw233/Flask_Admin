#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_test
Filename: mode_admin_login.py
Author: ronnyzh
Date: 2020-03-04 12:51
Revision: $Revision$
Description: $Description$
"""
from flask import request
from flask import session
from flask import redirect
from datetime import datetime
from server.admin import access_module
from define.define_redis_key import *
from public.public_func import *
from server import StrictRedis as redis
from define.define_consts import *
import hashlib
import sys
import json

# 菜单权限
TYPE2ACCESS = {
    '0': access_module.ACCESS_SADMIN_MODULES,
    '1': access_module.ACCESS_COMPANY_MODULES,
    '2': access_module.ACCESS_AG_ONE_CLASS_MODULES,
    '3': access_module.ACCESS_AG_TWO_CLASS_MODULES

}

def postLoginData(self, userName, passWord, vCode):
    """
    登录post数据： class Login - post
    """
    if not self.session.get('vCode'):
        return {'code': -1, 'msg': u'验证码过期，请重新登录'}

    if vCode != self.session.get('vCode', '').upper():
        return {'code': -1, 'msg': u'验证码无效'}

    agentIdTable = AGENT_ACCOUNT_TO_ID % (userName)

    if not self.redis.exists(agentIdTable):
        return {'code': -1, 'msg': u'无效的账号/密码'}

    agentId = self.redis.get(agentIdTable)
    adminTable = self.redis.hgetall(AGENT_TABLE % (agentId))

    if adminTable.get("valid") != '1':
        return {'code': -1, 'msg': u'该账号已被冻结'}

    sha256 = hashlib.sha256()
    if not isinstance(passWord, bytes):
        value = str(passWord).encode('utf-8')
    else:
        value = passWord
    sha256.update(value)
    if adminTable.get("passwd") != sha256.hexdigest():
        return {'code': -1, 'msg': u'无效的账号/密码'}

    self.session['lastLoginIp'], self.session['lastLoginDate'], self.session['type'] = map(adminTable.get,
                                                                                           ('lastLoginIp',
                                                                                            'lastLoginDate',
                                                                                            'type'))

    # 更新更新用户最后登录IP、最后登录时间
    self.redis.hmset(AGENT_TABLE % (agentId), {
        'lastLoginIp': request.remote_addr,
        'lastLoginDate': self.curTime.strftime("%Y-%m-%d %H:%M:%S"),
    })
    # 记录session信息
    self.session['account'] = userName
    self.session['id'] = agentId

    hall_fields = ('type', 'parent_id', 'roomcard', 'open_auth')
    agent_type, agent_parentAg, agent_cards, agent_openAuth = self.redis.hmget(AGENT_TABLE % (self.session['id']),
                                                                               hall_fields)
    self.session['agent_role'] = self.lang.TYPE_2_ADMINTYPE.get(agent_type)
    self.session['agent_type'] = agent_type
    if int(agent_type) in [0]:
        self.session['room_card'] = u'无限制'
    else:
        self.session['room_card'] = agent_cards

    # 重新生成权限 ！
    getNewAccess(self.redis, agentId)
    self.session['access'] = str(self.redis.smembers(AGENT2ACCESS % (agentId)))

    # 记录登录日志
    # agentOpLog(self.redis, userName, 1, request.remote_addr)
    return {'code': 1, 'jumpUrl': '/admin', 'msg': u'登录中'}
