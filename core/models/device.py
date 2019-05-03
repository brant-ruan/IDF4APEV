#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : device.py
@Time    : 2019-04-23 16:31
@Author  : Bonan Ruan
@Desc    :
"""

from dateutil import parser


class Device:
    def __init__(self, model, serialno, sdk, security_patch, release,
                 debuggable, abi, proc_version, secure, enforce, adb_secure):
        self.model = model
        self.serialno = serialno
        self.android_version = release
        self.kernel_version = ""
        # e.g. 3.10.65
        tmp = proc_version.split(' ')[2]
        for c in tmp:
            if c in"0123456789.":
                self.kernel_version += c
            else:
                break
        # e.g. 2019-05-03
        self.kernel_build_date = parser.parse(
            ' '.join(proc_version.split(' ')[-6:])).strftime('%Y-%m-%d')
        self.sec_patch_date = security_patch
        self.sdk = sdk
        self.abi = abi
        self.debuggable = debuggable
        self.selinux = enforce
        self.secure = secure
        self.adb_secure = adb_secure
