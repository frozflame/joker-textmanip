#!/usr/bin/env python3
# coding: utf-8

import argparse
import sys

from volkanic.system import CommandRegistry


def _chkargs(args):
    if not args:
        return '-'
    if len(args) > 1:
        sys.exit('error: too many arguments')
    return args[0]


def pprint_dict(_, args):
    from joker.textmanip.tabular import textfile_to_dict
    textfile_to_dict(_chkargs(args), printout=True)


def pprint_dictswap(_, args):
    from joker.textmanip.tabular import textfile_to_dict
    textfile_to_dict(_chkargs(args), printout=True, swap=True)


def pprint_list2d(_, args):
    from joker.textmanip.tabular import textfile_to_list
    textfile_to_list(_chkargs(args), printout=True)


def pprint_list(_, args):
    import pprint
    from joker.textmanip.stream import nonblank_lines_of
    lines = list(nonblank_lines_of(_chkargs(args)))
    pprint.pprint(lines)


def vprint_tab(_, args):
    from joker.textmanip import tabular
    rows = tabular.textfile_to_list(_chkargs(args))
    for row in tabular.tabular_format(rows):
        pass
        print(*row)


def total(_, args):
    from joker.textmanip.tabular import textfile_numsum
    textfile_numsum(_chkargs(args), printout=True)


def grep(_, args):
    import re
    from joker.textmanip.stream import nonblank_lines_of
    try:
        pattern = args[0]
    except IndexError:
        return
    regex = re.compile(pattern)
    idx = 1 if regex.groups == 1 else 0
    for line in nonblank_lines_of(_chkargs(args[1:])):
        mat = regex.search(line)
        if mat:
            print(mat.group(idx))


def _newline_conv(path, nl, suffix):
    with open(path) as fin, open(path + suffix, 'w', newline=nl) as fout:
        for line in fin:
            fout.write(line)


def nlconv(prog, args):
    desc = 'convert newlines'
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('-s', '--style', choices=['n', 'rn', 'r'])
    parser.add_argument('path', help='an input data file')
    ns = parser.parse_args(args)
    newlines = {'n': '\n', 'rn': '\r\n', 'r': '\r'}
    suffix = '.{}.txt'.format(ns.style)
    _newline_conv(ns.path, newlines.get(ns.style), suffix)


def urlsim(prog, args):
    from joker.textmanip.url import url_simplify
    desc = 'simplify a url'
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    aa = parser.add_argument
    parser.add_argument('-q', '--quote', action='store_true')
    parser.add_argument('url')
    parser.add_argument('query', nargs='*')
    ns = parser.parse_args(args)
    url = str(url_simplify(ns.url, ns.query))
    if ns.quote:
        import shlex
        url = shlex.quote(url)
    print(url)


entries = {
    'joker.textmanip.main:grep': '/',
    'joker.textmanip.main:total': '+',
    'joker.textmanip.main:nlconv': 'nl',
    'joker.textmanip.main:vprint_tab': 'tab',
    'joker.textmanip.main:pprint_list': 'l',
    'joker.textmanip.main:pprint_list2d': 'L',
    'joker.textmanip.main:pprint_dict': 'd',
    'joker.textmanip.main:pprint_dictswap': 'ds',
    'joker.textmanip.main:urlsim': 'urlsim',
    'joker.textmanip.draw:mkbox': 'box',
}

registry = CommandRegistry(entries)

if __name__ == '__main__':
    registry()
