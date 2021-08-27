#!/bin/bash

author='Yongchu Liu'
version='v0.1.3'
updated='2020-06-28'
usage="
Create databackup scripts. Version ${version}, updated on ${updated}

Usage: $(basename $0) [options] ...
options:
  -m INT        sync bandwidth limitation at MB/s, default=100
  -p STRING     prefix for sync project, required
  -s FILE       source path list, required
  -d PATH       destination path, required
  -o DIR        directory of output shell scripts, default=/{pool}/staff/datamover/datamove.commands
  -l DIR        path of logfile, default=/{pool}/staff/datamover/datamove.logs
                where {pool} is automaticall detected to be /aegi, /aegis or /agdisk
"

[[ $# -lt 1 ]] && echo "${usage}" && exit 0

limitm=100
prefix=""
srclist=""
desdir=""
starttime=`date +%Y%m%d`
pool=`pwd | cut -d"/" -f2`
logpath=/${pool}/staff/datamover/datamove.logs/${starttime}
outdir=/${pool}/staff/datamover/datamove.commands/${starttime}
md5file=md5_src.txt

while getopts :m:p:s:d:o:l: optname
do
  case ${optname} in
    m)
      limitm=$OPTARG;;
    p)
      prefix=$OPTARG;;
    s)
      srclist=$OPTARG;;
    d)
      desdir=$OPTARG;;
    o)
      outdir=$OPTARG;;
    l)
      logpath=$OPTARG;;
    ?)
      echo Unrecognized option.
      exit 1;;
  esac
done

[[ "$prefix" = "" ]] && echo "-- ERROR -- project prefix is required." && exit 1
[[ "$srclist" = "" ]] && echo "-- ERROR -- source list is required." && exit 1
[[ "$desdir" = "" ]] && echo "-- ERROR -- destination directory is required." && exit 1

#shift $(($OPTIND - 1))
[[ ! -d ${outdir} ]] && mkdir -p ${outdir}
[[ ! -d ${logpath} ]] && mkdir -p ${logpath}

bwlimit=$(expr ${limitm} \* 1024)
logdir=${desdir}/datamove.logs
logdir=$(realpath ${logdir})
desdir=$(realpath ${desdir})

datamoveshellcmd=${outdir}/${prefix}.datamove.sh
if [[ -f "$datamoveshellcmd" ]]; then
  echo "-- ERROR -- $datamoveshellcmd already exists, use another prefix"
else
  echo "#!/bin/bash" > ${datamoveshellcmd}
  echo "set -x" >> ${datamoveshellcmd}
  echo "[ ! -d $desdir ] && mkdir $desdir" >> ${datamoveshellcmd}
  echo "[ ! -d $logdir ] && mkdir $logdir" >> ${datamoveshellcmd}
#  for nn in `ls -d $*`; do
  while read -r nn
  do
    srcpathdirname=$(dirname ${nn})
    srcpathbasename=$(basename ${nn})
    datamovelog=${prefix}.${srcpathbasename}.${starttime}.datamove.log
    srcpath=${srcpathdirname}/${srcpathbasename}
    echo "rsync -auvP --bwlimit=${bwlimit} ${srcpath} ${desdir} --log-file=${logdir}/${datamovelog}" >> ${datamoveshellcmd}
    echo "cp -f ${logdir}/${datamovelog} ${logpath}/" >> ${datamoveshellcmd}
  done < ${srclist}
  echo "datamove script - ${datamoveshellcmd}"
fi

md5genshellcmd=${outdir}/${prefix}.md5gen.sh
if [[ -f "$md5genshellcmd" ]]; then
  echo "-- ERROR -- $md5genshellcmd already exists, use another prefix"
else
  echo "#!/bin/bash" > ${md5genshellcmd}
  echo "set -x" >> ${md5genshellcmd}
#  for nn in `ls -d $*`; do
  while read -r nn
  do
    srcpathdirname=$(dirname ${nn})
    srcpathbasename=$(basename ${nn})
    md5file2desdir=${desdir}/${srcpathbasename}/${md5file}
    echo "if [ ! -f $md5file2desdir ]; then" >> ${md5genshellcmd}
    echo "  pwd1=$PWD && cd $nn && find ./ -type f -print0 | xargs -0 md5sum | tee ${md5file2desdir} && cd \$pwd1" >> ${md5genshellcmd}
    echo "else" >> ${md5genshellcmd}
    echo "  echo $md5file already exists." >> ${md5genshellcmd}
    echo "fi" >> ${md5genshellcmd}
  done < ${srclist}
  echo "md5gen script - ${md5genshellcmd}"
fi

md5chkshellcmd=${outdir}/${prefix}.md5chk.sh
if [[ -f "$md5chkshellcmd" ]]; then
  echo "-- ERROR -- $md5chkshellcmd already exists, use another prefix"
else
  echo "#!/bin/bash" > ${md5chkshellcmd}
  echo "set -x" >> ${md5chkshellcmd}
#  for nn in `ls -d $*`; do
  while read -r nn
  do
    srcpathdirname=$(dirname ${nn})
    srcpathbasename=$(basename ${nn})
    md5file2desdir=${desdir}/${srcpathbasename}/${md5file}
    dessubdir=${desdir}/${srcpathbasename}
    md5checklog=${logdir}/${prefix}.${srcpathbasename}.${starttime}.md5chk.log
    echo "if [ ! -f $md5file2desdir ]; then" >> ${md5chkshellcmd}
    echo "  echo $md5file2desdir doesn\'t exist, please run $md5genshellcmd first." >> ${md5chkshellcmd}
    echo "elif [ ! -f $md5checklog ]; then" >> ${md5chkshellcmd}
    echo "  pwd1=$PWD && cd ${dessubdir} && md5sum -c $md5file | tee $md5checklog && cd \$pwd1" >> ${md5chkshellcmd}
    echo "else" >> ${md5chkshellcmd}
    echo "  echo $md5checklog already exists." >> ${md5chkshellcmd}
    echo "fi" >> ${md5chkshellcmd}
    echo "cp -f ${md5checklog} ${logpath}/" >> ${md5chkshellcmd}
  done < ${srclist}
  echo "md5chk script - ${md5chkshellcmd}"
fi
