# !/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os
import re


def url_to_filename(url):
    # http://stackoverflow.com/questions/295135/
    name = re.sub(r'[^\w\s_.-]+', '-', url)
    return re.sub(r'^{http|https|ftp}', '', name)


def keep_extension(old_path, new_path):
    _, old_ext = os.path.splitext(old_path)
    p, new_ext = os.path.splitext(new_path)
    if old_ext.lower() == new_ext.lower():
        return new_path
    return os.path.join(p, old_ext)


def replace_extension(path, ext):
    p, _ = os.path.splitext(path)
    return os.path.join(p, ext)
