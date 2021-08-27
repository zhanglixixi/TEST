#!/usr/bin/env bash

help_msg="
Usage: $(basename $0) pool1 [pool2] [pool3] ...
Note: pool can be qh01 qh03 qh04 qh05 qh06 aegis agdisk, etc..
"

[[ $# -lt 1 ]] && echo -e "${help_msg}" && exit 0
pools=$* # qh01 qh03 qh04 qh05 qh06 aegis agdisk
echo "pools: ${pools}"

function print_if_exists {
  local -r fpath=$1
  [[ -f ${fpath} ]] && echo ${fpath}
}

wgs_anno_inters=inter_files_wgs_snv_anno.txt
for pool in ${pools}; do
  ls /${pool}/results/clinic/ |
  while read -r sample; do
    print_if_exists /${pool}/results/clinic/${sample}/annotation/variation-v1.2/${sample}.txt
    print_if_exists /${pool}/results/clinic/${sample}/annotation/variation-v1.2/${sample}_v0_all.txt
    print_if_exists /${pool}/results/clinic/${sample}/annotation/variation-v1.2/${sample}_all.txt
    print_if_exists /qh05/results/clinic/AS27000/variant/snv/anno/AS27000.txt
    print_if_exists /qh05/results/clinic/AS27000/variant/snv/anno/AS27000_v0_all.txt
    print_if_exists /qh05/results/clinic/AS27000/variant/snv/anno/AS27000_all.txt
  done
done | xargs du -chs --time | sort -k2 | tee ${wgs_anno_inters}

clean_fqs=inter_files_clean_fastq.txt
for pool in ${pools}; do
  ls /${pool}/results/clinic/ |
  while read -r sample; do
    print_if_exists /${pool}/results/clinic/${sample}/fastq/data/${sample}.clean_1.fq.gz
    print_if_exists /${pool}/results/clinic/${sample}/cleanData/${sample}.clean.2.fq.gz
  done
done | xargs du -chs --time | sort -k2 | tee ${clean_fqs}

inter_bams=inter_files_bam.txt
for pool in ${pools}; do
  ls /${pool}/results/clinic/ |
  while read -r sample; do
    print_if_exists /${pool}/results/clinic/${sample}/bam/data/${sample}.deduped.bam
    print_if_exists /${pool}/results/clinic/${sample}/bam/data/${sample}.deduped.bam.bai
    print_if_exists /${pool}/results/clinic/${sample}/bam/data/${sample}.realigned.bam
    print_if_exists /${pool}/results/clinic/${sample}/bam/data/${sample}.realigned.bam.bai
    print_if_exists /qh05/results/clinic/AS27000/bam/data/${sample}.deduped.bam
    print_if_exists /qh05/results/clinic/AS27000/bam/data/${sample}.deduped.bam.bai
    print_if_exists /qh05/results/clinic/AS27000/bam/data/${sample}.realigned.bam
    print_if_exists /qh05/results/clinic/AS27000/bam/data/${sample}.realigned.bam.bai
  done
done | xargs du -chs --time | sort -k2 | tee ${inter_bams}
