#!/usr/bin/env bash

usage="
To show header names and their indcies.

Usage:
head -1 {file-to-check} | $(basename $0)
$(basename $0) {file-to-check}
"

input=${1:-/dev/stdin}
[[ -t 0 && $# -eq 0 ]] && echo "${usage}" && exit 0
head -1 ${input} | awk -F "\t" '{for(i=1;i<=NF;i++) printf("%i - %s\n", i, $i)}'

