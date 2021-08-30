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
        description='Get canonical transripts from UCSC known canonical.'
    )
    parser.add_argument('kctx', action='store',
                        help='UCSC known canonical, knownCanonical.txt(.gz)')
    parser.add_argument('kgxref', action='store',
                        help='UCSC known gene cross reference, kgXref.txt(.gz)')
    parser.add_argument('outfile', action='store', help='Output file name')
    return parser.parse_args()


def get_known_canonical_transcripts(kc_tx_file, kg_xref_file):
    chrs = chromosome_list(fix_chr=True)

    kg_xref = pd.read_csv(
        kg_xref_file, sep='\t', header=None, usecols=[i for i in range(0, 8)],
        names=['kg_id', 'mRNA', 'sp_id', 'sp_display_id', 'gene_symbol', 'refseq', 'prot_acc', 'description']
    )
    # print('\nBasic description statistics of kgXref:\n', kg_xref.describe(), '\n')

    kc_tx = pd.read_csv(
        kc_tx_file, sep='\t', header=None, usecols=[i for i in range(0, 6)],
        names=['chrom', 'start', 'end', 'cluster_id', 'transcript', 'protein']
    )

    kc_tx_exclude_alts = kc_tx[kc_tx.chrom.isin(chrs)]
    canonical_tx_ids = list(kc_tx_exclude_alts.transcript)
    kg_kc_valid_records = kg_xref[kg_xref.kg_id.isin(canonical_tx_ids)].dropna(axis=0, subset=['gene_symbol', 'refseq'])

    gene_txs0 = kg_kc_valid_records.groupby(by='gene_symbol')['refseq'].apply(list).reset_index(name='txs')
    gene_txs0['txs'] = gene_txs0['txs'].apply(lambda x: list(set(x)))
    gene_txs0['n_txs'] = gene_txs0['txs'].apply(lambda x: len(x))
    gene_txs = gene_txs0.sort_values(by='gene_symbol')[['gene_symbol', 'n_txs', 'txs']]
    gene_txs['label'] = 'UCSC_kckg'
    print(gene_txs0.groupby(by='n_txs').count()['gene_symbol'].reset_index(name='counts'))

    gene_tx0 = gene_txs[gene_txs['n_txs'] == 1]
    gene_tx0['tx'] = gene_tx0['txs'].apply(lambda x: x[0])
    gene_tx = gene_tx0[['gene_symbol', 'tx', 'label']]
    return gene_tx, gene_txs


def main():
    args = get_args()
    gene_tx, gene_txs = get_known_canonical_transcripts(args.kctx, args.kgxref)
    out_fns = ['{p}{s}'.format(p=args.outfile, s=s) for s in ['', '.details']]
    out_dfs = [gene_tx, gene_txs]
    outputs = dict(zip(out_fns, out_dfs))
    [df.to_csv(fn, sep='\t', header=False, index=False) for fn, df in outputs.items()]


if __name__ == '__main__':
    main()
