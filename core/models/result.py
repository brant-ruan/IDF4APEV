#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : result.py
@Time    : 2019-05-12 12:54
@Author  : Bonan Ruan
@Desc    :
"""

import time
import utils.consts as consts


class Result:
    def __init__(self):
        self.time = time.time()
        self.res_diagnose = []
        self.res_check = []

    def export(self):

        time_array = time.localtime(self.time)
        format_time = time.strftime("%Y_%m_%d_%H_%M_%S", time_array)
        filename = "IDF4APEV_Report_%s.md" % format_time
        document = "# %s\n\n" % consts.REPORT_NAME
        document += "## Overview\n\n"
        document += "Time: %s\n\n" % time.asctime(time_array)
        document += "%d device(s) diagnosed.\n\n" % self._count_device(self.res_diagnose)
        document += "%d device(s) checked.\n\n" % self._count_device(self.res_check)

        if self.res_check:
            document += "## Results from CHECK\n\n"
            document += "|Device|Vulnerability|Status|\n"
            document += "|:-:|:-:|:-:|\n"
            for res in self.res_check:
                document += "|" + res['device'].name + "|"
                document += res['poc'].cve + "|"
                if res['status'] == consts.VULNERABLE:
                    document += "vulnerable|\n"
                else:
                    document += "not vulnerable|\n"
            document += "\n"

        if self.res_diagnose:
            document += "## Results from DIAGNOSE\n\n"
            document += "|Device|Vulnerability|Status|\n"
            document += "|:-:|:-:|:-:|\n"
            for res in self.res_diagnose:
                document += "|" + res['device'].name + "|"
                document += res['vuln'].cve + "|"
                if res['status'] == consts.VULNERABLE:
                    document += "vulnerable|\n"
                else:
                    document += "not vulnerable|\n"
            document += "\n"

        try:
            f = open("reports/" + filename, "w")
            f.write(str(document))
            f.close()
        except BaseException:
            raise

    def add_diagnose_result(self, device, vuln, status):
        self.res_diagnose.append({
            'device': device,
            'vuln': vuln,
            'status': status
        })

    def add_check_result(self, device, poc, status):
        self.res_check.append({
            'device': device,
            'poc': poc,
            'status': status
        })

    def reset(self):
        self.time = time.time()
        self.res_diagnose = []
        self.res_check = []

    def _count_device(self, res):
        devices = set()
        for check in res:
            devices.add(check['device'].name)

        return len(devices)
