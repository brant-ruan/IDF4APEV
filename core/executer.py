#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : executer.py
@Time    : 2019-04-20 11:07
@Author  : Bonan Ruan
@Desc    :
"""

from core.models.device import Device
#from models.device import Device
from adb.client import Client as AdbClient
import utils.consts as consts

# you can use the command below to get the return value of an execution of adb shell.
# R=$(adb shell 'ls /mnt/; echo $?' | tail -1 | tr -d '\r')


class Executer:
    def __init__(self):
        pass

    def load_devices(self, only_number=False):
        try:
            # print(adb_commands.AdbCommands.Devices())
            client = AdbClient(host="127.0.0.1", port=5037)
            adb_devices = client.devices()
            # details not needed, we only need the number of connecting devices
            if only_number:
                return [x for x in range(len(adb_devices))]

            devices = []
            for dev in adb_devices:
                # adb shell getprop ro.boot.serialno
                # adb shell getprop ro.build.version.release
                # adb shell getprop ro.build.version.sdk
                # adb shell getprop ro.build.version.security_patch
                # adb shell getprop ro.debuggable
                # adb shell getprop ro.product.cpu.abi
                # adb shell getprop ro.product.model
                # adb shell getprop ro.secure

                # pure-python-adb supplies device.get_properties()
                # props_str = str(dev.shell("getprop"))
                # trantab = props_str.maketrans('', '', '[] \r')
                # props_list = props_str.translate(trantab).split('\n')
                # props_list = [props for props in props_list if props != '']
                # keys = [props.split(':')[0] for props in props_list]
                # values = [props.split(':')[1] for props in props_list]
                # props = dict(zip(keys, values))
                props = dev.get_properties()
                # adb shell cat /proc/version
                proc_version = str(dev.shell("cat /proc/version")).strip()
                name = dev.get_serial_no()
                # adb shell getenforce
                enforce = str(dev.shell("getenforce")).strip()
                device = Device(
                    name=name,
                    model=props['ro.product.model'],
                    sdk=props['ro.build.version.sdk'],
                    security_patch=props['ro.build.version.security_patch'],
                    release=props['ro.build.version.release'],
                    debuggable=props['ro.debuggable'],
                    abi=props['ro.product.cpu.abi'],
                    proc_version=proc_version,
                    secure=props['ro.secure'],
                    enforce=enforce
                )
                devices.append(device)

            return devices
        except KeyError as ke:
            print(ke)

    def exec_poc(self, device_name, binary):

        return consts.NOT_VULNERABLE


if __name__ == "__main__":
    e = Executer()
    a = []
    e.load_devices()
