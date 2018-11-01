#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import re
from collections import deque

chsi_digits = '零一二三四五六七八九'

chtr_digits = '零壹贰叁肆伍陆柒捌玖'

punctuations = [
    ('(', '\uff08'),
    (')', '\uff09'),
    ('.', '\u3002'),
    (',', '\uff0c'),
]


def _repdiv(num, divisor):
    results = []
    while num:
        d, m = divmod(num, divisor)
        results.append(m)
        num = d
    return results


def i2ch_lt10k(num, digits, units):
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


def i2chsi(num, digits, units):
    num = int(num)
    if num < 10:
        return digits[num]
    if num == 10:
        return units[1]
    if num < 20:
        return units[1] + digits[num % 10]
    parts = deque()
    for u8, n8 in enumerate(_repdiv(num, 10 ** 8)):
        if u8:
            parts.appendleft(units[5])
        for u4, n4 in enumerate(_repdiv(n8, 10 ** 4)):
            if u4:
                parts.appendleft(units[4])
            ch = i2ch_lt10k(n4, digits, units)
            parts.appendleft(ch)
    return ''.join(parts)


def integer_to_chsi(num):
    """Simplified characters used in mainland China"""
    return i2chsi(num, chsi_digits, ['', '十', '百', '千', '万', '亿'])


def integer_to_chsicap(num):
    """Tamper-safe characters used in mainland China"""
    return i2chsi(num, chtr_digits, ['', '拾', '佰', '仟', '万', '亿'])


def chinese_to_integer():
    raise NotImplementedError


_map_chsi_0110 = {
    '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
    '六': '6', '七': '7', '八': '8', '九': '9', '十': '10',
}

_map_chsi_1120 = {
    '十一': '11', '十二': '12', '十三': '13', '十四': '14', '十五': '15',
    '十六': '16', '十七': '17', '十八': '18', '十九': '19', '二十': '20',
}


def replace_small_chsi_with_decimal(s):
    regex = re.compile(r'[一二三四五六七八九十]+', re.UNICODE)
    for _map in [_map_chsi_1120, _map_chsi_0110]:
        s = regex.sub(lambda m: _map[m.group()], s)
    return s


def replace_small_decimal_with_chsi(s):
    regex = re.compile(r'\d+')
    return regex.sub(lambda m: integer_to_chsi(m.group()), s)
