#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import datetime
import sys

from joker.textmanip.path import smart_extension_join

"""
routine functions for quick n' dirty text manipulation scripts
"""


def text_routine_catstyle(func):
    if not sys.argv[1:]:
        for line in sys.stdin:
            print(func(line))
        return
    for path in sys.argv[1:]:
        for line in open(path):
            print(func(line))


def text_routine_perfile(func, ext=None):
    """
    If suffix None, append an auto-gen suffix
    If suffix
    :param func:
    :param ext:
    :return:
    """
    if ext is None:
        ext = '.out_{}'.format(datetime.datetime.now())

    for path in sys.argv[1:]:
        outpath = smart_extension_join(path, ext)
        func(path, outpath)

