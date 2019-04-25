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
import cmd2
import time
import os


class IDFShell(cmd2.Cmd):
    _AVAILABLE_SHOW = ('devices', 'pocs', 'vulns', 'banner')
    _AVAILABLE_DIAGNOSE = ('all',)
    _AVAILABLE_CHECK = ('all',)
    CMD_IDF_FUNCTIONS = "IDF functions"

    def __init__(self):
        super(IDFShell, self).__init__()
        #self.complete_show = self.path_complete
        self.quit_on_sigint = False
        self.echo = False
        self.vuln_num = 0
        self.poc_num = 0
        self.vulns = []
        self.pocs = []

    def initialize(self, pocs, vulns):
        poc_num = 0
        vuln_num = 0
        # TODO

        return poc_num, vuln_num

    def preloop(self):
        self.poutput(consts.banner)
        # load pocs and cves
        self.poc_num, self.vuln_num = self.initialize(self.pocs, self.vulns)
        # time.sleep(0.8)
        utils.debug(
            "%d PoCs for %d vulnerabilities loaded." %
            (self.poc_num, self.vuln_num))
        super(IDFShell, self).preloop()

    def postloop(self):
        self.poutput("Bye.")
        super(IDFShell, self).postloop()

    def help_introduction(self):
        self.poutput(
            "IDF4APEV refers to Integrated Detection Framework for Android\'s Privilege Escalation Vulnerabilites.")

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_version(self, s):
        self.poutput("version: " + consts.IDF_VERSION)

    def help_version(self):
        s = """Usage: version\n\nShow the version of IDF4APEV"""
        self.poutput(s)

    def complete_show(self, text, line, begidx, endidx):
        return [i for i in self._AVAILABLE_SHOW if i.startswith(text)]

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_show(self, s):
        if s == "banner":
            self.poutput(consts.banner)
        elif s == "vulns":
            pass
        elif s == "pocs":
            pass
        elif s == "devices":
            pass
        else:
            self.poutput("Invalid options.")

    def help_show(self):
        pass

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_info(self, s):
        pass

    def help_info(self):
        pass

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_diagnose(self, s):
        pass

    def help_diagnose(self):
        pass

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_check(self, s):
        pass

    def help_check(self):
        pass

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_export(self, s):
        pass

    def help_export(self):
        pass


def start_idf():
    consts.IDF_HOME = os.getcwd()

    shell = IDFShell()
    shell.colors = "Terminal"
    shell.prompt = "idf > "
    #shell.debug = True
    shell.cmdloop(intro=None)
    return


if __name__ == "__main__":
    start_idf()
