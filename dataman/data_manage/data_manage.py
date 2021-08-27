# -*- coding:utf-8 -*-

import os, sys
import argparse

### python data_manage.py -l MGI2K024.a.srclist -d dm02
### 用于数据备份

dm_list_dir = '/aegis/staff/datamover/datamove.list/'
# dm_list_file = 'MGI2K024.a.srclist'
dm_scripts_dir = '/aegis/staff/zhangly/datamove/biotoolkit/dataman/'
backup_log_dir = '/aegis/staff/zhangly/datamove/backuplog/'

def scripts_generate(dm_list_file, dm):
    '根据需要备份的list文件，生成备份的命令'
    os.chdir(dm_scripts_dir)
    os.system('bash '+str(dm_scripts_dir) + '/dmscript-gen.sh -m 40 -s ' + str(dm_list_dir)+''+str(dm_list_file)+' -p '+str(dm_list_file).strip().split('.srclist')[0]+' -d /mnt/'+str(dm)+'/Rawdata/')
    print('bash '+str(dm_scripts_dir) + '/dmscript-gen.sh -m 40 -s ' + str(dm_list_dir)+''+str(dm_list_file)+' -p '+str(dm_list_file).strip().split('.srclist')[0]+' -d /mnt/'+str(dm)+'/Rawdata/')

def data_copy(dm_list_file):
    '进行备份的三个步骤'
    os.chdir(dm_scripts_dir)
    dm_list = str(dm_list_file).strip().split('.srclist')[0]
    os.system('bash /aegis/staff/datamover/datamove.commands/*/'+str(dm_list)+'.datamove.sh')
    os.system('bash /aegis/staff/datamover/datamove.commands/*/'+str(dm_list)+'.md5gen.sh')
    os.system('bash /aegis/staff/datamover/datamove.commands/*/'+str(dm_list)+'.md5chk.sh')
    print('bash /aegis/staff/datamover/datamove.commands/*/'+str(dm_list)+'.datamove.sh')
    print('bash /aegis/staff/datamover/datamove.commands/*/'+str(dm_list)+'.md5gen.sh')
    print('bash /aegis/staff/datamover/datamove.commands/*/'+str(dm_list)+'.md5chk.sh')

def check(dm_list_file):
    '对备份结果进行检查'
    os.chdir(dm_scripts_dir)
    os.system('python3 '+str(dm_scripts_dir)+'mgi2k_backupper.py stats -s '+str(dm_list_dir)+str(dm_list_file)+' /aegis/staff/datamover/datamove.logs/*/'+str(dm_list_file).strip().split('.')[0]+'.*.*.md5chk.log')
    print('python3 '+str(dm_scripts_dir)+'mgi2k_backupper.py stats -s '+str(dm_list_dir)+str(dm_list_file)+' /aegis/staff/datamover/datamove.logs/*/'+str(dm_list_file).strip().split('.')[0]+'.*.*.md5chk.log')

def backuplog(dm_list_file):
    os.chdir(dm_list_dir)
    flog = open(str(backup_log_dir)+'backup_log.txt', 'a')
    with open(dm_list_file, 'r') as fin:
        for line in fin:
            flog.write(str(dm_list_file).strip().split('.')[0]+'\t'+str(line).strip()+'\n')
    flog.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', required=True, help='Please input datalist, eg: MGI2K024.a.srclist')
    parser.add_argument('--dm', '-d', required=True, help = 'put dm number, eg: dm02')
    
    args = parser.parse_args()

    dm_list_file = args.list
    dm = args.dm

    scripts_generate(dm_list_file, dm)
    data_copy(dm_list_file)
    check(dm_list_file)
    backuplog(dm_list_file)
