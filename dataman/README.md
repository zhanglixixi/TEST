# Data management tools

## 数据备份
目前数据使用外接机械硬盘进行冷备份。

1.连接硬盘并查看硬件情况
```textmate
sudo fdisk -l
```

2.初始化和挂载硬盘，如：
```textmate
./init-mnthdd-mgi2k.sh /dev/sdc /mnt/dm05 MGI2K015
```

3.在钉盘数据管理表中登记硬盘编号和序列号。

4.准备备份目录清单，并保存至`/aegis/staff/datamover/datamove.list`目录，命名规则和内容可见既往清单。
注意硬盘中剩余空间大于清单中文件总大小，用`df`查看硬盘空间，`cat list | xargs du -cs`查看清单中文件总大小。

5.生成备份脚本，运行命令和输出文件的例子如下，注意运行该脚本时请保证pwd在/aegis分区下。
```textmate
$ ./dmscript-gen.sh -m 50 -s /aegis/staff/datamover/datamove.list/MGI2K015.a.srclist -p MGI2K015.a -d /mnt/dm05/Rawdata/
datamove script - /aegis/staff/datamover/datamove.commands/20201113/MGI2K015.a.datamove.sh
md5gen script - /aegis/staff/datamover/datamove.commands/20201113/MGI2K015.a.md5gen.sh
md5chk script - /aegis/staff/datamover/datamove.commands/20201113/MGI2K015.a.md5chk.sh
```

6.分别依次运行以上三个脚本执行数据拷贝，md5生成和md5校验三个步骤。运行时间较长，建议使用tmux在后台执行。

7.检查校验结果，校验脚本需要在python3环境下运行，示例和结果如下：
```textmate
$ python mgi2k_backupper.py stats -s /aegis/staff/datamover/datamove.list/MGI2K014.a.srclist /aegis/staff/datamover/datamove.logs/20201111/MGI2K014.*.20201111.md5chk.log
Source	N_files	N_OKs
/qh01/data/internal/ngs/mgi2000/RUN2002052	4497	4497
/qh01/data/internal/ngs/mgi2000/RUN2003053	4631	4631
/qh01/data/internal/ngs/mgi2000/RUN2003054	4486	4486
/qh01/data/internal/ngs/mgi2000/RUN2003058	2429	2429
```
8.查验结果，当如上结果中N_files和N_OKs的值相同即表示所有文件均通过校验，删除原始文件。
可使用命令`cat list | xargs echo rm -rv | bash`。
并在钉盘数据管理表中更新。
否则需要查看md5chk.log中哪些文件出错，并重新备份和校验。

9.备份完一批硬盘（5个）时，取出硬盘并贴上标签，放入存储柜冷备份。


#### MD5 validation for MGI2000 platform data (暂未使用)
Usage:
```bash
python mgi2k_md5_check.py path/to/data out_dir lane/flowcell/run
```

如果输入一个run的路径，且选择run参数，则校验该run文件夹下的所有*.fq.gz数据；
如果输入一个flowcell的路径，且选择flowcell参数，则校验该flowcell下的所有数据；
如果输入一个lane的路径，且选择lane参数，则校验该lan下的所有数据。

输出文件：
md5checkresult.txt	由两列构成，第一列为文件名，第二列为md5校验的结果，若通过则记录为passed，若未通过则记录为error
md5checkresult_summary.txt	统计Passed与error的个数
