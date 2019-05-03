#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : commander.py.py
@Time    : 2019-04-20 11:04
@Author  : Bonan Ruan
@Desc    :
"""

from core.executer import Executer
from core.builder import Builder
from core.poc_manager import PoCManager
import utils.utils as utils

class Commander:
    def __init__(self):
        self.executer = Executer()
        self.builder = Builder()
        self.poc_manager = PoCManager()

    def load_devices(self, devices):
        self.executer.load_devices(devices)
        utils.debug("%d device(s) connect(s)." % len(devices))