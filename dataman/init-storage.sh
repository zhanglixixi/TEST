#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Global settings and default variables
# -----------------------------------------------------------------------------

prog=$(basename $0)
dirpath=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$(cd ${dirpath}/../coms/utils && pwd)/common-functions.sh"

# -----------------------------------------------------------------------------
# Argument parser
# -----------------------------------------------------------------------------
author="Yongchu Liu"
update="200922"
version_main="1.1"
version_full="${version_main}.${update}"
description="Perform storage initiation"
usage="${prog} [options] storage-pool (such as /qh03)"

[[ $# -lt 1 ]] && print_help_message "${prog}" "${version_full}" "${description}" "${usage}" && exit 0
pool=$1

create_dirs_advanced "root:root" 755 \
  ${pool}/archive \
  ${pool}/data \
  ${pool}/database \
  ${pool}/env \
  ${pool}/projects \
  ${pool}/results \
  ${pool}/staff

create_dirs_advanced "prd:devgroup" 775 \
  ${pool}/data/external/ngs \
  ${pool}/data/external/sanger \
  ${pool}/data/external/others \
  ${pool}/data/internal/ngs \
  ${pool}/data/internal/sanger \
  ${pool}/data/internal/others \
  ${pool}/data/internal/ngs/mgi2000 \
  ${pool}/data/outsource/ngs \
  ${pool}/data/outsource/sanger \
  ${pool}/data/outsource/others \
  ${pool}/data/upload/ngs \
  ${pool}/data/upload/sanger \
  ${pool}/data/upload/others \
  ${pool}/data/download \
  ${pool}/database/human \
  ${pool}/database/others \
  ${pool}/projects/scratch \
  ${pool}/results/clinic \
  ${pool}/results/development \
  ${pool}/results/reprocess \
  ${pool}/results/research

create_dirs_advanced "yongchu:yongchu" 755 ${pool}/staff/yongchu
create_dirs_advanced "datamover:datamover" 755 ${pool}/staff/datamover
