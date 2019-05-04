#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2019-04-20 16:04
@Author  : Bonan Ruan
@Desc    :
"""

from prettytable import PrettyTable


def write_file(file_path, content):
    try:
        f = open(file_path, "w")
        f.write(content)
        f.close()
    except BaseException:
        raise


def filter_obj(obj_list, entry_name, entry_value):
    try:
        return [obj for obj in obj_list if obj.__dict__[
            entry_name] == entry_value]
    except BaseException:
        return []


def show_table(obj_list):
    x = PrettyTable()

    if len(obj_list) == 0:
        return

    x.field_names = list(vars(obj_list[0]).keys())

    for obj in obj_list:
        x.add_row(list(vars(obj).values()))

    nl_print(x)


def nl_print(msg):
    """
    print with a new line :)
    :param msg:
    :return:
    """
    print(str(msg) + "\n")


RED_STR = "\033[31m%s\033[0m"
GREEN_STR = "\033[32m%s\033[0m"


def debug(message, mode=0):
    if mode == 0:
        print(GREEN_STR % message)
    elif mode == 1:
        print(RED_STR % message)
    return


def error(message):
    debug(message, 1)
    return
