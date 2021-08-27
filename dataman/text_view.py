#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Author: Yongchu Liu

from __future__ import absolute_import, unicode_literals
import pandas as pd
import argparse


def get_args():
    parser = argparse.ArgumentParser('A small tool for viewing text')
    return parser.parse_args()


def main():
    args = get_args()


if __name__ == '__main__':
    main()
