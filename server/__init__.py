#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: __init__.py
Author: ronnyzh
Date: 2020-02-24 19:46
Revision: $Revision$
Description: $Description$
"""

from flask import Flask
from flask import Blueprint
from flask_session import Session
from define.define_consts import *
from event.model_redis import *
from configs import CONFIGS
from lang.lang import initializeWeb
import redis
import datetime

app = Flask(__name__)
adminPrint = Blueprint('admin', __name__)

# redis配置
StrictRedis = getRedisInst()

# app配置
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['SESSION_TYPE'] = APP_SESSION_TYPE
app.config['SESSION_PERMANENT'] = APP_SESSION_PERMANENT
app.config['SESSION_USE_SIGNER'] = APP_SESSION_USE_SIGNER
app.config['SESSION_KEY_PREFIX'] = APP_SESSION_KEY_PREFIX
app.config['SESSION_REDIS'] = StrictRedis
app.config['PERMANENT'] = APP_PERMANENT
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=APP_PERMANENT_SESSION_LIFETIME)
Session(app)

# 安装语言包
initializeWeb()

# 蓝图
from server import admin

app.register_blueprint(adminPrint, url_prefix="/admin")
