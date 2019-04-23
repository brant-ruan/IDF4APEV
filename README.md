# IDF4APEV

## Overview

![banner](https://github.com/brant-ruan/IDF4APEV/blob/master/resources/images/banner.png)

**IDF4APEV** refers to *Integrated Detection Framework for Android's Privilege Escalation Vulnerabilites*.

## Developing Process

```
Design&Structure    [√]
poc_code/           [√]
initialize.py       [√]
pocs.json           [√]
vulnabilities.json  [√]
device.py           [ ]
poc.py              [ ]
vulnerability.py    [ ]
commander.py        [ ]
builder.py          [ ]
executer.py         [ ]
poc_manager.py      [ ]
idfconsole          [ ]
test the whole idf  [ ]
Web UI              [ ]
report generator    [ ]
```

## Technical Principles

### Diagnosis

1. If one device's kernel version is NOT located in the range of vulnerable version, it MAY BE not vulnerable.
2. If one device's security-update-date is later than the patch-date of a vulnerability, it MAY BE not vulnerable.

Diagnosis is not reliable because of many elements. For a good & sarcastic example you can see the post [HOW ANDROID PHONES HIDE MISSED SECURITY UPDATES FROM YOU](https://www.wired.com/story/android-phones-hide-missed-security-updates-from-you/).

### Triggering

PoC tells us whether one device is vulnerable or not.

## Installation

```bash
pip install -r requirements.txt
```

## Acknowledgement

The banner is create with the help of *toilet*, which is a very interesting tool and can be installed through `brew install toilet` on Mac OSX :)
