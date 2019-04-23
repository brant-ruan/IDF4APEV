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
CREATE TABLE "Vulnerability" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"vulnKernelVersion"	TEXT,
	"vulnAndroidVersion"	TEXT,
	"pocIsAvailable"	TEXT,
	"pocId"	INTEGER,
	"patchDate"	TEXT,
	"comment"	TEXT
)
"""

SQL_CREATE_POC_TABLE = """
CREATE TABLE "PoC" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"code"	TEXT,
	"buildOptions"	TEXT,
	"execOptions"	TEXT,
	"cveId"	TEXT,
	"risk"	TEXT,
	"comment"	TEXT
)
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
