#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals


from joker.textmanip.chinese import integer_to_chsi


def test_integer_to_chsi():
    assert integer_to_chsi(127000) == '一十二万七千'
    assert integer_to_chsi(127001) == '一十二万七千零一'
    assert integer_to_chsi(2127000127000) == '二万一千二百七十亿一十二万七千'
