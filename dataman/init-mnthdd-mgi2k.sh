#!/bin/bash

echo "------ You need sudo to run this script ------"
#echo "------ Manually run /sudo mkfs.ext4 dev.point/ to format new disk, not automated in script for security ------"
[[ $# -lt 3 ]] && echo Usage: $0 dev-point mnt-point hdd-item-number && exit 1
set -x

dev=$1
mnt=$2
itemn=$3

sudo mkfs.ext4 ${dev}
sudo mount ${dev} ${mnt}
cd ${mnt}
sudo touch ./----This-is-${itemn}----
sudo mkdir Rawdata Results Others
sudo chown -R yongchu:datamover Rawdata Results Others && sudo chmod -R 775 Rawdata Results Others
sudo smartctl -a ${dev} | grep Serial
