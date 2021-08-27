# Data management tools

## 数据备份


1.初始化和挂载硬盘完成后，准备备份目录清单，并保存至/aegis/staff/datamover/datamove.list目录
```textmate
python data_manage.py -l MGI2K026.a.srclist -d dm01
```



## 数据查询

1.对于每次的下机数据表，运行一次:
```textmate
python get_info_from_excel.py RUN*.xlsx out_dir
python get_info_from_excel.py /aegis/staff/zhangly/QC/RUN2101191-RUN2101192.xlsx /aegis/staff/zhangly/datamove/scripts/sampleinfo
```

2.备份信息查询：
```textmate
python data_backup_info.py -i RUN1912038 -b
```

3.下机信息查询：
```textmate
python data_backup_info.py -i AS20566
```

4.查询某个RUN的所有样本编号
```textmate
python data_backup_info.py -i RUN1912038 -r
```