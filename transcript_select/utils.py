#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

from __future__ import absolute_import, unicode_literals


def content_line(fin):
    for line in fin:
        line = line.rstrip('\n')
        if not line:
            continue
        if line.startswith('#'):
            continue
        yield line


def chromosome_list(fix_chr=False):
    chrs = ['chr{c}'.format(c=i+1) for i in range(0, 22)] if fix_chr else ['{c}'.format(c=i+1) for i in range(0, 22)]
    chrs += ['chrX', 'chrY'] if fix_chr else ['X', 'Y']
    return chrs


def main():
    pass


if __name__ == '__main__':
    main()
