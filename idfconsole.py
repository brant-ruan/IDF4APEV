#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : idfconsole.py
@Time    : 2019-04-20 07:47
@Author  : Bonan Ruan
@Desc    :
"""

from utils import consts
from utils import utils
import cmd2
import os
import json
from core.models.poc import PoC
from core.models.vuln import Vuln
from core.commander import Commander


class IDFShell(cmd2.Cmd):
    _AVAILABLE_SHOW = ('devices', 'pocs', 'vulns', 'banner')
    _AVAILABLE_DIAGNOSE = ('all',)
    _AVAILABLE_CHECK = ('all',)
    CMD_IDF_FUNCTIONS = "IDF functions"

    def __init__(self):
        super(IDFShell, self).__init__()
        self.quit_on_sigint = False
        self.echo = False

        self.vulns = []
        self.pocs = []
        self.devices = []

        self.commander = Commander()

    def initialize(self):

        try:
            # load PoCs
            pocs_dict = json.load(
                open(
                    consts.INFO_JSON_PATH +
                    consts.POC_JSON_FILE))
            for poc_name in pocs_dict:
                poc = PoC(
                    name=poc_name,
                    filename=pocs_dict[poc_name]['filename'],
                    build_options=pocs_dict[poc_name]['build_options'],
                    exec_options=pocs_dict[poc_name]['exec_options'],
                    cve=pocs_dict[poc_name]['cve'],
                    risk=pocs_dict[poc_name]['risk'],
                    comment=pocs_dict[poc_name]['comment'])
                self.pocs.append(poc)
            # load vulnerabilities
            vulns_dict = json.load(
                open(
                    consts.INFO_JSON_PATH +
                    consts.VULN_JSON_FILE))
            for vuln_name in vulns_dict:
                vuln = Vuln(
                    cve=vuln_name,
                    vuln_kernel_ver=vulns_dict[vuln_name]['vuln_kernel_ver'],
                    vuln_android_ver=vulns_dict[vuln_name]['vuln_android_ver'],
                    poc_id=vulns_dict[vuln_name]['poc_id'],
                    patch_date=vulns_dict[vuln_name]['patch_date'],
                    comment=vulns_dict[vuln_name]['comment'])
                self.vulns.append(vuln)
        except BaseException:
            raise

    def preloop(self):
        self.poutput(consts.banner)
        # load pocs and cves
        self.initialize()
        # time.sleep(0.8)
        utils.debug(
            "%d PoC(s) for %d vulnerability/ies loaded." %
            (len(self.pocs), len(self.vulns)))
        # load devices
        self.devices = self.commander.load_devices(only_number=True)
        utils.debug("%d device(s) connect(s)." % len(self.devices))
        super(IDFShell, self).preloop()

    def postloop(self):
        self.poutput("Bye.")
        super(IDFShell, self).postloop()

    def help_introduction(self):
        s = "IDF4APEV refers to Integrated Detection Framework for Android\'s Privilege Escalation Vulnerabilites.\n\n"
        self.poutput(s)

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_version(self, s):
        self.poutput("version: " + consts.IDF_VERSION)

    def help_version(self):
        s = "Usage: version\n\nShow the version of IDF4APEV\n\n"
        self.poutput(s)

    def complete_show(self, text, line, begidx, endidx):
        return [i for i in self._AVAILABLE_SHOW if i.startswith(text)]

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_show(self, s):
        if s == "banner":
            self.poutput(consts.banner)
        elif s == "vulns":
            utils.show_table(self.vulns)
        elif s == "pocs":
            utils.show_table(self.pocs)
        elif s == "devices":
            self.devices = self.commander.load_devices()
            utils.show_table(self.devices)
        else:
            self.poutput("Invalid options.")

    def help_show(self):
        # TODO
        pass

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_diagnose(self, s):
        # TODO
        pass

    def help_diagnose(self):
        # TODO
        pass

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_check(self, s):
        self.devices = self.commander.load_devices()
        device_filtered = self.devices
        poc_filtered = self.pocs

        opt = s.split(' ')
        if len(opt) != 2:
            self.poutput("Invalid options.")
            return
        if opt[0] != "all":
            device_filtered = utils.filter_obj(self.devices, "name", opt[0])
            if not device_filtered:
                self.poutput("Invalid serialno.")
                return
        if opt[1] != "all":
            poc_filtered = utils.filter_obj(self.pocs, "name", opt[1])
            if not poc_filtered:
                self.poutput("Invalid poc name.")
                return
        self.commander.check_devices(devices=device_filtered, pocs=poc_filtered)

    def help_check(self):
        # TODO
        pass

    @cmd2.with_category(CMD_IDF_FUNCTIONS)
    def do_export(self, s):
        # TODO
        pass

    def help_export(self):
        # TODO
        pass


def start_idf():
    consts.IDF_HOME = os.getcwd()
    # clean
    os.system("rm -r %s/cve_* &> /dev/null" % consts.TEMP_PATH)
    shell = IDFShell()
    shell.colors = "Terminal"
    shell.prompt = "idf > "
    shell.debug = True
    shell.cmdloop(intro=None)
    return


if __name__ == "__main__":
    start_idf()
