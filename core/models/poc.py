#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : poc.py.py
@Time    : 2019-04-20 15:49
@Author  : Bonan Ruan
@Desc    :
"""

from utils import consts


class PoC:
    def __init__(self, name, filename, build_options,
                 exec_options, cve, risk, comment):
        self.name = name
        self.file = consts.POC_CODE_PATH + filename
        self.buildOptions = build_options
        self.execOptions = exec_options
        self.cve = cve
        self.risk = risk
        self.comment = comment
