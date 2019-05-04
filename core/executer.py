#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : executer.py.py
@Time    : 2019-04-20 11:07
@Author  : Bonan Ruan
@Desc    :
"""

from core.models.device import Device
#from models.device import Device
from adb.client import Client as AdbClient


# you can use the command below to get the return value of an execution of adb shell.
# R=$(adb shell 'ls /mnt/; echo $?' | tail -1 | tr -d '\r')


class Executer:
    def __init__(self):
        pass

    def load_devices(self, only_number=False):
        # print(adb_commands.AdbCommands.Devices())
        client = AdbClient(host="127.0.0.1", port=5037)
        adb_devices = client.devices()
        # details not needed, we only need the number of connecting devices
        if only_number:
            return [x for x in range(len(adb_devices))]

        devices = []
        for dev in adb_devices:
            # adb shell getprop ro.adb.secure
            # adb shell getprop ro.boot.serialno
            # adb shell getprop ro.build.version.release
            # adb shell getprop ro.build.version.sdk
            # adb shell getprop ro.build.version.security_patch
            # adb shell getprop ro.debuggable
            # adb shell getprop ro.product.cpu.abi
            # adb shell getprop ro.product.model
            # adb shell getprop ro.secure
            props_str = str(dev.shell("getprop"))
            trantab = props_str.maketrans('', '', '[] \r')
            props_list = props_str.translate(trantab).split('\n')
            props_list = [props for props in props_list if props != '']
            keys = [props.split(':')[0] for props in props_list]
            values = [props.split(':')[1] for props in props_list]
            props = dict(zip(keys, values))

            # adb shell cat /proc/version
            proc_version = str(dev.shell("cat /proc/version")).strip()

            # adb shell getenforce
            enforce = str(dev.shell("getenforce")).strip()
            device = Device(
                model=props['ro.product.model'],
                serialno=props['ro.boot.serialno'],
                sdk=props['ro.build.version.sdk'],
                security_patch=props['ro.build.version.security_patch'],
                release=props['ro.build.version.release'],
                debuggable=props['ro.debuggable'],
                abi=props['ro.product.cpu.abi'],
                proc_version=proc_version,
                secure=props['ro.adb.secure'],
                enforce=enforce,
                adb_secure=props['ro.adb.secure']
            )
            devices.append(device)

        return devices


if __name__ == "__main__":
    e = Executer()
    a = []
    e.load_devices()
