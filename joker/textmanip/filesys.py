#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import os
import re


def keep_file_extension(old_path, new_path):
    _, old_ext = os.path.splitext(old_path)
    p, new_ext = os.path.splitext(new_path)
    if old_ext.lower() == new_ext.lower():
        return new_path
    return os.path.join(p, old_ext)


def human_filesize(number):
    """
    Human readable file size unit
    :param number: how many bytes
    :return: (num, unit)
    """
    units = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    for unit in units:
        if number < 10000 or unit == "YB":
            return number, unit
        else:
            number = number / 1024.0
            # to next loop, no return!


def url_to_filename(url):
    # http://stackoverflow.com/questions/295135/
    name = re.sub(r'[^\w\s-_.]+', '-', url)
    return re.sub(r'^{http|https|ftp}', '', name)

