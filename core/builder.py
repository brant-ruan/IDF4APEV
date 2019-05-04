#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : builder.py
@Time    : 2019-04-20 11:06
@Author  : Bonan Ruan
@Desc    :
"""

import utils.consts as consts
import utils.utils as utils
import time
import os

# Build Templates
APPLICATION_MK_TEMPLATE = "APP_ABI := %s\n" + \
    "APP_PLATFORM := android-%s"

ANDROID_MK_TEMPLATE = "LOCAL_PATH := $(call my-dir)\n" + \
    "include $(CLEAR_VARS)\n" + \
    "LOCAL_SRC_FILES := \\\n" + \
    "%s\n" + \
    "LOCAL_CFLAGS += -DDEBUG -D__ARM__ -Wunused\n" + \
    "LOCAL_MODULE := %s\n" + \
    "LOCAL_MODULE_TAGS := optional\n" + \
    "LOCAL_CFLAGS += -std=c99\n" + \
    "LOCAL_LDFLAGS += -static\n" + \
    "include $(BUILD_EXECUTABLE)\n"


class Builder:
    def __init__(self):
        pass

    def build_poc(self, poc_file, device_name, abi, sdk):
        poc_bin = poc_file[:-2]
        application_mk = APPLICATION_MK_TEMPLATE % (str(abi), str(sdk))
        android_mk = ANDROID_MK_TEMPLATE % (poc_file, poc_bin)
        original_src = "%s/%s/%s" % (consts.IDF_HOME,
                                     consts.POC_CODE_PATH, poc_file)
        work_dir = "%s/%s/%s_%s_%d/" % (consts.IDF_HOME,
                                        consts.TEMP_PATH,
                                        poc_bin,
                                        device_name,
                                        int(time.time()))
        build_dir = work_dir + "jni/"
        # mkdir for work
        os.system("mkdir -p %s" % build_dir)

        utils.write_file(build_dir + "Application.mk", application_mk)
        utils.write_file(build_dir + "Android.mk", android_mk)

        # copy src file
        os.system("cp %s %s" % (original_src, build_dir))
        # ndk-build
        os.system("cd %s; ndk-build &> /dev/null" % build_dir)

        return "%s/libs/%s/%s" % (work_dir, abi, poc_bin)
