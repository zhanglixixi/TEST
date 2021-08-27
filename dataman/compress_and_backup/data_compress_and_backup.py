# -*- coding:utf-8 -*-

import os
import sys
import argparse
import textwrap
### 例：/qh01/data/internal/ngs/mgi2000/RUN2009138


ref_genome = "/aegis/database/human/GRCH37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa"
# log_dir = "/aegis/staff/datamover/datamove.logs/gtz.log/"
# command_dir = "/aegis/staff/datamover/datamove.commands/gtz.command/"

### Test
log_dir = "/aegis/staff/zhangly/datamove/gtz/log/"
command_dir = "/aegis/staff/zhangly/datamove/gtz/command/"

def get_fq_gz_file(run_dir, log_dir):
    RUN = str(run_dir).strip().split('/')[-1]
    fq_gz_list = "{log_dir}/{RUN}_data.list".format(log_dir=log_dir, RUN=RUN)
    # print("ls {run_dir}/*/*/* > {fq_gz_list}".format(run_dir=run_dir, log_dir=log_dir, fq_gz_list=fq_gz_list))
    os.system("ls {run_dir}/*/*/* > {fq_gz_list}".format(run_dir=run_dir, log_dir=log_dir, fq_gz_list=fq_gz_list))
    return fq_gz_list

def gtz(fq_gz_list, run_dir, out_dir):
    gtz = "/aegis/staff/linph/software/gtz-zip/install/GTZ/gtz"
    RUN = str(run_dir).strip().split('/')[-1]
    os.chdir(command_dir)
    fout = open("{command_dir}/{RUN}_command.sh".format(command_dir=command_dir, RUN=RUN), 'w')

    with open(fq_gz_list, 'r') as fin:
        for line in fin:
            flowcell = str(line).strip().split('/')[-3]
            lane = str(line).strip().split('/')[-2]
            out = "{out_dir}/{RUN}/{flowcell}/{lane}/".format(out_dir=out_dir, RUN=RUN, flowcell=flowcell, lane=lane)
            os.system("mkdir -p {out}".format(out=out))
            if "fq.gz" in str(line):
                fq_gz = str(line).strip()
                fq_gz_name = str(fq_gz).split('/')[-1]
                cmd = "{gtz} {fq_gz} -o {out}/{fq_gz_name}.gtz --ref {ref_genome} -p {threads} --verify".format(
                    gtz=gtz, fq_gz=fq_gz, out=out, fq_gz_name=fq_gz_name, ref_genome=ref_genome, threads=threads)
            else:
                file_name = str(line).strip()
                cmd = "cp {file_name} {out}".format(file_name=file_name, out=out)
            fout.write(str(cmd)+'\n')
        fout.close()

    # os.system("nohup bash {command_dir}/{RUN}_command.sh > {log_dir}/{RUN}.log".format(command_dir=command_dir, RUN=RUN, log_dir=log_dir))
    print("nohup bash {command_dir}/{RUN}_command.sh > {log_dir}/{RUN}.log".format(command_dir=command_dir, RUN=RUN, log_dir=log_dir))
    return

def check(run_dir, out_dir):
    RUN = str(run_dir).strip().split('/')[-1]
    f1 = "{log_dir}/{RUN}_data.list".format(log_dir=log_dir, RUN=RUN)
    count1 = len(open(f1, 'r').readlines())
    out = "{out_dir}/{RUN}/*/*/".format(out_dir=out_dir, RUN=RUN)
    os.system("ls {out}/* > {log_dir}/{RUN}_backup.list".format(out=out, log_dir=log_dir, RUN=RUN))
    f2 = "{log_dir}/{RUN}_backup.list".format(log_dir=log_dir, RUN=RUN)
    count2 = len(open(f2, 'r').readlines())
    print("File number original: {count1}".format(count1=count1))
    print("File number backup: {count2}".format(count2=count2))
    if int(count1) == int(count2):
        print("{RUN} compress and backup [[ Success ]]".format(RUN=RUN))
    else:
        print("{RUN} compress and backup [ Fail ]".format(RUN=RUN))
    return

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            *************************
            Description:
            用于对下机数据进行压缩及备份
            *************************
            '''))
    parser.add_argument('--run_dir', '-r', required=True, help="input Run dir")
    parser.add_argument('--out_dir', '-o', required=True, help="Out dir for data backup")
    parser.add_argument('--threads', '-t', default="22", help="Threads for gtz")
    parser.add_argument('--tools', '-s', default='gtz', help="Tools used for fq compress")
    args = parser.parse_args()

    run_dir = args.run_dir
    threads = args.threads
    out_dir = args.out_dir

    fq_gz_list = get_fq_gz_file(run_dir, log_dir)
    gtz(fq_gz_list, run_dir, out_dir)
    check(run_dir, out_dir)
