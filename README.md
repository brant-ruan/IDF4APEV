# IDF4APEV

## Overview

![banner.png](https://github.com/brant-ruan/IDF4APEV/blob/master/resources/images/banner.png)

**IDF4APEV** refers to *Integrated Detection Framework for Android's Privilege Escalation Vulnerabilites*.

## Developing Process

```
Design&Structure    [√]
poc_code/           [√]
pocs.json           [√]
vulnabilities.json  [√]
device.py           [√]
poc.py              [√]
vulnerability.py    [√]
result.py           [√]
commander.py        [√]
builder.py          [√]
executer.py         [√]
idfconsole          [√]
test the whole idf  [√]
```

## Usage

```bash
show banner
show devices
show pocs
show cves
# diagnose
diagnose DEVICE_NAME
diagnose all
# trigger
check all all
check all POC_NAME
check DEVICE_NAME POC_NAME
check DEVICE_NAME all
# export report as markdown file into reports/
export
# clean result auto-generated before
reset
```

## Technical Principles

### Diagnosis

1. If one device's kernel version is NOT located in the range of vulnerable version, it MAY BE not vulnerable.
2. If one device's security-update-date is later than the patch-date of a vulnerability, it MAY BE not vulnerable.

Diagnosis is not reliable because of many elements. For a good & sarcastic example you can see the post [HOW ANDROID PHONES HIDE MISSED SECURITY UPDATES FROM YOU](https://www.wired.com/story/android-phones-hide-missed-security-updates-from-you/).

### Triggering

PoC tells us whether one device is vulnerable or not.

## Installation

### Python Modules

```bash
pip install -r requirements.txt
```

### ndk

You need to download ndk for your platform (Windows/Mac OS/Linux, etc.) and append the directory of `ndk-build` to `$PATH`.

### adb

You need to download adb and append the directory of `adb` to `$PATH`. 

## Demo

![demo.jpg](https://github.com/brant-ruan/IDF4APEV/blob/master/resources/images/demo.jpg)

## Extra

### Advantages of a Command Line Interface

- **portability** almost any computer is able to drive a text terminal, so a command line interface can really run everywhere.
- **resources** the CPU and memory cost of a command line interface is far lighter than a GUI library.
- **speed** for advanced users, it's often faster to type a command than to dive into menus and windows.
- **development** It is far faster to create a text oriented interface.
- **driving** you can easily drive a text oriented program with the popen command. That means that the whole application can be tested automatically.

## Acknowledgement

The banner is created with the help of *toilet*, which is a very interesting tool and can be installed through `brew install toilet` on Mac OSX :)
