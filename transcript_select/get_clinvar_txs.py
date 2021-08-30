#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

from __future__ import absolute_import, unicode_literals
import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(
        description='Get gene and transript information from variant_summary.txt(.gz).'
    )
    parser.add_argument('variant_summary', action='store',
                        help='ClinVar variant summary, variant_summary.txt(.gz)')
    parser.add_argument('outfile', action='store', help='Output file name')
    return parser.parse_args()


def get_clinvar_transcripts(variant_summary_file):
    var_info = pd.read_csv(
        variant_summary_file, sep='\t', header=0, dtype={'Chromosome': str},  # nrows=10000,
        usecols=['Type', 'Name', 'GeneID', 'GeneSymbol', 'Assembly', 'Chromosome', 'ReviewStatus', 'NumberSubmitters']
    )
    var_info['Transcript'] = var_info.Name.apply(lambda x: x.split('.')[0])

    # input data wash
    var_info = var_info[(var_info['Type'] == 'single nucleotide variant')
                        & (var_info['GeneID'] != -1)
                        & (var_info['Assembly'] == 'GRCh37')
                        & (var_info['Name'].str.startswith('N'))]

    gene_tx_counts = var_info.groupby(by=['GeneSymbol', 'Transcript']).count()['Name'].reset_index(name='counts')
    gene_tx_counts.sort_values(by=['GeneSymbol', 'counts'], inplace=True)

    gene_txs0 = gene_tx_counts.drop_duplicates(subset=['GeneSymbol'], keep='last')[['GeneSymbol', 'Transcript']]
    gene_txs0['txs'] = gene_txs0['Transcript'].apply(lambda x: [x])
    gene_txs0['n_txs'] = gene_txs0['txs'].apply(lambda x: len(x))
    gene_txs = gene_txs0[['GeneSymbol', 'n_txs', 'txs']]
    gene_txs['label'] = 'ClinVar'

    gene_tx0 = gene_txs[gene_txs['n_txs'] == 1]
    gene_tx0['tx'] = gene_tx0['txs'].apply(lambda x: x[0])
    gene_tx = gene_tx0[['GeneSymbol', 'tx', 'label']]
    print(gene_txs.groupby(by='n_txs').count()['GeneSymbol'].reset_index(name='counts'))
    return gene_tx, gene_txs, gene_tx_counts


def main():
    args = get_args()
    gene_tx, gene_txs, gene_tx_counts = get_clinvar_transcripts(args.variant_summary)
    out_fns = ['{p}{s}'.format(p=args.outfile, s=s) for s in ['', '.details', '.counts']]
    out_dfs = [gene_tx, gene_txs, gene_tx_counts]
    outputs = dict(zip(out_fns, out_dfs))
    [df.to_csv(fn, sep='\t', header=False, index=False) for fn, df in outputs.items()]


if __name__ == '__main__':
    main()
