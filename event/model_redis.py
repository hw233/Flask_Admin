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

from functools import wraps
import redis
from configs import CONFIGS

redisdb = None

redis_config = CONFIGS['redis']


def getRedisInst(dbNum=None, redis_config=redis_config, decode_responses=True, redis_type='StrictRedis'):
    global redisdb
    if not dbNum:
        db = redis_config['db']
    redisdb = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'], db=db,
                                   password=redis_config['password'], decode_responses=decode_responses)
    if redis_type == 'redis':
        redisData = redis.Redis(connection_pool=redisdb)
    if redis_type == 'StrictRedis':
        redisData = redis.StrictRedis(connection_pool=redisdb)
    return redisData


def wraps_getRedis(func):
    @wraps(object)
    def main(*args, **kwargs):
        redis = kwargs.get('redis')
        if not redis:
            redis = getRedisInst()
        kwargs['redis'] = redis
        return func(*args, **kwargs)

    return main
