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
description="Evaluate SNP ID results - compute distances between samples for evaluting"
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

create_dirs ${outdir}/snps
stamp_version_record ${outdir} "${prog}.${version_full}"
set_global_conda_env
#set -x

cp ${sample_vcf} ${outdir}/sample_vcf_map.txt
snps_bed_list=${outdir}/sample_snps_map.txt
[[ -f ${snps_bed_list} ]] && rm ${snps_bed_list} && touch ${snps_bed_list}
nth=0
while IFS=$'\t' read -r sample invcf; do
    let nth++
    log_info "${nth} - ${sample} - ${invcf}"
    snps_bed="${outdir}/snps/${sample}.snps.bed"
    bedtools intersect -wao -a ${snpid_bed} -b ${invcf} > ${snps_bed}
    echo -e "${sample}\t${snps_bed}" >> ${snps_bed_list}
done < ${sample_vcf}

out_dist=${outdir}/snps_dist.txt
python ${dirpath}/variants-dist.py -l ${snps_bed_list} -o ${out_dist}
