#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu
import argparse
import os
import sys


def get_args():
    parser = argparse.ArgumentParser(description='data backup fot mgi2k')
    subparsers = parser.add_subparsers(dest='command')
    stats = subparsers.add_parser('stats', help='stats of the md5sum check up results')
    stats.add_argument('-s', '--src_list', default=None, help='backup source list')
    stats.add_argument('md5sum', nargs='+', help='md5sum check result(s)')
    return parser.parse_args()


def get_src_files(src_list_file):
    all_files = {}
    with open(src_list_file, 'r') as fin:
        for line in fin:
            if not line or line.startswith('#'):
                continue
            src_path = line.strip('\n')
            fpaths = []
            for root, dirs, files in os.walk(src_path):
                for fname in files:
                    fpaths.append(os.path.join(root, fname).replace(src_path, '.'))
            all_files.update({src_path: fpaths})
    # [print(k, len(s)) for k, s in all_files.items()]
    return all_files


def get_md5sum_checks(infile):
    md5sum_checks = {}
    with open(infile, 'r') as fin:
        for line in fin:
            if not line or line.startswith('#'):
                continue
            fpath, ok = line.strip('\n').split(': ')
            md5sum_checks.update({fpath: True if ok == 'OK' else False})
    # [print(k, s) for k, s in md5sum_checks.items()]
    return md5sum_checks


def get_md5sum_stats(md5sum_checks, all_files=None):
    all_md5sum_checks = {}
    [all_md5sum_checks.update(mc) for mc in md5sum_checks]

    if all_files is None:
        print('N_files', 'N_OKs', sep='\t')
        n_files, n_oks = len(all_md5sum_checks), 0
        for fpath, c in all_md5sum_checks.items():
            n_oks += 1 if c else 0
        print(n_files, n_oks, sep='\t')

    else:
        print('Source', 'N_files', 'N_OKs', 'N_Fails', sep='\t')
        for src, files in all_files.items():
            n_files, n_oks = len(files), 0
            for fpath in files:
                if fpath not in all_md5sum_checks:
                    continue
                n_oks += 1 if all_md5sum_checks[fpath] else 0
            print(src, n_files, n_oks, n_files - n_oks, sep='\t')


def main():
    args = get_args()
    if args.command == 'stats':
        all_files = None if args.src_list is None else get_src_files(args.src_list)
        md5sum_checks = [get_md5sum_checks(md5_fp) for md5_fp in args.md5sum]
        get_md5sum_stats(md5sum_checks, all_files)


if __name__ == '__main__':
    main()
