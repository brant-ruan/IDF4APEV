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
from cmd2 import Cmd
import os

class IDFShell(Cmd, object):
    def preloop(self):
        #print(consts.banner)
        super(IDFShell, self).preloop()

    def postloop(self):
        print("Bye.")
        super(IDFShell, self).postloop()

    def emptyline(self):
        pass

    def help_introduction(self):
        print("IDF4APEV refers to Integrated Detection Framework for Android\'s Privilege Escalation Vulnerabilites.")

    def do_list(self, s):
        print(s)
        return

    def help_list(self):
        print("list devices - show connected devices")

    def do_exit(self, s):
        exit(consts.EXIT_SUCCESS)

    def do_shell(self, s):
        os.system(s)
    def help_shell(self):
        print("execute shell commands")

    def do_clear(self, s):
        os.system("clear")

    def do_show(self, s):
        if s == "banner":
            print(consts.banner)


def initialize():
    return


def start_idf():
    shell = IDFShell()
    shell.prompt = "idf > "
    shell.cmdloop(intro=consts.banner)
    return


def finish():
    return


if __name__ == "__main__":
    initialize()
    start_idf()
    finish()
