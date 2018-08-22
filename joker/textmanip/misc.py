#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import datetime
import random
import sys
from string import digits, ascii_letters, ascii_uppercase

# http://www.garykessler.net/library/base64.html
from joker.textmanip.path import smart_extension_join

b64_chars = digits + ascii_letters + '+/'
b64_urlsafe_chars = ascii_letters + digits + '_-'
b32_chars = ascii_uppercase + '234567'


def random_string(length, chars=None):
    if not chars:
        chars = digits + ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))


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
        ext = '.out_{}'.format(datetime.datetime.now())

    for path in sys.argv[1:]:
        outpath = smart_extension_join(path, ext)
        func(path, outpath)
