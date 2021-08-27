# -*- coding:utf-8 -*-
### 从下机的excel表中提取信息，生成*sampleinfo.txt
### python get_info_from_excel.py in_excel_list outout_dir


import os,sys
import xlrd

def get_info_from_excel(excelfile, outdir):
    '从下机信息excel表提取信息'

    data = xlrd.open_workbook(excelfile)
    sheet = data.sheet_by_index(0)
    nrows = sheet.nrows
    tmpfilename = str(excelfile).strip().split('/')[-1].split('.xlsx')[0]+'.tmp.txt'
    outfilename = str(excelfile).strip().split('/')[-1].split('.xlsx')[0]+'.sampleinfo.txt'
    # print(outfilename)
    with open(str(outdir)+'/'+str(tmpfilename),'w') as fout:
        for i in range(nrows):
            if i >1:
                row_value = sheet.row_values(i,0,12)
                sample = row_value[6]
                run_id = row_value[1]
                flowcell = row_value[2]
                lane = row_value[3]
                DNB = row_value[4]
                pooling =row_value[5]
                library = row_value[6]
                barcode = row_value[7]
                fout.write(str(sample)+'\t'+str(run_id)+'\t'+str(flowcell)+'\t'+str(lane)+'\t'+str(DNB)+'\t'+str(pooling)+'\t'+str(library)+'\t'+str(barcode)+'\n')
    
    ### 删除文档的空白行
    f1 = open(str(outdir)+'/'+str(tmpfilename), 'r', encoding='utf-8')
    f2 = open(str(outdir)+'/'+str(outfilename), 'w', encoding='utf-8')
    try:
        for line in f1.readlines():
            if not 'RUN' in line:
                line = line.strip('\n')
            f2.write(line)
    finally:
        f1.close()
        f2.close()
    os.system('rm '+str(outdir)+'/'+str(tmpfilename))
    # print('rm '+str(outdir)+'/'+str(tmpfilename))

    os.system('cat '+str(outdir)+'/RUN*.sampleinfo.txt > '+str(outdir)+'/ALLRUNS.sampleinfo.txt')
    return

if __name__ =='__main__':
    excelfile = sys.argv[1]
    outdir = sys.argv[2]

    print(excelfile)
    get_info_from_excel(excelfile, outdir)
