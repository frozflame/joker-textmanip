#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

from joker.textmanip.align import (
    find_common_prefix,
    find_common_suffix
)


def test_find_common_fix():
    assert find_common_prefix([]) == ''
    assert find_common_prefix(['']) == ''
    assert find_common_prefix(['a']) == 'a'
    assert find_common_prefix(['', '']) == ''
    assert find_common_prefix(['a', 'ab']) == 'a'

    assert find_common_suffix([]) == ''
    assert find_common_suffix(['']) == ''
    assert find_common_suffix(['a']) == 'a'
    assert find_common_suffix(['', '']) == ''
    assert find_common_suffix(['a', 'ba']) == 'a'
