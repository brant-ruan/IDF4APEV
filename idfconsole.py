#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : idfconsole.py.py
@Time    : 2019-04-20 07:47
@Author  : Bonan Ruan
@Desc    :
"""

from utils import consts
from utils import utils
import cmd

class IDFShell(cmd.Cmd, object):
    def preloop(self):
        print(consts.banner)
        super(IDFShell, self).preloop()
    def postloop(self):
        print("Bye.")
        super(IDFShell, self).postloop()
    def emptyline(self):
        pass
    def help_add(self):
        print("add two integral numbers")

def initialize():
    return

def start_idf():
    shell = IDFShell()
    shell.cmdloop()
    return

def finish():
    return

if __name__ == "__main__":
    initialize()
    start_idf()
    finish()