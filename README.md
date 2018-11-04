# Lianjia houseInfo collector

<br />

+ 项目概述：该项目提供一个[链家网](https://bj.lianjia.com/)房源爬虫工具，数据使用[Sqlite３](https://www.sqlite.org/index.html)进行存储。
+ 数据获取：在项目给出的demo中，我们选择获取北京市城内六区（西城、东城、海淀、朝阳、丰台、石景山）的二手房出售及租赁信息，在后面对此进行分析和可视化操作。
+ 数据分析与可视化：利用Pandas和Ｍatplotlib ([lianjia_data_analysis.ipynb](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/lianjia_data_analysis.ipynb)）分析和可视化链家在线房源数据，同时使用[高德开放平台](https://lbs.amap.com/)对房源地理位置进行了可视化展示。


<br />


## 使用说明
+ 下载源码并安装依赖
```
1. git clone https://github.com/I-mm/Lianjia-houseInfo
2. cd Lianjia-houseInfo
3. pip install -r requirements.txt
```

+ 设置数据库信息以及爬取城市行政区信息（settings.py）
```
vi settings.py
DBENGINE = 'sqlite3'
DBNAME = 'beijing_chengliuqu.db' # 导出数据库命名
CITY = 'bj'  # 爬取的城市分站, beijing=bj, shanghai=sh......
REGIONLIST = [u'dongcheng', u'xicheng', u'chaoyang', u'fengtai', u'shijingshan', u'haidian'] # 爬取的城市内行政区，这里我们爬取北京城六区的二手房信息
```

+ 运行 `python scrawl.py`

**Notes:** 

+ 该项目提供两种方式爬取房源信息，一个是根据行政区，另一个是根据小区名。 但是根据行政区的只显示前100页的数据，所以对于像北京市朝阳区这种房源比较多的行政区，最好通过小区名才能爬全。

<br />


##　部分文件说明

+ [beijing_chengliuqu.db](https://github.com/I-mm/Lianjia-houseInfo/blob/master/beijing_chengliuqu.db)：存储获得的北京城六区的二手房源信息
+ [data](https://github.com/I-mm/Lianjia-houseInfo/tree/master/data)：存储了由ｄｂ文件导出得到的ｃｓｖ格式的数据
+ [data_analysis](https://github.com/I-mm/Lianjia-houseInfo/tree/master/data_analysis)：数据分析相关代码和ｏｕｔｐｕｔ




<br />


## 数据分析

### 标量数据的分析和可视化

具体请参见**data_analysis**／[lianjia_data_analysis.ipynb](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/lianjia_data_analysis.ipynb)

<br />

### 地理位置的可视化展示

这里使用高德开放平台的[位置数据可视化](https://lbs.amap.com/getting-started/visual/)功能。根据要求，我们先需要根据房源语义上的地理位置信息，使用[web地理编码api](https://lbs.amap.com/api/webservice/guide/api/georegeo)将其转换为坐标信息并插入表尾一栏。在获得坐标数据之后，再使用该功能进行位置信息的可视化。

- [getCoordinate.py](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data/getCoordinate.py): 发起请求接收位置数据，被[readCSV.py](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data/readCSV.py)调用

部分可视化效果展示：（具体参见[output](https://github.com/I-mm/Lianjia-houseInfo/tree/master/data_analysis/output)）



**！！！！！！！这里放那一堆图！！！！！！！**

<br />



