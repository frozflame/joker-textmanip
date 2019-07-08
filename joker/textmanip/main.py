#!/usr/bin/env python3
# coding: utf-8

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
    rows = tabular.textfile_to_list(args[0])
    for row in tabular.tabular_format(rows):
        pass
        print(*row)


def total(_, args):
    from joker.textmanip.tabular import textfile_numsum
    textfile_numsum(_chkargs(args), printout=True)


entries = {
    'joker.textmanip.main:total': '+',
    'joker.textmanip.main:vprint_tab': 'tab',
    'joker.textmanip.main:pprint_dict': 'd',
    'joker.textmanip.main:pprint_dictswap': 'ds',
    'joker.textmanip.main:pprint_list': 'l',
    'joker.textmanip.main:pprint_list2d': 'L',
}


registry = CommandRegistry(entries)

if __name__ == '__main__':
    registry()
