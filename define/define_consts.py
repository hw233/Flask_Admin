#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: define_consts.py
Author: ronnyzh
Date: 2020-02-24 19:50
Revision: $Revision$
Description: 模板常量
"""

APP_SECRET_KEY = 'B1Zr98j/3yX$TXG5!18N]3X31FE/,GOP'
APP_SESSION_TYPE = 'redis'
APP_SESSION_PERMANENT = False
APP_SESSION_USE_SIGNER = False
APP_SESSION_KEY_PREFIX = 'FlaskSession:'
APP_PERMANENT = True
APP_PERMANENT_SESSION_LIFETIME = 3600

ADMIN_PATH = '/admin/'
STATIC_PATH = '/static'
BACK_PRE = '/admin'
ADMIN_LANG = 'CHN'
