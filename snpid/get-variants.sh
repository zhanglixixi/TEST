#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Argument parser
# -----------------------------------------------------------------------------
prog=$(basename "${BASH_SOURCE[0]}")
dirpath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$(cd ${dirpath}/../coms/utils && pwd)/global-settings.sh"

snpid_bed="/qh04/database/human/enrichments/bed/snpid-v1/hg19/targets.bed"

author="Yongchu Liu"
update="200925"
version_main="1.0"
version_full="${version_main}.${update}"
description="Extract variant from VCF file for SNPID testing"
usage="${prog} [options] outdir sample-vcf-map
Options:
  -b|--bed FILE    SNP ID bed file [${snpid_bed}]
  -h|--help        print help message"

while true; do
  case "$1" in
    -b|--bed)
      snpid_bed=$2; shift 2; ;;
    -h|--help)
      print_help_message "${prog}" "${version_full}" "${description}" "${usage}"; exit 0;;
    *) break ;;
   esac
done

[[ $# -lt 2 ]] && print_help_message ${prog} ${version_full} "${description}" "${usage}" && exit 0
outdir=$1
sample_vcf=$2

create_dirs ${outdir}
stamp_version_record ${outdir} "${prog}.${version_full}"
set_global_conda_env
#set -x

nth=0
while IFS=$'\t' read -r sample invcf; do
    let nth++
    log_info "${nth} - ${sample} - ${invcf}"
    bedtools intersect -wao -a ${snpid_bed} -b ${invcf} > "${outdir}/${sample}.snps.bed"
done < ${sample_vcf}
