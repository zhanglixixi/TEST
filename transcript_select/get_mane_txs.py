#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

from __future__ import absolute_import, unicode_literals
import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(
        description='Get gene and transript information from mane.{version}.bed'
    )
    parser.add_argument('manebed', action='store',
                        help='MANE bed format, normally converted from bigbed by UCSC tool bigBedToBed')
    parser.add_argument('outfile', action='store', help='Output file name')
    return parser.parse_args()


def get_mane_transcripts(manebed):
    mane_entries = pd.read_csv(manebed, sep='\t', header=None, usecols=[18, 21], names=['gene', 'tx'])
    mane_entries['tx'] = mane_entries['tx'].apply(lambda x: x.split('.')[0])
    gene_txs0 = mane_entries.groupby(by='gene')['tx'].apply(list).reset_index(name='txs')
    gene_txs0['n_txs'] = gene_txs0['txs'].apply(lambda x: len(x))
    gene_txs = gene_txs0.sort_values(by='gene')[['gene', 'n_txs', 'txs']]
    gene_txs['label'] = 'MANE'

    gene_tx0 = gene_txs[gene_txs['n_txs'] == 1]
    gene_tx0['tx'] = gene_tx0['txs'].apply(lambda x: x[0])
    gene_tx = gene_tx0[['gene', 'tx', 'label']]

    print(gene_txs.groupby(by='n_txs').count()['gene'].reset_index(name='counts'))
    return gene_tx, gene_txs


def main():
    args = get_args()
    gene_tx, gene_txs = get_mane_transcripts(args.manebed)
    out_fns = ['{p}{s}'.format(p=args.outfile, s=s) for s in ['', '.details']]
    out_dfs = [gene_tx, gene_txs]
    outputs = dict(zip(out_fns, out_dfs))
    [df.to_csv(fn, sep='\t', header=False, index=False) for fn, df in outputs.items()]


if __name__ == '__main__':
    main()
