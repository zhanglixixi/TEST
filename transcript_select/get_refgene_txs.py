#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

from __future__ import absolute_import, unicode_literals
import argparse
import pandas as pd
from utils import chromosome_list


def get_args():
    parser = argparse.ArgumentParser(
        description='Get gene and transript information from refGene.txt(.gz).'
    )
    parser.add_argument('refgene', action='store',
                        help='UCSC refgene file, refGene.txt(.gz)')
    parser.add_argument('outfile', action='store', help='Output file')
    return parser.parse_args()


def get_refgene_transcripts(refgene_file):
    chrs = chromosome_list(fix_chr=True)
    refgenes = pd.read_csv(refgene_file, sep='\t', header=None, usecols=[1, 2, 8, 12],
                           names=['tx', 'chrom', 'n_exons', 'gene'])

    refgenes_exclude_alts = refgenes[refgenes.chrom.isin(chrs)]
    refgenes_exclude_alts_sorted = refgenes_exclude_alts.sort_values(by=['gene', 'n_exons'])
    gene_txs0 = refgenes_exclude_alts_sorted.groupby(by='gene')['tx'].apply(list).reset_index(name='txs')
    gene_txs0['n_txs'] = gene_txs0['txs'].apply(lambda x: len(x))
    gene_txs = gene_txs0.sort_values(by='gene')[['gene', 'n_txs', 'txs']]
    gene_txs['label'] = 'UCSC_refGene'

    gene_tx0 = refgenes_exclude_alts_sorted.drop_duplicates(subset=['gene'], keep='last')
    gene_tx = gene_tx0[['gene', 'tx']]
    gene_tx['label'] = 'UCSC_refGene'

    print(gene_txs0.groupby(by='n_txs').count()['gene'].reset_index(name='counts'))
    print(gene_tx.groupby(by='gene').count().reset_index().groupby(by='tx').count()['gene'].reset_index(name='counts'))
    return gene_tx, gene_txs


def main():
    args = get_args()
    gene_tx, gene_txs = get_refgene_transcripts(args.refgene)
    out_fns = ['{p}{s}'.format(p=args.outfile, s=s) for s in ['', '.details']]
    out_dfs = [gene_tx, gene_txs]
    outputs = dict(zip(out_fns, out_dfs))
    [df.to_csv(fn, sep='\t', header=False, index=False) for fn, df in outputs.items()]


if __name__ == '__main__':
    main()
