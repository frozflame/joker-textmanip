#!/usr/bin/env python3
# coding: utf-8

__version__ = '0.0.6'

b64_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/'

b64_urlsafe_chars = \
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'

b32_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'


def random_string(length, chars=None):
    import random
    chars = chars or b32_chars
    return ''.join(random.choice(chars) for _ in range(length))


def remove_chars(s, chars):
    """
    :param s: (str)
    :param chars: (str or list) characters to be removed
    :return: (str)
    """
    return s.translate(dict.fromkeys(ord(c) for c in chars))


def remove_control_chars(s):
    return s.translate(dict.fromkeys(range(32)))


def remove_whitespaces(s):
    return ''.join(s.split())


def remove_newlines(s):
    return ' '.join(s.splitlines())
