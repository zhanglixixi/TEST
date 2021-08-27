# Transcript select introduction
这个子项目的目标在于解决转录本选择的问题，并建立一个可以由人工持续校对后持续追加的模式。

## 经典转录本参考数据库
1. [LRG](http://www.lrg-sequence.org/) 提供一个ACMG推荐的经典转录本集，但包含的基因数目很少
2. [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) 中转录本使用频率，通过统计ClinVar数据库中每个基因的突变记录中使用的转录本的频率，采用使用频率最高的
3. [MANE](https://www.ncbi.nlm.nih.gov/refseq/MANE/) 全称 Matched Annotation from NCBI and EMBL-EBI。
提供一个MANE Select集，目前版本0.9，但MANE只针对hg38，不再维护hg19/GRCh37，有一定参考价值。
```textmate
MANE Select: One high-quality representative transcript per protein-coding gene that is well-supported by experimental data and represents the biology of the gene.
``` 
4. [UCSC](http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/) 整理过known canonical集，
需要和其数据中对应的known gene cross reference配合使用。不过这个数据集最近的更新已经是2013年。

## 内部经典转录本版本
#### `transcript_select_20210111.txt 修正LAMA3的转录本为NM_198129`
#### `transcript_select_20201105.txt`
其中5个数据库的来源及优先级如下：
0. inhouse_transcript.txt（用于转录本数据的修正，列于优先级第一位）
1. LRG （由ACMG校对，共1080条记录）
2. MANE （基于hg38，共15569条记录）
3. ClinVar （根据基因对应突变频率统计，共10971条记录）
4. UCSC_kgkc （共22481条记录）
5. UCSC_refgene （共28210条记录）

## 项目工具
#### `select_transcript.py`

```textmate
usage: select_transcript.py [-h] output inputs [inputs ...]

To select transcript as canonical from mulitiple inputs

positional arguments:
  output      Output file name
  inputs      Input file(s). Priority decrease from first to last given file

optional arguments:
  -h, --help  show this help message and exit
```

从多个输入的转录本数据文件中对转录本进行挑选，输入数据库的优先级按顺序递减。

输入转录本文件格式为`tab`分隔的基因，转录本和标签三列，示例：
```textmate
A1CF    NM_014576       ClinVar
A2M     NM_000014       ClinVar
A2ML1   NM_144670       ClinVar
A4GALT  NM_017436       ClinVar
```

输出两个文件，一个为主要结果，包含`tab`分隔的四列，基因，转录本，标签和优先级，示例：
```textmate
ADAMTS18        NM_199355       ClinVar 1
ADAMTS19        NM_133638       ClinVar 1
ADAMTS2 NM_014244       ClinVar 1
ADAMTS20        NM_025003       ClinVar 1
```

另一个为详细结果，记录基因对应的转录本在个输入数据文件中的情况，示例：
```textmate
A1BG    ['NM_130786', 'NM_130786', 'NM_130786'] ['UCSC_kckg', 'MANE', 'UCSC_refGene']   [2, 3, 4]
A1BG-AS1        ['NR_015380', 'NR_015380']      ['UCSC_kckg', 'UCSC_refGene']   [2, 4]
A1CF    ['NM_014576', 'NM_138932', 'NM_014576', 'NM_001198819'] ['ClinVar', 'UCSC_kckg', 'MANE', 'UCSC_refGene']        [1, 2, 3, 4]
A2M     ['NM_000014', 'NM_000014', 'NM_000014', 'NM_001347423'] ['ClinVar', 'UCSC_kckg', 'MANE', 'UCSC_refGene']        [1, 2, 3, 4]
```

#### `get_clinvar_txs.py`

```textmate
usage: get_clinvar_txs.py [-h] variant_summary outfile

Get gene and transript information from variant_summary.txt(.gz).

positional arguments:
  variant_summary  ClinVar variant summary, variant_summary.txt(.gz)
  outfile          Output file name

optional arguments:
  -h, --help       show this help message and exit
```

从ClinVar数据库中按基因所包含突变是用的转录本频次对转录本进行挑选。
输入为ClinVar数据库中下载的`variant_summary.txt(.gz)`，
输出按频率筛选的转录本，各基因使用转录本的频次统计，示例分别为：
```textmate
A1CF    NM_014576       ClinVar
A2M     NM_000014       ClinVar
A2ML1   NM_144670       ClinVar
```
```textmate
ABCA2   NM_212533       1
ABCA2   NM_001606       36
ABCA3   NM_001089       275
```

#### `get_mane_txs.py`

```textmate
usage: get_mane_txs.py [-h] manebed outfile

Get gene and transript information from mane.{version}.bed

positional arguments:
  manebed     MANE bed format, normally converted from bigbed by UCSC tool
              bigBedToBed
  outfile     Output file name

optional arguments:
  -h, --help  show this help message and exit
```

从MANE数据库中提取基因和转录本对应表，格式与以上类似。

#### `get_ucsc_kctxs.py`

```textmate
usage: get_ucsc_kctxs.py [-h] kctx kgxref outfile

Get canonical transripts from UCSC known canonical.

positional arguments:
  kctx        UCSC known canonical, knownCanonical.txt(.gz)
  kgxref      UCSC known gene cross reference, kgXref.txt(.gz)
  outfile     Output file name

optional arguments:
  -h, --help  show this help message and exit
```

从UCSC整理的known canonical transcript和known gene cross reference中提取基因转录本对应表，
格式与以上类似。

#### `get_refgene_txs.py`

```textmate
usage: get_refgene_txs.py [-h] refgene outfile

Get gene and transript information from refGene.txt(.gz).

positional arguments:
  refgene     UCSC refgene file, refGene.txt(.gz)
  outfile     Output file

optional arguments:
  -h, --help  show this help message and exit
```

从UCSC refGene.txt(.gz)中提取基因转录本对应表。
通常来说，这个作为最后优先级，即，当其他数据都没包含对基因的转录本选择且存在多个转录本时，
选择refGene记录中最长（exon数目对多）的转录本。

#### `get_LRG_GRCh38_txs.py`

```textmate
usage: get_LRG_GRCh38_txs.py [-h] LRG_GRCh38 outfile

Get gene and transript information from list_LRGs_transcripts_GRCh38_xrefs.txt.

positional arguments:
  LRG_GRCh38     LRG GRCh38 file, list_LRGs_transcripts_GRCh38_xrefs.txt
  outfile     Output file

optional arguments:
  -h, --help  show this help message and exit
```

从LRG list_LRGs_transcripts_GRCh38_xrefs.txt中提取基因转录本对应表。

