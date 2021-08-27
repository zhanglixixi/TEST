# Data management tools

## 下机数据压缩及数据备份


1.初始化和挂载硬盘完成后，准备备份目录清单，并保存至/aegis/staff/datamover/datamove.list目录
```textmate
python data_compress_and_backup.py -r /aegis/staff/zhangly/datamove/gtz/test_data/RUN2009136 -o /aegis/staff/zhangly/datamove/gtz/test_out

-r	需要备份的下机数据路径
-o	备份数据的输出路径
-t	线程数（默认为22）
-s	备份工具选择（默认为GTZ）
```




