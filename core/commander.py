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
                        (device.name, vuln.cve), mode=consts.DEBUG_GREEN)
                print("")

    def _diagnose_device(self, device, vuln):
        # if security patch date is not earlier than the patch date of vuln
        # then this device may be not vulnerable

        if not _date_is_earlier(device_date=device.sec_patch_date,
                                patch_date=vuln.patch_date):
            return consts.NOT_VULNERABLE
        # if kernel version of device is not in the range of vulnerable kernel version
        # then it may be not vulnerable
        if not _kernel_is_in_range(
                device_ver=device.kernel_version, vuln_ver_list=vuln.vuln_kernel_ver):
            return consts.NOT_VULNERABLE

        return consts.VULNERABLE


def _date_is_earlier(device_date, patch_date):
    try:
        # some old devices even do not have a security-patch-date!!!
        if not device_date:
            return True
        if device_date < patch_date:
            return True

        return False
    except BaseException:
        raise


def _kernel_is_in_range(device_ver, vuln_ver_list):
    try:
        dev_ver_num = _version_to_int(device_ver)
        vuln_ver_min = 0
        if vuln_ver_list[0]:
            vuln_ver_min = _version_to_int(vuln_ver_list[0])
        vuln_ver_max = _version_to_int(vuln_ver_list[1])
        if dev_ver_num >= vuln_ver_min:
            if dev_ver_num < vuln_ver_max:
                return True

        return False
    except BaseException:
        raise


def _version_to_int(version):
    ver_num = 0
    i = 1
    ver_list = version.split('.')
    ver_list.reverse()
    for sub_ver in ver_list:
        ver_num += int(sub_ver) * i
        i *= 1000
    return ver_num
