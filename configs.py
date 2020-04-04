#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: configs.py
Author: ronnyzh
Date: 2020-02-24 19:43
Revision: $Revision$
Description: $Description$
"""

CONFIGS = {
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 1
    },
    'mysql': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'x.091015%',
        'database': '365game',
        'maxConnections': 55,
        'minFreeConnections': 11,
    },
    'async_mysql': {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        'password': 'x.091015%',
        "db": "365game",
        # "init_command": 'select count(*) from match_record',
    }
}
