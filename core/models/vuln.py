#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : vuln.py
@Time    : 2019-04-20 15:48
@Author  : Bonan Ruan
@Desc    :
"""


class Vuln:
    def __init__(self, cve, vuln_kernel_ver, vuln_android_ver,
                 poc_id, patch_date, comment):
        self.cve = cve
        self.vuln_kernel_ver = vuln_kernel_ver
        self.vuln_android_ver = vuln_android_ver
        self.poc_id = poc_id
        self.patch_date = patch_date
        self.comment = comment
