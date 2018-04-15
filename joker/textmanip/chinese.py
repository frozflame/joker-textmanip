#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import re
from collections import deque

chsi_digits = '零一二三四五六七八九'

chtr_digits = '零壹贰叁肆伍陆柒捌玖'


def _repdiv(num, divisor):
    results = []
    while num:
        d, m = divmod(num, divisor)
        results.append(m)
        num = d
    return results


def i2ch(num, digits, units):
    parts = deque()
    for u, n in enumerate(_repdiv(num, 10)):
        if n:
            parts.appendleft(units[u])
        parts.appendleft(digits[n])
    ch = ''.join(parts)
    ch = re.sub(r'零+$', '', ch, flags=re.UNICODE)
    ch = re.sub(r'零{2,}', '零', ch, flags=re.UNICODE)
    ch = re.sub(r'\s+', '', ch, flags=re.UNICODE)
    return ch


def integer_to_chsi(num):
    parts = deque()
    for u8, n8 in enumerate(_repdiv(num, 10 ** 8)):
        if u8:
            parts.appendleft('亿')
        for u4, n4 in enumerate(_repdiv(n8, 10 ** 4)):
            if u4:
                parts.appendleft('万')
            ch = i2ch(n4, chsi_digits, ['', '十', '百', '千'])
            parts.appendleft(ch)
    return ''.join(parts)


def integer_to_chtr():
    pass


def chinese_to_integer():
    pass
