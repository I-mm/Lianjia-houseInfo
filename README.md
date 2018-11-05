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
DBENGINE = 'sqlite3'
DBNAME = 'beijing_chengliuqu.db' # 导出数据库命名
CITY = 'bj'  # 爬取的城市分站, beijing=bj, shanghai=sh......
REGIONLIST = [u'dongcheng', u'xicheng', u'chaoyang', u'fengtai', u'shijingshan', u'haidian'] # 爬取的城市内行政区，这里我们爬取北京城六区的二手房信息
```

+ 运行 `python scrawl.py`

**Notes:** 

+ 该项目提供两种方式爬取房源信息，一个是根据行政区，另一个是根据小区名。 但是根据行政区的只显示前100页的数据，所以对于像北京市朝阳区这种房源比较多的行政区，最好通过小区名才能爬全。

<br />


## 部分文件说明

+ [beijing_chengliuqu.db](https://github.com/I-mm/Lianjia-houseInfo/blob/master/beijing_chengliuqu.db)：存储获得的北京城六区的二手房源信息
+ [data](https://github.com/I-mm/Lianjia-houseInfo/tree/master/data)：存储了由db文件导出得到的csv格式的数据
+ [data_analysis](https://github.com/I-mm/Lianjia-houseInfo/tree/master/data_analysis)：数据分析相关代码和output




<br />


## 数据分析

### 标量数据的分析和可视化

具体请参见**data_analysis**／[lianjia_data_analysis.ipynb](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/lianjia_data_analysis.ipynb)

<br />

### 地理位置的可视化展示

这里使用高德开放平台的[位置数据可视化](https://lbs.amap.com/getting-started/visual/)功能。根据要求，我们先需要根据房源语义上的地理位置信息，使用[web地理编码api](https://lbs.amap.com/api/webservice/guide/api/georegeo)将其转换为坐标信息并插入表尾一栏。在获得坐标数据之后，再使用该功能进行位置信息的可视化。

- [getCoordinate.py](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data/getCoordinate.py): 发起请求接收位置数据，被[readCSV.py](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data/readCSV.py)调用
  
    说明：出于隐私原因，此开源版本隐去了笔者的api key
    ```python
    def get_addrCoor(addr):
      key = "xxxxxxxxxxxxxxxxxxxxxxxxxx" 
      url = "http://restapi.amap.com/v3/geocode/geo?key=" + key + "&address=" + urllib.parse.quote(
        addr) + "&city=" + urllib.parse.quote("北京")
      html = url_open(url)
      target = json.loads(html)
    ```

部分地理位置可视化效果展示：（具体参见[location_visualization](https://github.com/I-mm/Lianjia-houseInfo/tree/master/data_analysis/output/location_visualization)）

- [北京城六区所有二手房源地理分布-圆圈大小代表单价](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/output/location_visualization/%E5%8C%97%E4%BA%AC%E5%9F%8E%E5%85%AD%E5%8C%BA%E6%89%80%E6%9C%89%E4%BA%8C%E6%89%8B%E6%88%BF%E6%BA%90%E5%9C%B0%E7%90%86%E5%88%86%E5%B8%83-%E5%9C%86%E5%9C%88%E5%A4%A7%E5%B0%8F%E4%BB%A3%E8%A1%A8%E5%8D%95%E4%BB%B7.png)

![北京城六区所有二手房源地理分布](https://github.com/I-mm/Lianjia-houseInfo/blob/master/pictures/%E5%8C%97%E4%BA%AC%E5%9F%8E%E5%85%AD%E5%8C%BA%E6%89%80%E6%9C%89%E4%BA%8C%E6%89%8B%E6%88%BF%E6%BA%90%E5%9C%B0%E7%90%86%E5%88%86%E5%B8%83-%E5%9C%86%E5%9C%88%E5%A4%A7%E5%B0%8F%E4%BB%A3%E8%A1%A8%E5%8D%95%E4%BB%B7.png)

- [总价最高的十套二手房源地理分布](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/output/location_visualization/TotalpriceHighst10.png)

![总价最高的十套二手房源地理分布](https://github.com/I-mm/Lianjia-houseInfo/blob/master/pictures/)

- [单价最高的十套二手房源地理分布](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/output/location_visualization/UnitpriceHighest10.png)
- [面积最大的十套二手房源地理分布](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/output/location_visualization/AreaLargest10.png)
- [面积最小的十套二手房源地理分布](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/output/location_visualization/AreaSmallest10.png)
- [关注度最高的十套二手房源地理分布](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data_analysis/output/location_visualization/GuanzhuHighest10.png)



<br />



