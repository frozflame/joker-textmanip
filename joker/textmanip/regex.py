#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import re

from joker.textmanip.align import commonprefix, commonsuffix


def infer_affix_pattern(strings):
    strings = list(set(x or '' for x in strings))
    if not strings:
        return '.*'

    if len(strings) == 1:
        return re.escape(list(strings)[0])

    prefix = commonprefix(strings)
    suffix = commonsuffix(strings)
    a = len(prefix)
    b = - len(suffix) or None
    strings = [x[a:b] for x in strings]

    minlen = min(len(x) for x in strings)
    maxlen = max(len(x) for x in strings)

    strings = [re.escape(x) for x in strings if x]
    strings.sort()

    if maxlen == 1:
        if len(strings) == 1:
            ptn = strings[0]
        else:
            ptn = '[{}]'.format(''.join(strings))
    else:
        ptn = '|'.join(strings)
        ptn = '(?:{})'.format(ptn)

    if minlen == 0:
        ptn += '?'
    return re.escape(prefix) + ptn + re.escape(suffix)


build_pattern = infer_affix_pattern


def make_range_pattern(blocks):
    """
    >>> blocks = [(48, 50), 65]
    >>> make_range_pattern(blocks)
    '0-2A'
    """
    parts = []
    for tuple_or_int in blocks:
        if isinstance(tuple_or_int, tuple):
            p = '{}-{}'.format(*map(chr, tuple_or_int[:2]))
            parts.append(p)
        else:
            parts.append(chr(tuple_or_int))
    return ''.join(parts)


cjk_blocks = [
    (0x2E80, 0x2EFF, "CJK Radicals Supplement"),
    (0x3000, 0x303F, "CJK Symbols & Punctuation"),
    (0x31C0, 0x31EF, "CJK Strokes"),
    (0x3200, 0x32FF, "CJK Enclosed Letters and Months"),
    (0x3300, 0x33FF, "CJK Compatibility"),
    (0x3400, 0x4DBF, "CJK Unified Ideographs Extension A"),
    (0x4E00, 0x9FFF, "CJK Unified Ideographs"),
    (0xF900, 0xFAFF, "CJK Compatibility Ideographs"),
    (0xFE30, 0xFE4F, "CJK Compatibility Forms"),
]


def remove_cjk(text):
    cjk = make_range_pattern(cjk_blocks)
    return re.sub('[{}]'.format(cjk), '', text)


def remove_spaces_beside_cjk(text):
    cjk = make_range_pattern(cjk_blocks)
    parts = re.split(r'\s*([{}]+)\s*'.format(cjk), text)
    return ''.join(parts)


def remove_spaces_between_cjk(text):
    cjk = make_range_pattern(cjk_blocks)
    return re.sub(r'([{0}]+)\s+(?=[{0}])'.format(cjk), r'\1', text)
