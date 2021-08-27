#!/usr/bin/env bash

prog=$(basename "${BASH_SOURCE[0]}")
dirpath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
usage="${prog} in_fq.gz out_fq.gz read_number"

[[ $# -lt 3 ]] && echo -e "${usage}" && exit 0

in_fq=$1
out_fq=$2
readnum=$3

linenum=$(echo "${readnum} * 4" | bc)
echo "sample ${linenum} reads from ${in_fq}, to ${out_fq}"

conda_env="/qh03/env/anaconda3.dev1/bin/activate cnvtools"
source ${conda_env}
set -x
zcat ${in_fq} | head -n ${linenum} | pigz -c -p 4 - > ${out_fq}
