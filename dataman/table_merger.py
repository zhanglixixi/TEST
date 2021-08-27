#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

from __future__ import absolute_import, unicode_literals
import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(description='merge tables according to input list')
    parser.add_argument('in_list', action='store',
                        help='input table lisit, lable and table path, tab separated')
    parser.add_argument('outfile', action='store',
                        help='output file')
    return parser.parse_args()


def merge_tables(infile, outfile):
    data1 = []
    with open(infile, 'r') as fin:
        for line in fin:
            if not line or line.startswith('#'):
                continue
            label, fpath = line[:-1].split('\t')
            print(label)
            data0 = pd.read_csv(fpath, sep='\t', header=0, index_col=None)
            data0.insert(0, 'Label', label)
            data1.append(data0)
    data = pd.concat(data1)
    data.to_csv(outfile, sep='\t', header=True, index=False)


def main():
    args = get_args()
    merge_tables(args.in_list, args.outfile)


if __name__ == '__main__':
    main()
