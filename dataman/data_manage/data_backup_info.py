# -*- coding:utf-8 -*-

### backup: 获取样本的备份信息。输入AS号列表，输出样本的备份盘信息
### info: 获取样本的下机信息与数据信息。输入AS号列表，输出样本的下机信息与质控信息：RUN、lane、barcode、数据量、depth、GC、Q30等
### 查询给定run包含哪些样本

### python data_backup_info.py in_AS_list out_file

import os,sys
import argparse

data_backup_dir = '/aegis/staff/datamover/datamove.list/'
data_info_dir = '/aegis/staff/zhangly/datamove/scripts/sampleinfo/'


def get_backup_info1(query):
    '获取AS号与备份盘的信息'
    dir1 = data_backup_dir
    os.chdir(dir1)
    allfiles = os.listdir(dir1)
    for i in allfiles:
        with open(i, 'r') as fin:
            for line in fin:
                if str(query) in str(line).strip():
                    info1 = str(query)+'\t'+str(i)+'\t'+str(line.strip())
                    print(info1)
                else:
                    info1 = str(query)+' backup info not found!'
                    # print(info1)
    return(info1)
# get_backup_info1('RUN1912032')

def get_backup_info2(AS):
    '获取AS号与下机信息'
    dir2 = data_info_dir
    os.chdir(dir2)
    info2list=[]
    with open('ALLRUNS.sampleinfo.txt', 'r') as fin:
        for line in fin:
            if str(AS) == str(line).strip().split('\t')[0]:
                run = str(line).strip().split('\t')[1]
                Flowcell = str(line).strip().split('\t')[2]
                lane = str(line).strip().split('\t')[3]
                barcode = str(line).strip().split('\t')[7]
                info2 =str(AS)+','+str(run)+','+str(Flowcell)+','+str(lane)+','+str(barcode)
                # print(info2)
                info2list.append(info2)
    for i in info2list:
        print(i)
    return(info2list)
# print(get_backup_info2('AS20566'))

def get_dataQCs_info(AS):
    '获取数据质控信息：总数据量、平均深度、GC、Q30'
    file_path1 = '/agdisk/backup/clinic/'+str(AS)+'/global/qc/'+str(AS)+'_qc_check.txt'
    file_path2 = '/agdisk/backup/clinic/'+str(AS)+'/qualityControl/'+str(AS)+'_qc_check.txt'
    # print(file_path1)
    # print(file_path2)
    RawBases, AveDepth, GC, Q30=[],[],[],[]
    # file_path=''
    if os.path.exists(file_path1):
        file_path = file_path1
    elif os.path.exists(file_path2):
        file_path = file_path2
    else:
        file_path=''
        print(str(AS)+' data not found\n')
    if str(file_path) == str(file_path1) or str(file_path) == str(file_path2):
        with open(str(file_path), 'r') as f1:
            for line in f1:
                if str(line).strip().split(':')[0].strip() == 'RawBases':
                    RawBases.append(str(line).strip().split(':')[1])
                if str(line).strip().split(':')[0].strip() == 'AveDepth':
                    AveDepth.append(str(line).strip().split(':')[1])
                if str(line).strip().split(':')[0].strip() == 'GC':
                    GC.append(str(line).strip().split(':')[1])
                if str(line).strip().split(':')[0].strip() == 'Q30':
                    Q30.append(str(line).strip().split(':')[1])
    print(str(AS)+'\t'+'RawBases: '+str(RawBases))
    print(str(AS)+'\t'+'AveDepth: '+str(AveDepth))
    print(str(AS)+'\t'+'GC: '+str(GC))
    print(str(AS)+'\t'+'Q30: '+str(Q30))
    return(AS, RawBases, AveDepth, GC, Q30)
# print(get_dataQCs_info('AS23335'))

def get_samples_in_run(run):
    '查询某个run的所有样本'
    dir3 = data_info_dir
    os.chdir(dir3)
    samplelist=[]
    with open('ALLRUNS.sampleinfo.txt', 'r') as fin:
        for line in fin:
            if 'RUN' in str(line).strip():
                runinfo = str(line).strip().split('\t')[1]
                if str(runinfo) == str(run):
                    samplelist.append(str(line).strip().split('\t')[0])
    for i in samplelist:
        print(str(i))
    return(samplelist)
# print(get_samples_in_run('RUN2012178'))




if __name__ == "__main__":
    ### python data_backup_info.py AS_list output
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='Please input query sample, eg: RUN1912032 or AS8282')  
    parser.add_argument('--run', '-r', action='store_true', default=False, help='Please input RUN')
    parser.add_argument('--backup', '-b', action='store_true', default=False, help='Data backup infomation')
    
    args = parser.parse_args()

    sample = args.input

    if args.backup :
        ### 备份信息
        print('----- backp info -----')
        get_backup_info1(sample)
    elif args.run:
        ### 查询该RUN的所有样本
        print('----- samples in '+str(sample)+' -----')
        get_samples_in_run(sample)
    else:
        ### AS号与下机信息
        print('----- data info -----')
        get_backup_info2(sample)
        ### AS号与质控信息
        print('----- data QC info -----')
        get_dataQCs_info(sample)
