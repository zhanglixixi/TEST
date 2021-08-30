#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

from __future__ import absolute_import, unicode_literals
import argparse
import pandas as pd
import os


def get_args():
    parser = argparse.ArgumentParser(
        description='To select transcript as canonical from mulitiple inputs'
    )
    parser.add_argument('output', action='store', help='Output file name')
    parser.add_argument('inputs', nargs='+', help='Input file(s). Priority decrease from first to last given file')
    # parser.add_argument('--genelist', action='store', default=None,
    #                     help='Process gene list in this file only')
    return parser.parse_args()


def _select_transcript(inputs):
    gn_tx_selected = {}
    inputs.reverse()
    for infile in inputs:
        gn_tx = pd.read_csv(infile, sep='\t', header=None, index_col=None)
        gn_tx_dict = dict(zip(gn_tx[0], gn_tx[1]))
        gn_tx_selected.update(gn_tx_dict)
        print('{n1} records in total, after merging {n2} records from {f}'.format(
            n1=len(gn_tx_selected), n2=len(gn_tx_dict), f=infile))
    return gn_tx_selected


def get_gene_list(infile):
    genes = list(pd.read_csv(infile, sep='\t', header=None, index_col=0, usecols=[0]).index)
    return dict(zip(genes, [None] * len(genes)))


def output_gn_tx(outfile, gn_tx, genes=None):
    with open(outfile, 'w') as fout:
        if genes is None:
            [fout.write('{gn}\t{tx}\n'.format(gn=k, tx=v)) for k, v in gn_tx.items()]
        else:
            genes.update((k, gn_tx[k]) for k in set(gn_tx).intersection(genes))
            [fout.write('{gn}\t{tx}\n'.format(gn=k, tx=v)) for k, v in genes.items()]


def select_trascript(infiles):
    priority = 0
    gn_tx_all = pd.DataFrame()
    for infile in infiles:
        priority += 1
        gn_tx_label = pd.read_csv(infile, sep='\t', header=None, index_col=None, names=['gene', 'tx', 'label'])
        gn_tx_label['priority'] = priority
        gn_tx_all = pd.concat([gn_tx_all, gn_tx_label])

    gn_tx_all.sort_values(by=['gene', 'priority'])
    gn_tx_select = gn_tx_all.drop_duplicates(subset='gene', keep='first')
    gn_tx_details = gn_tx_all.groupby(by='gene').aggregate(list).reset_index()
    return gn_tx_select, gn_tx_details


def main():
    args = get_args()

    print('Priority oder is:')
    [print('{n}: {f}'.format(n=i+1, f=args.inputs[i])) for i in range(0, len(args.inputs))]

    gn_tx_select, gn_tx_details = select_trascript(args.inputs)

    out_fns = ['{p}{s}'.format(p=args.output, s=s) for s in ['', '.details']]
    out_dfs = [gn_tx_select, gn_tx_details]
    outputs = dict(zip(out_fns, out_dfs))
    [df.to_csv(fn, sep='\t', header=False, index=False) for fn, df in outputs.items()]


if __name__ == '__main__':
    main()
