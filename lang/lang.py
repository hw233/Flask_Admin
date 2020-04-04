#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: Flask_resume
Filename: lang.py
Author: ronnyzh
Date: 2020-02-24 23:46
Revision: $Revision$
Description: $Description$
"""

from define.define_consts import ADMIN_LANG

LANGS = {}


def initializeWeb():
    global LANGS
    langModules = __import__('lang.web', fromlist=['cn', 'tw', 'en'])
    LANGS['CHN'] = langModules.cn
    setattr(LANGS['CHN'], '__code__', 'CHN')


def getLangInst(lang=ADMIN_LANG):
    global LANGS
    assert lang in LANGS
    return LANGS[lang]
