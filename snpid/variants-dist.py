#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

import pandas as pd
import argparse
import os
import sys
from pathlib import Path
__version__ = '0.2.0'


def output_results(distances, outfile):
    Path(os.path.dirname(outfile)).mkdir(parents=True, exist_ok=True)
    with open(outfile, 'w') as fout:
        [fout.write('{key}\t{value}\n'.format(key=k, value=v)) for k, v in distances.items()]


def get_args():
    parser = argparse.ArgumentParser(
        prog='variants-dist.py',
        description='Compute distance matrix for given variants. Version: {}'.format(__version__))
    parser.add_argument('-l', '--filelist', required=True,
                        help='File list of SNPs (bed intersect with vcf), label filepath, tab separated')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    args = parser.parse_args()
    return args


def get_filelist(infile):
    labeled_filsts = {}
    with open(infile) as fin:
        for line in fin:
            if len(line) == 0:
                continue
            label, filepath = line.split('\t')
            labeled_filsts.update({label.strip(): filepath.strip()})
    return labeled_filsts


def get_snp_genotype(label, infile):
    snpinfo = pd.read_csv(infile, sep='\t', header=None, dtype=str, usecols=[0,1,2,7,8,11,13])
    headers = {0:'Chr', 1:'Start', 2:'End', 7:'Ref', 8:'Alt', 11:'Info', 13:'GT'}
    snpinfo.rename(headers, axis=1, inplace=True)

    def determine_gt(row):
        if row['Info'] == '.':
            return '..'
        else:
            infolist = row['Info'].split(';')
            infodict = {}
            for infofield in infolist:
                if '=' not in infofield:
                    continue
                k, v = infofield.split('=')
                infodict.update({k: v})
            if float(infodict['AF']) == 1.0:
                return '{a1}{a2}'.format(a1=row['Alt'], a2=row['Alt'])
            elif float(infodict['AF']) == 0.5:
                return '{a1}{a2}'.format(a1=row['Ref'], a2=row['Alt'])
            else:
                sys.exit('Unexpected AF values')

    snpinfo[label] = snpinfo.apply(lambda row: determine_gt(row), axis=1)
    snpinfo.set_index(['Chr', 'Start', 'End'], inplace=True)
    snpinfo1 = pd.DataFrame(snpinfo[label])
    return snpinfo1


def genotype_distance(labeled_files):
    first_label = list(labeled_files.keys())[0]
    first_file = list(labeled_files.values())[0]
    genotypes = get_snp_genotype(first_label, first_file)
    genotypes.drop([first_label], axis=1, inplace=True)
    for label, filepath in labeled_files.items():
        genotype = get_snp_genotype(label, filepath)
        genotypes = genotypes.join(genotype)
    print(genotypes)

    def distance(genotype_two_lables):
        def difference(row):
            diff = 0
            two_labels = list(genotype_two_lables.columns)
            for n in [0, 1]:
                if row[two_labels[0]][n] != row[two_labels[1]][n]:
                    diff += 1
            return diff
        genotype_two_lables['Diff'] = genotype_two_lables.apply(lambda row: difference(row), axis=1)
        ddist = int(genotype_two_lables['Diff'].sum(axis=0))
        return ddist

    lables = list(genotypes.columns)
    nlables = len(lables)
    distances = {}
    for ith in range(0, nlables, 1):
        print(' {ith} / {nlabels} - {label1}'.format(ith=ith+1, nlabels=nlables, label1=lables[ith]))
        for jth in range(ith+1, nlables, 1):
            genotype_two_labels = genotypes[[lables[ith], lables[jth]]]
            dist = distance(genotype_two_labels)
            distances.update({'{label1} - {label2}'.format(label1=lables[ith], label2=lables[jth]): dist})
            # print(dist)
    distances1 = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
    return distances1


def main():
    args = get_args()
    labled_files = get_filelist(args.filelist)
    # print(labled_files)
    distances = genotype_distance(labled_files)
    output_results(distances, args.output)


if __name__ == '__main__':
    main()
