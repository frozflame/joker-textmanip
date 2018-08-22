# !/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os
import re


def url_to_filename(url):
    # http://stackoverflow.com/questions/295135/
    name = re.sub(r'[^\w\s_.-]+', '-', url)
    return re.sub(r'^{http|https|ftp}', '', name)


def ext_join(path, ext):
    """
    >>> smart_extension_join('~/html/index.txt', 'html')
    '~/html/index.html'
    >>> smart_extension_join('~/html/index.txt', '.html')
    '~/html/index.txt.html'

    :param path: (str)
    :param ext: (str)
    :return:
    """
    if ext.startswith(os.path.extsep):
        return path + ext
    p, _ = os.path.splitext(path)
    return p + os.path.extsep + ext


smart_extension_join = ext_join
