#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

from joker.textmanip.regex import (
    remove_cjk, remove_spaces_beside_cjk, remove_spaces_between_cjk)


def rp(o):
    print(repr(o))


def test_cjk_remove():
    s = " democracy 德 先生 science 赛 先生 "
    t = " democracy   science   "
    r = remove_cjk(s)
    assert t == r, rp(r)

    s = " democracy 德 先生 science 赛 先生 "
    t = " democracy德先生science赛先生"
    r = remove_spaces_beside_cjk(s)
    assert t == r, rp(r)

    s = " democracy 德 先生 science 赛 先生 "
    t = " democracy 德先生 science 赛先生 "
    r = remove_spaces_between_cjk(s)
    assert t == r, rp(r)


if __name__ == '__main__':
    test_cjk_remove()
