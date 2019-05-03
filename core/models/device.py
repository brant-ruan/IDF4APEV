#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : device.py
@Time    : 2019-04-23 16:31
@Author  : Bonan Ruan
@Desc    :

adb -s SERIAL_NUM shell getprop ro.adb.secure
adb shell getprop ro.boot.serialno
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.security_patch
adb shell getprop ro.debuggable
adb shell getprop ro.product.cpu.abi
adb shell getprop ro.product.model
adb shell getprop ro.secure
adb shell getenforce
adb shell cat /proc/version
"""

from dateutil import parser


class Device:
    def __init__(self, model, serialno, sdk, security_patch, release,
                 debuggable, abi, proc_version, secure, getenforce, adb_secure):
        self.model = model
        self.serialno = serialno
        self.android_version = release
        self.kernel_version = proc_version.split(' ')[2]
        # e.g. 2019-05-03
        self.kernel_build_date = parser.parse(
            ' '.join(proc_version.split(' ')[-6:])).strftime('%Y-%m-%d')
        self.security_patch_date = security_patch
        self.sdk = sdk
        self.abi = abi
        self.debuggable = debuggable
        self.selinux = getenforce
        self.secure = secure
        self.adb_secure = adb_secure
