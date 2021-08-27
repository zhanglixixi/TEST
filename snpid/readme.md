# SNP ID

当比较两个样本在基因组某一个具体位置上的SNP，则有可能相同或不同，并且相同的概率不低。
显而易见地，当比较的位置增多，则所有位置上的SNP都相同的概率就会越来越低。

因此，使用经过一定挑选的区域，采用区域内的基因型可以达到给样本标记SNP ID的目的。

`snpid-evalute.sh`可以用于计算一批给定的VCF在所给基因组区域(bed)上突变的差异大小。
结果按差异大小进行排序。

因此，可以用于判定一批VCF中是否存在相同的SNP ID。即VCF是否来自于同一样本。

## 用法
```textmate
Program: snpid-evaluate.sh
Version: 1.0.200925
Description: Evaluate SNP ID results - compute distances between samples for evaluting

Usage: snpid-evaluate.sh [options] outdir sample-vcf-map
Options:
  -b|--bed FILE    SNP ID bed file [/qh04/database/human/enrichments/bed/snpid-v1/hg19/targets.bed]
  -h|--help        print help message
```

其中 `--bed` 指定挑选的基因组区域，`sample-vcf-map`为指定`sample`和`vcf`对应关系的文件，tab分隔，示例如下：

```textmate
SAS17439	/qh01/results/development/SAS17439/variant/snv/data/SAS17439.norm.vcf.gz
SAS17440	/qh01/results/development/SAS17440/variant/snv/data/SAS17440.norm.vcf.gz
SAS17441	/qh01/results/development/SAS17441/variant/snv/data/SAS17441.norm.vcf.gz
SAS17442	/qh01/results/development/SAS17442/variant/snv/data/SAS17442.norm.vcf.gz
SAS17444	/qh01/results/development/SAS17444/variant/snv/data/SAS17444.norm.vcf.gz
SAS17445	/qh01/results/development/SAS17445/variant/snv/data/SAS17445.norm.vcf.gz
SAS17446	/qh01/results/development/SAS17446/variant/snv/data/SAS17446.norm.vcf.gz
SAS17447	/qh01/results/development/SAS17447/variant/snv/data/SAS17447.norm.vcf.gz
SAS17448	/qh01/results/development/SAS17448/variant/snv/data/SAS17448.norm.vcf.gz
SAS17449	/qh01/results/development/SAS17449/variant/snv/data/SAS17449.norm.vcf.gz
SAS17453	/qh01/results/development/SAS17453/variant/snv/data/SAS17453.norm.vcf.gz
SAS17454	/qh01/results/development/SAS17454/variant/snv/data/SAS17454.norm.vcf.gz
SAS17455	/qh01/results/development/SAS17455/variant/snv/data/SAS17455.norm.vcf.gz
SAS17456	/qh01/results/development/SAS17456/variant/snv/data/SAS17456.norm.vcf.gz
SAS17457	/qh01/results/development/SAS17457/variant/snv/data/SAS17457.norm.vcf.gz
SAS17458	/qh01/results/development/SAS17458/variant/snv/data/SAS17458.norm.vcf.gz
```

SNP差异结果存在`snps_dist.txt`文件中，其格式如下，a,b,c为SNP差异值，按从小到大排序：
```textmate
sample1 - sample2	a
sample1 - sample3	b
sample2 - sample3	c
...
```

# 场景
一种常用的场景是检查测序数据（WES/WGS）是否来自于某一样本。
在有数据的情况下，只需要对该样本的指定SNP ID区域测序，然后计算两个vcf之间的SNP距离即可。

SNPID测序的分析流程使用最新版 `biomodules-{version}/shellflows/snpid/snpid.sge.sh`，用法为
```textmate
Program: snpid.sge.sh
Version: 1.0.200924
Description: shell script flow - snpid

Usage: snpid.sge.sh [options] outdir prefix fq1 fq2
Options:
  -m|--biomodules-dir PATH    biomodules directory [/aegis/staff/yongchu/CodeSpace/dev/biomodules]
  -f|--config FILE            configuration file [/aegis/staff/yongchu/CodeSpace/dev/biomodules/coms/configs/mgi2000.snpid.v1.configs.sh]
  -h|--help                   print help message
```
