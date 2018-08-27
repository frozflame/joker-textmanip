#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import datetime
import sys

# http://www.garykessler.net/library/base64.html
from joker.textmanip.path import ext_join


def text_routine_catstyle(func):
    # routine function for quick and dirty text manipulation scripts
    if not sys.argv[1:]:
        for line in sys.stdin:
            print(func(line))
        return
    for path in sys.argv[1:]:
        for line in open(path):
            print(func(line))


def text_routine_perfile(func, ext=None):
    # routine function for quick and dirty text manipulation scripts
    if ext is None:
        ext = '.out-{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())

    for path in sys.argv[1:]:
        outpath = ext_join(path, ext)
        func(path, outpath)
