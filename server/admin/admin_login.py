#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: admin_login.py
Author: ronnyzh
Date: 2020-02-24 21:51
Revision: $Revision$
Description: $Description$
"""

from server import adminPrint
from event.model_event import *


@adminPrint.route('/', methods=['GET', 'POST'])
@EventClass.doResponse
class Login(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info['login_url'] = self.pathJoin()

    def get(self):
        tpl_data = {'tpl': 'user/login.html'}
        return self.render(tpl_data)

    @EventClass.checkArgv(parserObj={
        'userName': {'type': str, 'isEmpty': False, 'isName': u'用户名'},
        'passWord': {'type': str, 'isEmpty': False, 'isName': u'密码'},
        'vCode': {'type': str, 'isEmpty': False, 'isName': u'验证码'},
    })
    def post(self, userName, passWord, vCode):
        print(userName, passWord, vCode)
