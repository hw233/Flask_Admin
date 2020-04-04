#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_test
Filename: admin_index.py
Author: ronnyzh
Date: 2020-03-03 7:44
Revision: $Revision$
Description: $Description$
"""

from server import adminPrint
from event.model_event import *


@adminPrint.route('/index', methods=['GET', 'POST'])
@EventClass.doResponse
class Index(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info['home_url'] = self.pathJoin('home')

    def get(self):
        tpl_data = {'tpl': 'index.html'}
        return self.render(tpl_data)

