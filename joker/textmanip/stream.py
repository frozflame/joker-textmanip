#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import io
import os
import sys
import time
import weakref


def _iter_lines(path, *args, **kwargs):
    with open(path, *args, **kwargs) as fin:
        for line in fin:
            yield line


def _iter_stdin_lines():
    for line in sys.stdin:
        yield line


def iter_lines(path, *args, **kwargs):
    if not path or path in ['-', 'stdin', '/dev/stdin']:
        return _iter_stdin_lines()
    else:
        return _iter_lines(path, *args, **kwargs)


def nonblank_lines_of(path, *args, **kwargs):
    for line in iter_lines(path, *args, **kwargs):
        line = line.strip()
        if not line:
            continue
        yield line


def _write_lines(lines, path, mode='w', *args, **kwargs):
    with open(path, mode, *args, **kwargs) as fout:
        fout.writelines(lines)


def _write_stdout_lines(lines, target=sys.stdout):
    for line in lines:
        target.write(line)
    target.flush()


def write_lines(lines, path, mode='w', *args, **kwargs):
    if not path or path in ['-', 'stdout', '/dev/stdout']:
        _write_stdout_lines(lines)
    elif path in ['stderr', '/dev/stderr']:
        _write_stdout_lines(lines, sys.stderr)
    else:
        _write_lines(lines, path, mode, *args, **kwargs)


class Stream(object):
    __slots__ = ['file']
    opened = weakref.WeakValueDictionary()
    _preopened = {
        (1, 'w'): sys.stdout,
        (2, 'w'): sys.stderr,
        ('', 'r'): sys.stdin,
        ('', 'w'): sys.stdout,
        ('-', 'r'): sys.stdin,
        ('-', 'w'): sys.stdout,
        ('<stdin>', 'r'): sys.stdin,
        ('<stdout>', 'w'): sys.stdout,
        ('<stderr>', 'w'): sys.stderr,
    }
    _safe_attributes = {'mode', 'name'}

    @classmethod
    def open(cls, file, mode='r', *args, **kwargs):
        k = file, mode
        f = cls._preopened.get(k)
        if f is None:
            f = open(file, mode, *args, **kwargs)
            cls.opened[id(f)] = f
        return cls(f)

    @classmethod
    def wrap(cls, content):
        if isinstance(content, str):
            return cls(io.StringIO(content))
        if isinstance(content, bytes):
            return cls(io.BytesIO(content))
        return cls(io.StringIO(str(content)))

    def __init__(self, file):
        self.file = file

    def __iter__(self):
        return iter(self.file)

    def __getattr__(self, name):
        if name in self._safe_attributes:
            return getattr(self.file, name, None)
        return getattr(self.file, name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if id(self.file) in self.opened:
            self.file.__exit__(exc_type, exc_val, exc_tb)

    def is_binary(self):
        if self.mode:
            return 'b' in self.mode
        try:
            return isinstance(self.file.read(0), bytes)
        except Exception:
            pass


class ShellStream(Stream):
    def lines(self):
        for line in self.file:
            yield line.strip()

    def nonblank_lines(self):
        for line in self.file:
            line = line.strip()
            if line:
                yield line

    def ungrep(self, pattern, flags=0):
        import re
        for line in self.file:
            if re.search(pattern, line, flags) is None:
                yield line

    def grep(self, pattern, flags=0, group=None):
        import re
        for line in self.file:
            mat = re.search(pattern, line, flags)
            if mat is None:
                continue
            if group is None:
                yield line
            else:
                yield mat.group(group)

    def quote(self, strip=False):
        import shlex
        if self.is_binary():
            raise TypeError('file should be opened in text mode')
        if strip in ('l', 'r'):
            func = getattr(str, str(strip) + 'strip')
            lines = (func(line) for line in self.file)
        elif strip:
            lines = (line.strip() for line in self.file)
        else:
            lines = (line.rstrip('\n') for line in self.file)
        for line in lines:
            yield shlex.quote(line)


class AtomicTailer(object):
    """
    Read log file on-line
    inspired by https://github.com/six8/pytailer

    a minimized version with this issue fixed:
        https://github.com/six8/pytailer/issues/9
    """

    def __init__(self, file, read_size=1024, interval=1.,
                 linesep=None, timeout=60):

        if isinstance(file, str):
            self.file = open(file)
        else:
            self.file = file

        self.read_size = read_size
        self.start_pos = self.file.tell()
        self.interval = interval
        self.linesep = linesep or os.linesep
        self.timeout = timeout

    def __iter__(self):
        return self.follow()

    def follow(self):
        """\
        follow a growing file
        tldr: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157035
        """
        tm = time.time()
        while True:
            pos = self.file.tell()
            line = self.file.readline()
            if line.endswith(self.linesep):
                tm = time.time()
                yield line
            else:
                if time.time() - tm > self.timeout:
                    if line:
                        yield line
                    break
                self.file.seek(pos)
                time.sleep(self.interval)

    def follow_lines(self, limit=1000):
        tm = time.time()
        lines = []
        while True:
            if len(lines) >= limit:
                yield lines
                lines = []
            pos = self.file.tell()
            line = self.file.readline()
            if line.endswith(self.linesep):
                tm = time.time()
                lines.append(line)
            else:
                if time.time() - tm > self.timeout:
                    if line:
                        lines.append(line)
                    if lines:
                        yield lines
                    break
                self.file.seek(pos)
                time.sleep(self.interval)
