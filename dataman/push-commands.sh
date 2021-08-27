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
description="Push commands to slave nodes"
usage="${prog} \"commands\" user node [node2] [node3] ...
NOTE: commands must be quoted by \"\"."

[[ $# -lt 3 ]] && print_help_message "${prog}" "${version_full}" "${description}" "${usage}" && exit 0

commands=$1
user=$2
shift 2
nodes=$*

log_info "Nodes: ${nodes}"
log_info "Command: ${commands}"

for node in ${nodes}; do
  log_info "On node ${node} run commands: ${commands}"
  ssh -t ${user}@${node} "${commands}"
  sleep 1
done
