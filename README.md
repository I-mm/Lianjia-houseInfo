# Lianjia houseInfo collector



+ 项目概述：该项目提供一个链家网全国房源爬虫工具，数据使用Sqlite进行存储。
+ 数据获取：在项目给出的demo中，我们选择获取北京市城内六区（西城、东城、海淀、朝阳、丰台、石景山）的二手房出售及租赁数据，在后面对此进行分析和可视化操作。
+ 数据分析与可视化：利用Python Pandas ([source code](https://github.com/I-mm/Lianjia-houseInfo/blob/master/data/lianjia.ipynb))分析链家在线房源数据，本项目提供了一个例子可以参考。

## 使用说明
+ 下载源码并安装依赖包
```
1. git clone https://github.com/XuefengHuang/lianjia-scrawler.git
2. cd lianjia-scrawler
# If you'd like not to use [virtualenv](https://virtualenv.pypa.io/en/stable/), please skip step 3 and 4.
3. virtualenv lianjia
4. source lianjia/bin/activate
5. pip install -r requirements.txt
6. python scrawl.py
```

+ 设置数据库信息以及爬取城市行政区信息（支持三种数据库格式）
```
DBENGINE = 'mysql' #ENGINE OPTIONS: mysql, sqlite3, postgresql
DBNAME = 'test'
DBUSER = 'root'
DBPASSWORD = ''
DBHOST = '127.0.0.1'
DBPORT = 3306
CITY = 'bj' # only one, shanghai=sh shenzhen=sh......
REGIONLIST = [u'chaoyang', u'xicheng'] # 只支持拼音
```

+ 运行 `python scrawl.py`! (请注释16行如果已爬取完所想要的小区信息)

+ 可以修改`scrawl.py`来只爬取在售房源信息或者成交房源信息或者租售房源信息

+ 该程序提供两种方式爬取房源信息，一个是根据行政区，另一个是根据小区名。 但是根据行政区的只显示前100页的数据，对于像北京朝阳这种房源比较多的区，最好通过小区名才能爬全。具体内容请看下一部分。







# 对链家网北京城六区二手房源数据的分析

## 导入链家网二手房在售房源数据（数据更新时间2018-11-3）

```
# coding=utf-8
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# stdout = sys.stdout
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.stdout = stdout

# plt.rcParams['font.sans-serif'] = ['SimHei']    
# plt.rcParams['axes.unicode_minus'] = False

#所有房源信息
house=pd.read_csv('houseinfo_readable_withXY_correct_12000.csv')

# 所有小区信息
community=pd.read_csv('community_readable.csv')

# # 将小区信息和房屋信息表格拼接
community['community'] = community['title']
house_detail = pd.merge(house, community, on='community')

# 将字符串转换成数字
def data_adj(area_data, str):       
    if str in area_data :        
        return float(area_data[0 : area_data.find(str)])    
    else :        
        return None
# 处理房屋面积数据
house['square'] = house['square'].apply(data_adj,str = '平米')
```

## 删除别墅信息

```
bieshu=house[house.housetype.str.contains('别墅')]
print ('记录中共有%d栋别墅'%bieshu.shape[0])
house.drop(bieshu.index,inplace=True)
print ('删除别墅后，现在还剩下%d条房屋记录'%house.shape[0])
```

```
记录中共有7栋别墅
删除别墅后，现在还剩下12334条房屋记录
```

## 数据1：总价前十的二手房源

```
totalHighest10 = house.sort_values('totalPrice',ascending=False).head(10)
display(totalHighest10)
totalHighest10.to_csv("output/totalHighest10.csv",index=False,sep=',')
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

```
.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
```

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>houseID</th>
      <th>title</th>
      <th>link</th>
      <th>community</th>
      <th>years</th>
      <th>housetype</th>
      <th>square</th>
      <th>direction</th>
      <th>floor</th>
      <th>taxtype</th>
      <th>totalPrice</th>
      <th>unitPrice</th>
      <th>followInfo</th>
      <th>decoration</th>
      <th>validdate</th>
      <th>coor_xy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1860</th>
      <td>1.011030e+11</td>
      <td>东单灯市口 霞公府 南北向4居 诚意出售 高楼层</td>
      <td>https://bj.lianjia.com/ershoufang/101103153250...</td>
      <td>霞公府</td>
      <td>中楼层(共7层)/2011年建板楼/东单</td>
      <td>4室2厅</td>
      <td>497.57</td>
      <td>南 北</td>
      <td>中楼层(共7层)/2011年建板楼/东单</td>
      <td>房本满五年</td>
      <td>6688.0</td>
      <td>134414</td>
      <td>196人关注/2次带看近地铁6688万单价134414元/平米</td>
      <td>精装</td>
      <td>12:16.7</td>
      <td>116.408453,39.909869</td>
    </tr>
    <tr>
      <th>3280</th>
      <td>1.011030e+11</td>
      <td>朱雀门坡上叠拼别墅  东南北三面采光   带60平米花园</td>
      <td>https://bj.lianjia.com/ershoufang/101102721772...</td>
      <td>朱雀门</td>
      <td>底层(共5层)/2008年建板楼/陶然亭</td>
      <td>4室2厅</td>
      <td>376.28</td>
      <td>东 南 北</td>
      <td>底层(共5层)/2008年建板楼/陶然亭</td>
      <td>房本满五年</td>
      <td>5239.0</td>
      <td>139232</td>
      <td>240人关注/6次带看房本满五年随时看房5239万单价139232元/平米</td>
      <td>其他</td>
      <td>13:39.2</td>
      <td>116.388148,39.875875</td>
    </tr>
    <tr>
      <th>1199</th>
      <td>1.011030e+11</td>
      <td>北二环 中轴国际 高层观景房 平层一梯一户</td>
      <td>https://bj.lianjia.com/ershoufang/101103070630...</td>
      <td>中轴国际</td>
      <td>高楼层(共21层)/2005年建板楼/安定门</td>
      <td>4室4厅</td>
      <td>452.80</td>
      <td>南 西北</td>
      <td>高楼层(共21层)/2005年建板楼/安定门</td>
      <td>房本满五年</td>
      <td>4972.0</td>
      <td>109806</td>
      <td>83人关注/0次带看近地铁房本满五年4972万单价109806元/平米</td>
      <td>精装</td>
      <td>11:40.5</td>
      <td>116.400677,39.950142</td>
    </tr>
    <tr>
      <th>4055</th>
      <td>1.011020e+11</td>
      <td>耕天下 平层五居室 五个卧室朝南 带露台 园区中间位置</td>
      <td>https://bj.lianjia.com/ershoufang/101102234163...</td>
      <td>耕天下</td>
      <td>中楼层(共7层)/2003年建板楼/陶然亭</td>
      <td>5室3厅</td>
      <td>330.24</td>
      <td>南 北</td>
      <td>中楼层(共7层)/2003年建板楼/陶然亭</td>
      <td>房本满五年</td>
      <td>4650.0</td>
      <td>140807</td>
      <td>117人关注/0次带看房本满五年4650万单价140807元/平米</td>
      <td>其他</td>
      <td>14:24.4</td>
      <td>116.391903,39.873245</td>
    </tr>
    <tr>
      <th>3938</th>
      <td>1.011020e+11</td>
      <td>金融世家 大户型 配套齐 一个房本 诚心卖</td>
      <td>https://bj.lianjia.com/ershoufang/101102374972...</td>
      <td>金融世家</td>
      <td>中楼层(共15层)/2008年建板塔结合/木樨地</td>
      <td>4室2厅</td>
      <td>300.79</td>
      <td>西北</td>
      <td>中楼层(共15层)/2008年建板塔结合/木樨地</td>
      <td>房本满五年</td>
      <td>4250.0</td>
      <td>141295</td>
      <td>190人关注/1次带看近地铁房本满两年4250万单价141295元/平米</td>
      <td>精装</td>
      <td>14:17.6</td>
      <td>116.346735,39.904601</td>
    </tr>
    <tr>
      <th>4631</th>
      <td>1.011030e+11</td>
      <td>红玺台东户高层观景房几乎全新拎包即住</td>
      <td>https://bj.lianjia.com/ershoufang/101102673940...</td>
      <td>红玺台</td>
      <td>高楼层(共24层)/2011年建板楼/太阳宫</td>
      <td>4室2厅</td>
      <td>300.84</td>
      <td>南 北</td>
      <td>高楼层(共24层)/2011年建板楼/太阳宫</td>
      <td>房本满五年</td>
      <td>4200.0</td>
      <td>139610</td>
      <td>201人关注/5次带看近地铁房本满五年4200万单价139610元/平米</td>
      <td>精装</td>
      <td>15:01.1</td>
      <td>116.439163,39.979600</td>
    </tr>
    <tr>
      <th>6174</th>
      <td>1.011030e+11</td>
      <td>高层观景4+2户型 南北通透 独梯独户</td>
      <td>https://bj.lianjia.com/ershoufang/101102982736...</td>
      <td>棕榈泉国际公寓</td>
      <td>中楼层(共30层)/2003年建板楼/朝阳公园</td>
      <td>4室2厅</td>
      <td>369.58</td>
      <td>南 北</td>
      <td>中楼层(共30层)/2003年建板楼/朝阳公园</td>
      <td>房本满五年</td>
      <td>4180.0</td>
      <td>113102</td>
      <td>86人关注/2次带看近地铁房本满五年4180万单价113102元/平米</td>
      <td>精装</td>
      <td>16:29.8</td>
      <td>116.425310,39.995172</td>
    </tr>
    <tr>
      <th>384</th>
      <td>1.011010e+11</td>
      <td>海晟名苑南区 3室2厅 4000万</td>
      <td>https://bj.lianjia.com/ershoufang/101100826453...</td>
      <td>海晟名苑南区</td>
      <td>顶层(共22层)/2004年建板塔结合/工体</td>
      <td>3室2厅</td>
      <td>305.54</td>
      <td>东 南 西 北</td>
      <td>顶层(共22层)/2004年建板塔结合/工体</td>
      <td>房本满五年</td>
      <td>4000.0</td>
      <td>130916</td>
      <td>180人关注/0次带看房本满五年4000万单价130916元/平米</td>
      <td>简装</td>
      <td>10:54.9</td>
      <td>116.441909,39.937691</td>
    </tr>
    <tr>
      <th>7125</th>
      <td>1.011030e+11</td>
      <td>星河湾 4室2厅 4000万</td>
      <td>https://bj.lianjia.com/ershoufang/101103054106...</td>
      <td>星河湾</td>
      <td>低楼层(共12层)/2006年建板楼/朝青</td>
      <td>4室2厅</td>
      <td>426.16</td>
      <td>南 北</td>
      <td>低楼层(共12层)/2006年建板楼/朝青</td>
      <td>房本满五年</td>
      <td>4000.0</td>
      <td>93862</td>
      <td>71人关注/0次带看近地铁房本满五年4000万单价93862元/平米</td>
      <td>精装</td>
      <td>17:25.4</td>
      <td>116.523310,39.928504</td>
    </tr>
    <tr>
      <th>4087</th>
      <td>1.011030e+11</td>
      <td>北二环内=什刹海区域=和政客明星做邻居=六层板楼电梯</td>
      <td>https://bj.lianjia.com/ershoufang/101103020559...</td>
      <td>丽豪园</td>
      <td>顶层(共6层)/1999年建板楼/六铺炕</td>
      <td>5室3厅</td>
      <td>289.65</td>
      <td>南 西 北</td>
      <td>顶层(共6层)/1999年建板楼/六铺炕</td>
      <td>房本满五年</td>
      <td>3999.0</td>
      <td>138064</td>
      <td>60人关注/0次带看房本满五年3999万单价138064元/平米</td>
      <td>精装</td>
      <td>14:26.2</td>
      <td>116.388296,39.947370</td>
    </tr>
  </tbody>
</table>

</div>

## 数据2：单价前十的二手房源

```
unitHighest10 = house.sort_values('unitPrice',ascending=False).head(10)
display(unitHighest10)
unitHighest10.to_csv("output/unitHighest10.csv",index=False,sep=',')
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

```
.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
```

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>houseID</th>
      <th>title</th>
      <th>link</th>
      <th>community</th>
      <th>years</th>
      <th>housetype</th>
      <th>square</th>
      <th>direction</th>
      <th>floor</th>
      <th>taxtype</th>
      <th>totalPrice</th>
      <th>unitPrice</th>
      <th>followInfo</th>
      <th>decoration</th>
      <th>validdate</th>
      <th>coor_xy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3193</th>
      <td>1.011030e+11</td>
      <td>广电部 新小区 南向一居室 管理好 环境好</td>
      <td>https://bj.lianjia.com/ershoufang/101103064332...</td>
      <td>北滨河路2号院</td>
      <td>中楼层(共16层)/1992年建塔楼/木樨地</td>
      <td>1室1厅</td>
      <td>53.80</td>
      <td>南</td>
      <td>中楼层(共16层)/1992年建塔楼/木樨地</td>
      <td>房本满五年</td>
      <td>806.9</td>
      <td>149982</td>
      <td>4人关注/2次带看近地铁房本满五年806.9万单价149982元/平米</td>
      <td>其他</td>
      <td>13:34.1</td>
      <td>116.351199,39.900688</td>
    </tr>
    <tr>
      <th>3502</th>
      <td>1.011020e+11</td>
      <td>西城广安门 三期复式 挑高5.2米 带赠送面积 采光好</td>
      <td>https://bj.lianjia.com/ershoufang/101102397536...</td>
      <td>荣丰2008</td>
      <td>高楼层(共16层)/2007年建塔楼/广安门</td>
      <td>1室1厅</td>
      <td>31.14</td>
      <td>西</td>
      <td>高楼层(共16层)/2007年建塔楼/广安门</td>
      <td>房本满五年</td>
      <td>467.0</td>
      <td>149968</td>
      <td>200人关注/0次带看近地铁房本满两年467万单价149968元/平米</td>
      <td>精装</td>
      <td>13:51.8</td>
      <td>116.336616,39.894695</td>
    </tr>
    <tr>
      <th>1504</th>
      <td>1.011030e+11</td>
      <td>磁器库南巷 1室1厅 666万</td>
      <td>https://bj.lianjia.com/ershoufang/101103495318...</td>
      <td>磁器库南巷</td>
      <td>底层(共1层)/2003年建板楼/东单</td>
      <td>1室1厅</td>
      <td>44.41</td>
      <td>北</td>
      <td>底层(共1层)/2003年建板楼/东单</td>
      <td>房本满五年</td>
      <td>666.0</td>
      <td>149967</td>
      <td>10人关注/7次带看近地铁房本满两年666万单价149967元/平米</td>
      <td>精装</td>
      <td>11:56.9</td>
      <td>116.406165,39.913017</td>
    </tr>
    <tr>
      <th>3365</th>
      <td>1.011030e+11</td>
      <td>满五年唯一，两层复式，有露台，精装修</td>
      <td>https://bj.lianjia.com/ershoufang/101103445496...</td>
      <td>阳光丽景</td>
      <td>中楼层(共18层)/2003年建板塔结合/马甸</td>
      <td>5室2厅</td>
      <td>235.59</td>
      <td>南 北</td>
      <td>中楼层(共18层)/2003年建板塔结合/马甸</td>
      <td>房本满五年</td>
      <td>3533.0</td>
      <td>149964</td>
      <td>95人关注/7次带看房本满五年3533万单价149964元/平米</td>
      <td>精装</td>
      <td>13:44.9</td>
      <td>116.385834,39.964424</td>
    </tr>
    <tr>
      <th>2650</th>
      <td>1.011030e+11</td>
      <td>西城德胜2002年的小区  南北大两居 看房随时 随时签约</td>
      <td>https://bj.lianjia.com/ershoufang/101103109420...</td>
      <td>新外大街乙8号院</td>
      <td>高楼层(共7层)/2002年建板楼/马甸</td>
      <td>2室1厅</td>
      <td>77.82</td>
      <td>南 北</td>
      <td>高楼层(共7层)/2002年建板楼/马甸</td>
      <td>房本满五年</td>
      <td>1167.0</td>
      <td>149962</td>
      <td>14人关注/6次带看随时看房1167万单价149962元/平米</td>
      <td>精装</td>
      <td>13:02.4</td>
      <td>116.372214,39.962012</td>
    </tr>
    <tr>
      <th>3659</th>
      <td>1.011030e+11</td>
      <td>朱雀门 南北两居 全明格局 看房方便随时签约</td>
      <td>https://bj.lianjia.com/ershoufang/101103415542...</td>
      <td>朱雀门</td>
      <td>中楼层(共8层)/2009年建板楼/陶然亭</td>
      <td>2室2厅</td>
      <td>105.03</td>
      <td>南 北</td>
      <td>中楼层(共8层)/2009年建板楼/陶然亭</td>
      <td>房本满五年</td>
      <td>1575.0</td>
      <td>149958</td>
      <td>13人关注/6次带看1575万单价149958元/平米</td>
      <td>精装</td>
      <td>14:02.0</td>
      <td>116.388148,39.875875</td>
    </tr>
    <tr>
      <th>4408</th>
      <td>1.011030e+11</td>
      <td>金融街 西城晶华 东南方正两居室 朝向好 户型方正</td>
      <td>https://bj.lianjia.com/ershoufang/101103429009...</td>
      <td>西城晶华</td>
      <td>底层(共11层)/2008年建板塔结合/金融街</td>
      <td>2室2厅</td>
      <td>116.58</td>
      <td>东南</td>
      <td>底层(共11层)/2008年建板塔结合/金融街</td>
      <td>房本满五年</td>
      <td>1748.0</td>
      <td>149940</td>
      <td>51人关注/3次带看近地铁1748万单价149940元/平米</td>
      <td>精装</td>
      <td>14:45.4</td>
      <td>116.365869,39.921067</td>
    </tr>
    <tr>
      <th>2841</th>
      <td>1.011030e+11</td>
      <td>房子带两个地下车位满五年家庭唯一采光视野好封闭管理</td>
      <td>https://bj.lianjia.com/ershoufang/101102647932...</td>
      <td>阳光丽景</td>
      <td>顶层(共19层)/2003年建塔楼/马甸</td>
      <td>4室2厅</td>
      <td>153.41</td>
      <td>南</td>
      <td>顶层(共19层)/2003年建塔楼/马甸</td>
      <td>房本满五年</td>
      <td>2300.0</td>
      <td>149926</td>
      <td>221人关注/18次带看房本满五年2300万单价149926元/平米</td>
      <td>精装</td>
      <td>13:14.2</td>
      <td>116.385834,39.964424</td>
    </tr>
    <tr>
      <th>12018</th>
      <td>1.011030e+11</td>
      <td>万柳 碧水云天双南向两居室 诚意出售</td>
      <td>https://bj.lianjia.com/ershoufang/101103002322...</td>
      <td>碧水云天</td>
      <td>低楼层(共16层)/2003年建塔楼/万柳</td>
      <td>2室1厅</td>
      <td>66.70</td>
      <td>南</td>
      <td>低楼层(共16层)/2003年建塔楼/万柳</td>
      <td>房本满五年</td>
      <td>1000.0</td>
      <td>149926</td>
      <td>20人关注/11次带看房本满五年1000万单价149926元/平米</td>
      <td>精装</td>
      <td>22:14.8</td>
      <td>116.492708,39.880533</td>
    </tr>
    <tr>
      <th>3574</th>
      <td>1.011030e+11</td>
      <td>西城区 地铁达官营站 荣丰2008三期复式出售</td>
      <td>https://bj.lianjia.com/ershoufang/101103247746...</td>
      <td>荣丰2008</td>
      <td>中楼层(共16层)/2007年建塔楼/广安门</td>
      <td>1室1厅</td>
      <td>31.35</td>
      <td>东</td>
      <td>中楼层(共16层)/2007年建塔楼/广安门</td>
      <td>房本满五年</td>
      <td>470.0</td>
      <td>149921</td>
      <td>36人关注/0次带看近地铁房本满两年470万单价149921元/平米</td>
      <td>其他</td>
      <td>13:56.8</td>
      <td>116.336616,39.894695</td>
    </tr>
  </tbody>
</table>

</div>

## 数据3：关注人数最多10套二手房源

```
house['guanzhu'] = house['followInfo'].apply(data_adj,str = '人关注')
guanzhuHighest10 = house.sort_values('guanzhu',ascending=False).head(10)
display(guanzhuHighest10)
guanzhuHighest10.to_csv("output/guanzhuHighest10.csv",index=False,sep=',')
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

```
.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
```

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>houseID</th>
      <th>title</th>
      <th>link</th>
      <th>community</th>
      <th>years</th>
      <th>housetype</th>
      <th>square</th>
      <th>direction</th>
      <th>floor</th>
      <th>taxtype</th>
      <th>totalPrice</th>
      <th>unitPrice</th>
      <th>followInfo</th>
      <th>decoration</th>
      <th>validdate</th>
      <th>coor_xy</th>
      <th>guanzhu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4872</th>
      <td>1.011030e+11</td>
      <td>华纺东区 南北通透 次顶层 无个税 有钥匙</td>
      <td>https://bj.lianjia.com/ershoufang/101103060299...</td>
      <td>华纺易城</td>
      <td>高楼层(共18层)/2005年建板塔结合/朝青</td>
      <td>2室1厅</td>
      <td>94.06</td>
      <td>南 北</td>
      <td>高楼层(共18层)/2005年建板塔结合/朝青</td>
      <td>房本满五年</td>
      <td>745.0</td>
      <td>79205</td>
      <td>16772人关注/11次带看近地铁房本满五年745万单价79205元/平米</td>
      <td>精装</td>
      <td>15:14.8</td>
      <td>116.514192,39.929839</td>
      <td>16772.0</td>
    </tr>
    <tr>
      <th>2095</th>
      <td>1.011030e+11</td>
      <td>新街口平安里南北通透满五唯一 有钥匙随时看 独立管理</td>
      <td>https://bj.lianjia.com/ershoufang/101103130761...</td>
      <td>大乘巷</td>
      <td>高楼层(共6层)/1989年建板楼/官园</td>
      <td>2室1厅</td>
      <td>59.60</td>
      <td>南 北</td>
      <td>高楼层(共6层)/1989年建板楼/官园</td>
      <td>房本满五年</td>
      <td>715.0</td>
      <td>119967</td>
      <td>13479人关注/33次带看近地铁房本满五年随时看房715万单价119967元/平米</td>
      <td>简装</td>
      <td>12:32.5</td>
      <td>116.366230,39.935495</td>
      <td>13479.0</td>
    </tr>
    <tr>
      <th>2091</th>
      <td>1.011030e+11</td>
      <td>北京西城月坛99年南北通透大两居，双阳台，采光无遮挡</td>
      <td>https://bj.lianjia.com/ershoufang/101103229329...</td>
      <td>月坛北街25号院</td>
      <td>底层(共6层)/1999年建板楼/月坛</td>
      <td>2室1厅</td>
      <td>77.70</td>
      <td>南 北</td>
      <td>底层(共6层)/1999年建板楼/月坛</td>
      <td>房本满五年</td>
      <td>980.0</td>
      <td>126127</td>
      <td>9121人关注/27次带看近地铁房本满五年随时看房980万单价126127元/平米</td>
      <td>精装</td>
      <td>12:32.5</td>
      <td>116.338548,39.920261</td>
      <td>9121.0</td>
    </tr>
    <tr>
      <th>7625</th>
      <td>1.011000e+11</td>
      <td>角门东里两居，格局好，楼层好，业主诚心卖</td>
      <td>https://bj.lianjia.com/ershoufang/101100452567...</td>
      <td>角门东里</td>
      <td>高楼层(共19层)/1995年建塔楼/角门</td>
      <td>2室1厅</td>
      <td>62.65</td>
      <td>东南</td>
      <td>高楼层(共19层)/1995年建塔楼/角门</td>
      <td>房本满五年</td>
      <td>380.0</td>
      <td>60655</td>
      <td>6745人关注/35次带看近地铁房本满五年随时看房380万单价60655元/平米</td>
      <td>精装</td>
      <td>17:55.2</td>
      <td>116.384616,39.847858</td>
      <td>6745.0</td>
    </tr>
    <tr>
      <th>7626</th>
      <td>1.011020e+11</td>
      <td>万科紫苑 南北通透全能小三居 精装修 保持好！</td>
      <td>https://bj.lianjia.com/ershoufang/101102299892...</td>
      <td>万科紫苑</td>
      <td>低楼层(共15层)/2011年建板楼/青塔</td>
      <td>3室2厅</td>
      <td>95.22</td>
      <td>南 北</td>
      <td>低楼层(共15层)/2011年建板楼/青塔</td>
      <td>房本满五年</td>
      <td>695.0</td>
      <td>72989</td>
      <td>5865人关注/49次带看近地铁房本满两年随时看房695万单价72989元/平米</td>
      <td>精装</td>
      <td>17:55.2</td>
      <td>116.255762,39.868997</td>
      <td>5865.0</td>
    </tr>
    <tr>
      <th>7481</th>
      <td>1.011030e+11</td>
      <td>风景club南北通透3居格局方正诚意出售</td>
      <td>https://bj.lianjia.com/ershoufang/101102731655...</td>
      <td>风景club</td>
      <td>顶层(共12层)/2007年建板楼/草桥</td>
      <td>3室1厅</td>
      <td>124.03</td>
      <td>南 北</td>
      <td>顶层(共12层)/2007年建板楼/草桥</td>
      <td>房本满五年</td>
      <td>890.0</td>
      <td>71757</td>
      <td>4794人关注/40次带看近地铁房本满五年随时看房890万单价71757元/平米</td>
      <td>精装</td>
      <td>17:48.5</td>
      <td>116.351285,39.841230</td>
      <td>4794.0</td>
    </tr>
    <tr>
      <th>7563</th>
      <td>1.011020e+11</td>
      <td>富卓苑 低楼层南北通透两居室 无遮挡</td>
      <td>https://bj.lianjia.com/ershoufang/101101502347...</td>
      <td>富卓苑</td>
      <td>低楼层(共6层)/2000年建板楼/马家堡</td>
      <td>2室1厅</td>
      <td>69.59</td>
      <td>南 北</td>
      <td>低楼层(共6层)/2000年建板楼/马家堡</td>
      <td>房本满五年</td>
      <td>450.0</td>
      <td>64665</td>
      <td>4569人关注/15次带看近地铁房本满五年随时看房450万单价64665元/平米</td>
      <td>简装</td>
      <td>17:51.9</td>
      <td>116.378235,39.838490</td>
      <td>4569.0</td>
    </tr>
    <tr>
      <th>6070</th>
      <td>1.011000e+11</td>
      <td>弘善家园南向开间，满两年，免增值税</td>
      <td>https://bj.lianjia.com/ershoufang/101100379913...</td>
      <td>弘善家园</td>
      <td>中楼层(共28层)/2009年建塔楼/潘家园</td>
      <td>1室0厅</td>
      <td>42.64</td>
      <td>南</td>
      <td>中楼层(共28层)/2009年建塔楼/潘家园</td>
      <td>房本满五年</td>
      <td>260.0</td>
      <td>60976</td>
      <td>3978人关注/16次带看近地铁房本满两年随时看房260万单价60976元/平米</td>
      <td>毛坯</td>
      <td>16:22.8</td>
      <td>116.453958,39.867764</td>
      <td>3978.0</td>
    </tr>
    <tr>
      <th>5142</th>
      <td>1.011020e+11</td>
      <td>北工大 禧福汇小区 南北三居 满五年 业主诚售</td>
      <td>https://bj.lianjia.com/ershoufang/101102015306...</td>
      <td>禧福汇</td>
      <td>高楼层(共20层)/2008年建板塔结合/北工大</td>
      <td>3室1厅</td>
      <td>139.66</td>
      <td>南 北</td>
      <td>高楼层(共20层)/2008年建板塔结合/北工大</td>
      <td>房本满五年</td>
      <td>1170.0</td>
      <td>83775</td>
      <td>3454人关注/27次带看近地铁房本满五年随时看房1170万单价83775元/平米</td>
      <td>精装</td>
      <td>15:29.9</td>
      <td>116.475102,39.883100</td>
      <td>3454.0</td>
    </tr>
    <tr>
      <th>11791</th>
      <td>1.011030e+11</td>
      <td>时尚大两居，观景落地飘窗，视野广阔，采光好</td>
      <td>https://bj.lianjia.com/ershoufang/101103177623...</td>
      <td>中国房子</td>
      <td>9层/2005年建板楼/田村</td>
      <td>2室2厅</td>
      <td>112.28</td>
      <td>南</td>
      <td>9层/2005年建板楼/田村</td>
      <td>房本满五年</td>
      <td>810.0</td>
      <td>72142</td>
      <td>3298人关注/15次带看房本满五年随时看房810万单价72142元/平米</td>
      <td>简装</td>
      <td>22:01.4</td>
      <td>116.304548,39.929429</td>
      <td>3298.0</td>
    </tr>
  </tbody>
</table>

</div>

## 数据4：二手房户型和关注人数的分布关系

```
plt.figure(dpi = 600)
fig, ax1 = plt.subplots(1,1)    
type_interest_group = house['guanzhu'].groupby(house['housetype']).agg([('户型', 'count'), ('关注人数', 'sum')])    
ti_sort = type_interest_group[type_interest_group['户型'] > 50].sort_values(by='户型') #取户型>50的数据
ti_sort.plot(kind='barh', grid=True, ax=ax1)    
plt.title('二手房户型和关注人数的分布关系')    
plt.ylabel('户型') 
plt.show()
fig.savefig("output/二手房户型和关注人数的分布关系.png")
```

## 数据5：二手房源的面积分布

```
plt.figure(dpi = 600)
fig,ax2 = plt.subplots(1,1)    
area_level = [0, 50, 100, 150, 200, 250, 300, 500]    
label_level = ['小于50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350']    
area_cut = pd.cut(house['square'], area_level, labels=label_level)        
area_cut.value_counts().plot(kind='bar', grid=True,ax=ax2)    
plt.title('二手房面积分布')    
plt.xlabel('面积')    
plt.legend(['数量'])    
plt.show()
fig.savefig("output/二手房面积分布.png")
```

## 数据6：关于二手房源面积与总价的聚类分析

```
# 缺失值处理:直接将缺失值去掉    
cluster_data = house[['guanzhu','square','totalPrice']].dropna()    
#将簇数设为3    
K_model = KMeans(n_clusters=6)    
alg = K_model.fit(cluster_data)    
'------聚类中心------'   
center = pd.DataFrame(alg.cluster_centers_, columns=['关注人数','面积','房价'])    
cluster_data['label'] = alg.labels_ 
center
```



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

```
.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
```

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>关注人数</th>
      <th>面积</th>
      <th>房价</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3241.772727</td>
      <td>92.472273</td>
      <td>673.863636</td>
    </tr>
    <tr>
      <th>1</th>
      <td>63.319779</td>
      <td>100.160623</td>
      <td>802.086608</td>
    </tr>
    <tr>
      <th>2</th>
      <td>79.700000</td>
      <td>242.123839</td>
      <td>2562.903226</td>
    </tr>
    <tr>
      <th>3</th>
      <td>13124.000000</td>
      <td>77.120000</td>
      <td>813.333333</td>
    </tr>
    <tr>
      <th>4</th>
      <td>63.939607</td>
      <td>155.454452</td>
      <td>1382.082935</td>
    </tr>
    <tr>
      <th>5</th>
      <td>79.320000</td>
      <td>69.176498</td>
      <td>437.837901</td>
    </tr>
  </tbody>
</table>

</div>



## 数据7：十套面积最小的二手房源

```
smallestArea10 = house.sort_values('square',ascending=True).head(10)
display(smallestArea10)
smallestArea.to_csv("output/smallestArea10.csv",index=False,sep=',')
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

```
.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
```

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>houseID</th>
      <th>title</th>
      <th>link</th>
      <th>community</th>
      <th>years</th>
      <th>housetype</th>
      <th>square</th>
      <th>direction</th>
      <th>floor</th>
      <th>taxtype</th>
      <th>totalPrice</th>
      <th>unitPrice</th>
      <th>followInfo</th>
      <th>decoration</th>
      <th>validdate</th>
      <th>coor_xy</th>
      <th>guanzhu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>11757</th>
      <td>1.011020e+11</td>
      <td>聚兴园产权车位，诚心出售，方便看</td>
      <td>https://bj.lianjia.com/ershoufang/101102083610...</td>
      <td>聚兴园</td>
      <td>/2005年建板楼/鲁谷</td>
      <td>车位</td>
      <td>11.96</td>
      <td>东 南 西 北</td>
      <td>/2005年建板楼/鲁谷</td>
      <td>房本满五年</td>
      <td>25.0</td>
      <td>20904</td>
      <td>37人关注/0次带看房本满两年25万单价20904元/平米</td>
      <td>无电梯</td>
      <td>21:57.8</td>
      <td>116.222526,39.892695</td>
      <td>37.0</td>
    </tr>
    <tr>
      <th>11769</th>
      <td>1.011030e+11</td>
      <td>聚兴园 车位 30万</td>
      <td>https://bj.lianjia.com/ershoufang/101102917689...</td>
      <td>聚兴园</td>
      <td>/2006年建板楼/鲁谷</td>
      <td>车位</td>
      <td>13.80</td>
      <td>南 北</td>
      <td>/2006年建板楼/鲁谷</td>
      <td>房本满五年</td>
      <td>30.0</td>
      <td>21740</td>
      <td>11人关注/0次带看房本满两年30万单价21740元/平米</td>
      <td>无电梯</td>
      <td>21:57.8</td>
      <td>116.222526,39.892695</td>
      <td>11.0</td>
    </tr>
    <tr>
      <th>4434</th>
      <td>1.011030e+11</td>
      <td>西绦南巷 1室1厅 213万</td>
      <td>https://bj.lianjia.com/ershoufang/101102645058...</td>
      <td>西绦南巷</td>
      <td>底层(共1层)/2009年建暂无数据/六铺炕</td>
      <td>1室1厅</td>
      <td>15.25</td>
      <td>南</td>
      <td>底层(共1层)/2009年建暂无数据/六铺炕</td>
      <td>房本满五年</td>
      <td>213.0</td>
      <td>139673</td>
      <td>621人关注/4次带看近地铁213万单价139673元/平米</td>
      <td>简装</td>
      <td>14:47.2</td>
      <td>116.391059,39.947905</td>
      <td>621.0</td>
    </tr>
    <tr>
      <th>1474</th>
      <td>1.011020e+11</td>
      <td>华人一品阁 1房间1卫 90万</td>
      <td>https://bj.lianjia.com/ershoufang/101101915213...</td>
      <td>华人一品阁</td>
      <td>低楼层(共3层)/2006年建板塔结合/东四</td>
      <td>1房间1卫</td>
      <td>16.12</td>
      <td>南</td>
      <td>低楼层(共3层)/2006年建板塔结合/东四</td>
      <td>房本满五年</td>
      <td>90.0</td>
      <td>55832</td>
      <td>202人关注/1次带看房本满五年90万单价55832元/平米</td>
      <td>简装</td>
      <td>11:55.1</td>
      <td>116.410599,39.932952</td>
      <td>202.0</td>
    </tr>
    <tr>
      <th>1554</th>
      <td>1.011020e+11</td>
      <td>华人一品阁 1房间1卫 90万</td>
      <td>https://bj.lianjia.com/ershoufang/101101915230...</td>
      <td>华人一品阁</td>
      <td>低楼层(共3层)/2006年建板塔结合/东四</td>
      <td>1房间1卫</td>
      <td>16.12</td>
      <td>南</td>
      <td>低楼层(共3层)/2006年建板塔结合/东四</td>
      <td>房本满五年</td>
      <td>90.0</td>
      <td>55832</td>
      <td>105人关注/0次带看房本满五年90万单价55832元/平米</td>
      <td>简装</td>
      <td>11:58.6</td>
      <td>116.410599,39.932952</td>
      <td>105.0</td>
    </tr>
    <tr>
      <th>1770</th>
      <td>1.011030e+11</td>
      <td>华人一品阁 1房间1卫 110万</td>
      <td>https://bj.lianjia.com/ershoufang/101102563755...</td>
      <td>华人一品阁</td>
      <td>低楼层(共3层)/2007年建板塔结合/东四</td>
      <td>1房间1卫</td>
      <td>20.28</td>
      <td>北</td>
      <td>低楼层(共3层)/2007年建板塔结合/东四</td>
      <td>房本满五年</td>
      <td>110.0</td>
      <td>54241</td>
      <td>32人关注/0次带看110万单价54241元/平米</td>
      <td>精装</td>
      <td>12:11.7</td>
      <td>116.410599,39.932952</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>4296</th>
      <td>1.011030e+11</td>
      <td>荣丰二期小户型，西城二环居家，精装修拎包入住</td>
      <td>https://bj.lianjia.com/ershoufang/101103329581...</td>
      <td>荣丰2008</td>
      <td>低楼层(共20层)/2004年建塔楼/广安门</td>
      <td>1室0厅</td>
      <td>21.93</td>
      <td>北</td>
      <td>低楼层(共20层)/2004年建塔楼/广安门</td>
      <td>房本满五年</td>
      <td>325.0</td>
      <td>148199</td>
      <td>7人关注/1次带看近地铁房本满两年325万单价148199元/平米</td>
      <td>精装</td>
      <td>14:38.6</td>
      <td>116.336616,39.894695</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>8602</th>
      <td>1.011030e+11</td>
      <td>金色南向开间 满五年家庭名下仅一套住房</td>
      <td>https://bj.lianjia.com/ershoufang/101103405391...</td>
      <td>世纪金色嘉园</td>
      <td>低楼层(共30层)/2003年建塔楼/北京南站</td>
      <td>1室0厅</td>
      <td>23.75</td>
      <td>南</td>
      <td>低楼层(共30层)/2003年建塔楼/北京南站</td>
      <td>房本满五年</td>
      <td>219.0</td>
      <td>92211</td>
      <td>51人关注/0次带看近地铁房本满五年219万单价92211元/平米</td>
      <td>简装</td>
      <td>18:52.9</td>
      <td>116.372109,39.869255</td>
      <td>51.0</td>
    </tr>
    <tr>
      <th>3074</th>
      <td>1.011040e+11</td>
      <td>西城 荣丰2008小区  楼西南角  随时看房  正南向</td>
      <td>https://bj.lianjia.com/ershoufang/101103528644...</td>
      <td>荣丰2008</td>
      <td>高楼层(共26层)/2006年建塔楼/广安门</td>
      <td>1室0厅</td>
      <td>23.80</td>
      <td>南</td>
      <td>高楼层(共26层)/2006年建塔楼/广安门</td>
      <td>房本满五年</td>
      <td>320.0</td>
      <td>134454</td>
      <td>27人关注/23次带看近地铁随时看房320万单价134454元/平米</td>
      <td>简装</td>
      <td>13:27.3</td>
      <td>116.336616,39.894695</td>
      <td>27.0</td>
    </tr>
    <tr>
      <th>4072</th>
      <td>1.011030e+11</td>
      <td>荣丰南向开间 中间层 满五年 业主诚售</td>
      <td>https://bj.lianjia.com/ershoufang/101103099015...</td>
      <td>荣丰2008</td>
      <td>中楼层(共26层)/2006年建塔楼/广安门</td>
      <td>1室0厅</td>
      <td>23.80</td>
      <td>南</td>
      <td>中楼层(共26层)/2006年建塔楼/广安门</td>
      <td>房本满五年</td>
      <td>335.0</td>
      <td>140757</td>
      <td>74人关注/3次带看近地铁房本满五年335万单价140757元/平米</td>
      <td>精装</td>
      <td>14:26.2</td>
      <td>116.336616,39.894695</td>
      <td>74.0</td>
    </tr>
  </tbody>
</table>

</div>

## 数据8：十套面积最大二手房源

```
largestArea10 = house.sort_values('square',ascending=False).head(10)
display(largestArea10)
largestArea.to_csv("output/largestArea10.csv",index=False,sep=',')
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

```
.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
```

</style>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>houseID</th>
      <th>title</th>
      <th>link</th>
      <th>community</th>
      <th>years</th>
      <th>housetype</th>
      <th>square</th>
      <th>direction</th>
      <th>floor</th>
      <th>taxtype</th>
      <th>totalPrice</th>
      <th>unitPrice</th>
      <th>followInfo</th>
      <th>decoration</th>
      <th>validdate</th>
      <th>coor_xy</th>
      <th>guanzhu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>11523</th>
      <td>1.011030e+11</td>
      <td>庐师山庄联排别墅 独立小庭院 上下三层 诚心出售</td>
      <td>https://bj.lianjia.com/ershoufang/101103114726...</td>
      <td>庐师山庄</td>
      <td>2层/2006年建暂无数据/苹果园</td>
      <td>5室2厅</td>
      <td>535.31</td>
      <td>南 北</td>
      <td>2层/2006年建暂无数据/苹果园</td>
      <td>房本满五年</td>
      <td>3300.0</td>
      <td>61647</td>
      <td>30人关注/1次带看房本满五年3300万单价61647元/平米</td>
      <td>其他</td>
      <td>21:44.2</td>
      <td>116.195319,39.942990</td>
      <td>30.0</td>
    </tr>
    <tr>
      <th>3416</th>
      <td>1.011020e+11</td>
      <td>配套齐全，楼龄新，三层复式，业主诚心出售</td>
      <td>https://bj.lianjia.com/ershoufang/101102231681...</td>
      <td>立恒名苑</td>
      <td>高楼层(共24层)/2002年建塔楼/天宁寺</td>
      <td>7室3厅</td>
      <td>532.82</td>
      <td>南 西 北</td>
      <td>高楼层(共24层)/2002年建塔楼/天宁寺</td>
      <td>房本满五年</td>
      <td>2480.0</td>
      <td>46545</td>
      <td>97人关注/4次带看房本满五年随时看房2480万单价46545元/平米</td>
      <td>其他</td>
      <td>13:46.6</td>
      <td>116.347683,39.883466</td>
      <td>97.0</td>
    </tr>
    <tr>
      <th>1185</th>
      <td>1.011020e+11</td>
      <td>金宝街 70年产权大四居 视野开阔 朝向好 大户型！</td>
      <td>https://bj.lianjia.com/ershoufang/101101814319...</td>
      <td>建国门北大街5号</td>
      <td>高楼层(共24层)/2008年建塔楼/建国门内</td>
      <td>4室1厅</td>
      <td>508.74</td>
      <td>东 南 西</td>
      <td>高楼层(共24层)/2008年建塔楼/建国门内</td>
      <td>房本满五年</td>
      <td>2900.0</td>
      <td>57004</td>
      <td>136人关注/0次带看近地铁房本满五年随时看房2900万单价57004元/平米</td>
      <td>精装</td>
      <td>11:39.0</td>
      <td>116.433714,39.914319</td>
      <td>136.0</td>
    </tr>
    <tr>
      <th>1860</th>
      <td>1.011030e+11</td>
      <td>东单灯市口 霞公府 南北向4居 诚意出售 高楼层</td>
      <td>https://bj.lianjia.com/ershoufang/101103153250...</td>
      <td>霞公府</td>
      <td>中楼层(共7层)/2011年建板楼/东单</td>
      <td>4室2厅</td>
      <td>497.57</td>
      <td>南 北</td>
      <td>中楼层(共7层)/2011年建板楼/东单</td>
      <td>房本满五年</td>
      <td>6688.0</td>
      <td>134414</td>
      <td>196人关注/2次带看近地铁6688万单价134414元/平米</td>
      <td>精装</td>
      <td>12:16.7</td>
      <td>116.408453,39.909869</td>
      <td>196.0</td>
    </tr>
    <tr>
      <th>7100</th>
      <td>1.011030e+11</td>
      <td>外交部南街京华豪园复式，改善客户购买，70年住宅产权</td>
      <td>https://bj.lianjia.com/ershoufang/101102754825...</td>
      <td>京华豪园</td>
      <td>顶层(共21层)/2000年建塔楼/朝阳门外</td>
      <td>6室3厅</td>
      <td>483.70</td>
      <td>西 西北 北</td>
      <td>顶层(共21层)/2000年建塔楼/朝阳门外</td>
      <td>房本满五年</td>
      <td>2600.0</td>
      <td>53753</td>
      <td>112人关注/0次带看近地铁房本满五年2600万单价53753元/平米</td>
      <td>简装</td>
      <td>17:23.7</td>
      <td>116.436700,39.917794</td>
      <td>112.0</td>
    </tr>
    <tr>
      <th>3587</th>
      <td>1.011030e+11</td>
      <td>五栋大楼，南北通透，顶层复式，带电梯</td>
      <td>https://bj.lianjia.com/ershoufang/101102655114...</td>
      <td>五栋大楼</td>
      <td>高楼层(共16层)/2005年建板塔结合/车公庄</td>
      <td>5室3厅</td>
      <td>462.94</td>
      <td>南 西 北</td>
      <td>高楼层(共16层)/2005年建板塔结合/车公庄</td>
      <td>房本满五年</td>
      <td>2540.0</td>
      <td>54867</td>
      <td>107人关注/1次带看近地铁房本满五年随时看房2540万单价54867元/平米</td>
      <td>精装</td>
      <td>13:56.8</td>
      <td>116.348656,39.933556</td>
      <td>107.0</td>
    </tr>
    <tr>
      <th>1199</th>
      <td>1.011030e+11</td>
      <td>北二环 中轴国际 高层观景房 平层一梯一户</td>
      <td>https://bj.lianjia.com/ershoufang/101103070630...</td>
      <td>中轴国际</td>
      <td>高楼层(共21层)/2005年建板楼/安定门</td>
      <td>4室4厅</td>
      <td>452.80</td>
      <td>南 西北</td>
      <td>高楼层(共21层)/2005年建板楼/安定门</td>
      <td>房本满五年</td>
      <td>4972.0</td>
      <td>109806</td>
      <td>83人关注/0次带看近地铁房本满五年4972万单价109806元/平米</td>
      <td>精装</td>
      <td>11:40.5</td>
      <td>116.400677,39.950142</td>
      <td>83.0</td>
    </tr>
    <tr>
      <th>1970</th>
      <td>1.011020e+11</td>
      <td>东城区凯德华玺封闭式管理西南向带露台</td>
      <td>https://bj.lianjia.com/ershoufang/101102182731...</td>
      <td>凯德华玺</td>
      <td>低楼层(共14层)/2008年建塔楼/金宝街</td>
      <td>6房间5卫</td>
      <td>439.04</td>
      <td>南 北</td>
      <td>低楼层(共14层)/2008年建塔楼/金宝街</td>
      <td>房本满五年</td>
      <td>3500.0</td>
      <td>79720</td>
      <td>43人关注/1次带看近地铁房本满五年3500万单价79720元/平米</td>
      <td>精装</td>
      <td>12:21.7</td>
      <td>116.420545,39.923876</td>
      <td>43.0</td>
    </tr>
    <tr>
      <th>8756</th>
      <td>1.011030e+11</td>
      <td>中海九号公馆 5室3厅 3100万</td>
      <td>https://bj.lianjia.com/ershoufang/101102507319...</td>
      <td>中海九号公馆</td>
      <td>3层/2012年建暂无数据/科技园区</td>
      <td>5室3厅</td>
      <td>437.46</td>
      <td>南 北</td>
      <td>3层/2012年建暂无数据/科技园区</td>
      <td>房本满五年</td>
      <td>3100.0</td>
      <td>70864</td>
      <td>32人关注/5次带看近地铁房本满两年随时看房3100万单价70864元/平米</td>
      <td>毛坯</td>
      <td>19:01.4</td>
      <td>116.295990,39.817889</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>12241</th>
      <td>1.011030e+11</td>
      <td>业主诚售西山壹号院精装修一层下跃</td>
      <td>https://bj.lianjia.com/ershoufang/101102503341...</td>
      <td>西山壹号院</td>
      <td>底层(共6层)/2013年建板楼/西北旺</td>
      <td>4室3厅</td>
      <td>435.24</td>
      <td>南 北</td>
      <td>底层(共6层)/2013年建板楼/西北旺</td>
      <td>房本满五年</td>
      <td>3500.0</td>
      <td>80416</td>
      <td>67人关注/9次带看房本满两年随时看房3500万单价80416元/平米</td>
      <td>精装</td>
      <td>22:27.0</td>
      <td>116.268596,40.040056</td>
      <td>67.0</td>
    </tr>
  </tbody>
</table>

</div>

## 各个区域均价排序

```
bizcircle_unitprice=house_detail.groupby('bizcircle').mean()['unitPrice'].sort_values(ascending=False)
bizcircle_unitprice.head(20).plot(kind='bar',x='bizcircle',y='unitPrice', title='各个区域均价分布')
plt.legend(['均价']) 
plt.show()
```

```
---------------------------------------------------------------------------

TypeError                                 Traceback (most recent call last)

<ipython-input-29-9dd737c25e14> in <module>()
      1 bizcircle_unitprice=house_detail.groupby('bizcircle').mean()['unitPrice'].sort_values(ascending=False)
----> 2 bizcircle_unitprice.head(20).plot(kind='bar',x='bizcircle',y='unitPrice', title='各个区域均价分布')
      3 plt.legend(['均价'])
      4 plt.show()
```

```
~\AppData\Local\Programs\Python\Python36\lib\site-packages\pandas\plotting\_core.py in __call__(self, kind, ax, figsize, use_index, title, grid, legend, style, logx, logy, loglog, xticks, yticks, xlim, ylim, rot, fontsize, colormap, table, yerr, xerr, label, secondary_y, **kwds)
   2739                            colormap=colormap, table=table, yerr=yerr,
   2740                            xerr=xerr, label=label, secondary_y=secondary_y,
-> 2741                            **kwds)
   2742     __call__.__doc__ = plot_series.__doc__
   2743 
```

```
~\AppData\Local\Programs\Python\Python36\lib\site-packages\pandas\plotting\_core.py in plot_series(data, kind, ax, figsize, use_index, title, grid, legend, style, logx, logy, loglog, xticks, yticks, xlim, ylim, rot, fontsize, colormap, table, yerr, xerr, label, secondary_y, **kwds)
   2000                  yerr=yerr, xerr=xerr,
   2001                  label=label, secondary_y=secondary_y,
-> 2002                  **kwds)
   2003 
   2004 
```

```
~\AppData\Local\Programs\Python\Python36\lib\site-packages\pandas\plotting\_core.py in _plot(data, x, y, subplots, ax, kind, **kwds)
   1802         plot_obj = klass(data, subplots=subplots, ax=ax, kind=kind, **kwds)
   1803 
-> 1804     plot_obj.generate()
   1805     plot_obj.draw()
   1806     return plot_obj.result
```

```
~\AppData\Local\Programs\Python\Python36\lib\site-packages\pandas\plotting\_core.py in generate(self)
    256     def generate(self):
    257         self._args_adjust()
--> 258         self._compute_plot_data()
    259         self._setup_subplots()
    260         self._make_plot()
```

```
~\AppData\Local\Programs\Python\Python36\lib\site-packages\pandas\plotting\_core.py in _compute_plot_data(self)
    371         if is_empty:
    372             raise TypeError('Empty {0!r}: no numeric data to '
--> 373                             'plot'.format(numeric_data.__class__.__name__))
    374 
    375         self.data = numeric_data
```

```
TypeError: Empty 'DataFrame': no numeric data to plot
```

## 各个区域小区数量

```
bizcircle_community=community.groupby('bizcircle')['title'].size().sort_values(ascending=False)
bizcircle_community.head(20).plot(kind='bar', x='bizcircle',y='size', title='各个区域小区数量分布')
plt.legend(['数量']) 
plt.show()
```

## 按小区均价排序

```
community_unitprice = house.groupby('community').mean()['unitPrice'].sort_values(ascending=False)
community_unitprice.head(15).plot(kind='bar',x='community',y='unitPrice', title='各个小区均价分布')
plt.legend(['均价']) 
plt.show()
```