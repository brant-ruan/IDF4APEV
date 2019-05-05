#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : commander.py
@Time    : 2019-04-20 11:04
@Author  : Bonan Ruan
@Desc    :
"""

from core.executer import Executer
from core.builder import Builder
from core.poc_manager import PoCManager
import utils.utils as utils
import utils.consts as consts
import time


class Commander:
    def __init__(self):
        self.executer = Executer()
        self.builder = Builder()
        self.poc_manager = PoCManager()

    def load_devices(self, only_number=False):
        devices = self.executer.load_devices(only_number=only_number)
        return devices

    def check_devices(self, devices, pocs):
        for device in devices:
            for poc in pocs:
                time.sleep(1)
                utils.debug(
                    "[*] Checking device <%s> with poc <%s>" %
                    (device.name, poc.name))
                status = self._check_device(device=device, poc=poc)
                if status == consts.VULNERABLE:
                    utils.debug(
                        "[!] Device <%s> is VULNERABLE to vulnerability <%s>" %
                        (device.name, poc.cve), mode=consts.DEBUG_RED)
                else:
                    utils.debug(
                        "[√] Device <%s> is NOT VULNERABLE to vulnerability <%s>" %
                        (device.name, poc.cve), mode=consts.DEBUG_GREEN)
                print("")

    def _check_device(self, device, poc):
        utils.debug(
            "[*] \tBuilding\tpoc: %s\tsdk: android-%s\tabi: %s" %
            (poc.file, device.sdk, device.abi))
        file_path = self.builder.build_poc(
            poc_file=poc.file, device_name=device.name, abi=device.abi, sdk=device.sdk)

        utils.debug(
            "[*] \tExecuting\tpoc: %s\tdevice: %s" %
            (poc.file, device.name))
        status = self.executer.exec_poc(
            device_name=device.name, binary=file_path)

        return status

    def diagnose_devices(self, devices, vulns):
        for device in devices:
            for vuln in vulns:
                utils.debug(
                    "[*] Diagnosing device <%s> with vulnerability <%s>" %
                    (device.name, vuln.cve))
                status = self._diagnose_device(device, vuln)
                if status == consts.VULNERABLE:
                    utils.debug(
                        "[!] Device <%s> MAY BE VULNERABLE to vulnerability <%s>" %
                        (device.name, vuln.cve), mode=consts.DEBUG_YELLOW)
                else:
                    utils.debug(
                        "[√] Device <%s> MAY BE NOT VULNERABLE to vulnerability <%s>" %
                        (device.name, vuln.cve), mode=consts.DEBUG_YELLOW)
                print("")

    def _diagnose_device(self, device, vuln):

        #TODO
        status = consts.NOT_VULNERABLE
        return status
