#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    : initialize.py
@Time    : 2019-04-20 15:28
@Author  : Bonan Ruan
@Desc    : to do some initializations before idf works
"""

import sqlite3
from utils import consts
from utils import utils

SQL_CREATE_VULNERABILITY_TABLE = """

"""

SQL_CREATE_POC_TABLE = """

"""

# initialize database
conn = sqlite3.connect(consts.DATABASE)
cursor = conn.cursor()

cursor.execute(SQL_CREATE_VULNERABILITY_TABLE)
cursor.execute(SQL_CREATE_POC_TABLE)

cursor.close()
conn.commit()
conn.close()

utils.debug("Vulnerability table created.")
utils.debug("Vulnerability information added to table.")
utils.debug("PoC table created.")
utils.debug("PoC information added to table.")
#utils.error("failed.")
