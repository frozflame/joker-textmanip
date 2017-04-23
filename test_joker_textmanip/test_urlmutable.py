#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

from joker.textmanip.parse.url import URLMutable


def test_mutlink():
    s = 'https://www.youtube.com/results?search_query=buc'
    mlink = URLMutable(s)
    print(mlink)
    print(mlink.query)
    return mlink


def test_embed_link():
    h = 'https://github.com/'
    g = 'https://youtube.com/'
    k = 'embeded'
    urlmut = URLMutable(h)
    urlmut.embed_link(k, g)
    assert g == urlmut.unembed_link(k)


if __name__ == '__main__':
    lm = test_mutlink()
    test_mutlink()
