#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: runServer.py
Author: ronnyzh
Date: 2020-02-24 19:32
Revision: Revision: 1.0.0
Description: $Description$
"""

from server import app

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=9000)
