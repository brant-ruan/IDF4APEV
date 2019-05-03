#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : executer.py.py
@Time    : 2019-04-20 11:07
@Author  : Bonan Ruan
@Desc    :
"""

from models.device import Device
from adb.client import Client as AdbClient

# you can use the command below to get the return value of an execution of adb shell.
# R=$(adb shell 'ls /mnt/; echo $?' | tail -1 | tr -d '\r')


class Executer:
    def __init__(self):
        # KitKat+ devices require authentication
        #self.signer = sign_m2crypto.M2CryptoSigner(
        #    op.expanduser('~/.android/adbkey'))
        pass

    def load_devices(self, devices=None):
        #print(adb_commands.AdbCommands.Devices())
        client = AdbClient(host="127.0.0.1", port=5037)
        adb_devices = client.devices()
        for dev in adb_devices:
            properties = dev.shell("getprop")
            properties.replace('[', '')
            print(properties)

            #device = Device(dev.)


if __name__ == "__main__":
    e = Executer()
    e.load_devices()