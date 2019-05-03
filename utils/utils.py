#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : functions.py.py
@Time    : 2019-04-20 16:04
@Author  : Bonan Ruan
@Desc    :
"""

RED_STR = "\033[31m%s\033[0m"
GREEN_STR = "\033[32m%s\033[0m"


def show_table(obj_list):
    #TODO
    pass


def debug(message, mode=0):
    if mode == 0:
        print(GREEN_STR % message)
    elif mode == 1:
        print(RED_STR % message)
    return


def error(message):
    debug(message, 1)
    return
