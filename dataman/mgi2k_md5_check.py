# -*- coding:utf-8 -*-
import sys
import os

print("Usage: python md5_check.py in_dir out_dir run/flowcell/lane")
print("------------------------------------")
print("Example 1: python /aegis/staff/zhangly/scripts/md5check/md5_check.py /qh01/data/internal/ngs/mgi2000/RUN2007096/V300066794A/L01 /aegis/staff/zhangly/scripts/md5check/out lane")
print("Example 2: python /aegis/staff/zhangly/scripts/md5check/md5_check.py /qh01/data/internal/ngs/mgi2000/RUN2007096/V300066794A /aegis/staff/zhangly/scripts/md5check/out flowcell")
print("Example 3: python /aegis/staff/zhangly/scripts/md5check/md5_check.py /qh01/data/internal/ngs/mgi2000/RUN2007096 /aegis/staff/zhangly/scripts/md5check/out run")


def md5check(datalist, path, outdir):
    f1 = open(datalist, 'r')
    # os.system('mkdir '+str(outdir))
    fmd5 = open(str(outdir)+'/'+str(datalist).strip().split('/')[-1].split('.')[0]+'_md5.txt', 'w')
    data_list=[]
    for l1 in f1:
        data_list.append(str(l1).strip())
    datas = ' '.join(data_list)
        # print (datas)
    os.system('md5sum '+str(datas) +' > '+str(outdir)+'/'+str(datalist).strip().split('/')[-1].split('.')[0]+'_md5.txt')
        # os.system('md5sum '+str(l1).strip()+' > '+str(path)+'/md5.txt')
        # fmd5.write(str(os.system('md5sum '+str(l1).strip()))+'\n')
    f1.close()
    fmd5.close()
    # print(dict_md5)

    dictB = {}
    fmd5 = open(str(outdir)+'/'+str(datalist).strip().split('/')[-1].split('.')[0]+'_md5.txt', 'r')
    for line in fmd5:
        sample = str(line).strip().split('  ')[1]
        md5 = str(line).strip().split('  ')[0]
        dictB[sample] = md5
    fmd5.close()
    # print (dictB)

    dictA = {}
    for files in os.walk(path):
        for fname in files:
            # print (fname)
            for i in fname:
                if '_FileInfo.csv' in i:
                    f2 = open(str(path)+'/'+str(i), 'r')
    # f2 = open(str(path)+'/V300066794A_L01_FileInfo.csv', 'r')
                    for l2 in f2:
                        sample = str(path)+'/'+str(l2).strip().split(',')[0]
                        md5 = str.lower(str(l2).strip().split(',')[1].replace('-', ''))
                        dictA[sample] = md5     
                    f2.close()
    # print (dictA)

    f=open(str(outdir)+'/'+str(datalist).strip().split('/')[-1].split('.')[0]+'_md5checkresult.txt', 'w')
    for i in dictA.keys():
        if str(dictA[i]) == str(dictB[i]):
            f.write(str(i)+'\t'+'Passed!'+'\n')
        else:
            f.write(str(i)+'\t'+'Error!'+'\n')  
    f.close()

    sumlist=[]
    fsum = open(str(outdir)+'/'+str(datalist).strip().split('/')[-1].split('.')[0]+'_md5checkresult.txt', 'r')
    for line in fsum:
        sumlist.append(str(line).strip().split('\t')[1])
    fsum.close()
    stat={}
    fsumout = open(str(outdir)+'/'+str(datalist).strip().split('/')[-1].split('.')[0]+'_md5checkresult_summary.txt', 'w')
    for item in sumlist:
        if item not in stat:
            stat[item]=1
        else:
            stat[item]+=1
    for i in stat.keys():
        print (str(i)+' : '+str(stat[i])+'\n')
        fsumout.write(str(i)+'\t'+str(stat[i])+'\n')
    fsumout.close()

    return

datapath = sys.argv[1]
outdir = sys.argv[2]
checktype = sys.argv[3]

try:
    os.mkdir(str(outdir))
except:
    print(str(outdir)+' exist')

if checktype =='lane':
    datapath = datapath
    outdir = outdir
    os.system('ls '+str(datapath)+'/*.fq.gz > '+str(outdir)+'/datalist.txt')
    # cmd = """ls {path}/*.fq.gz > {path}/{datalist}""".format(path = datapath , datalist ='datalist.txt')
    datalist = str(outdir)+'/datalist.txt'
    md5check(datalist, datapath, outdir)
elif checktype =='flowcell':
    for fi in os.listdir(datapath):
        fi_d = os.path.join(datapath, fi)
        datapathlist=[]
        if os.path.isdir(fi_d):
            datapathlist.append(fi_d)
            for i in datapathlist:
            # datapath = fi_d
                outdir = outdir
                print (str(outdir))
                os.system('ls '+str(i)+'/*fq.gz > '+str(outdir)+'/'+str(i).split('/')[-1]+'_datalist.txt')
            # cmd = """ls {path}/*.fq.gz > {path}/{datalist}""".format(path = str(datapath) , datalist ='datalist.txt')
                datalist = str(outdir)+'/'+str(i).split('/')[-1]+'_datalist.txt'
                md5check(datalist, i, outdir)
        else:
            continue
elif checktype =='run':
    for fi in os.listdir(datapath):
        fi_d = os.path.join(datapath, fi)
        if os.path.isdir(fi_d):
            for fj in os.listdir(fi_d):
                datapathlist=[]
                if os.path.isdir(fi_d+'/'+fj):
                    # print fi_d+'/'+fj
                    datapathlist.append(fi_d+'/'+fj)
                    # datapath = fi_d+'/'+fj
                    for i in datapathlist:
                        outdir = outdir
                        # print (i)
                        # print (str(i).split('/')[-2]+'_'+str(i).split('/')[-1]+'_datalist.txt')
                        os.system('ls '+str(i)+'/*fq.gz > '+str(outdir)+'/'+str(i).split('/')[-2]+'_'+str(i).split('/')[-1]+'_datalist.txt')
                    # cmd = """ls {path}/*.fq.gz > {path}/{datalist}""".format(path = str(datapath) , datalist ='datalist.txt')
                        datalist = str(outdir)+'/'+str(i).split('/')[-2]+'_'+str(i).split('/')[-1]+'_datalist.txt'
                        md5check(datalist, i, outdir)