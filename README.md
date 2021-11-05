## 1120173454_徐德轩_第三次选做作业_hw4

### 一、爬虫工具调研

----------------

+ **Beautifulsoup**
> Beautiful Soup 一种设计用于实现 Web 爬取等快速数据获取项目的 Python 软件库。它在设计上处于 HTML 或 XML 解析器之上，提供用于迭代、搜索和修改解析树等功能的 Python 操作原语。往往能为开发人员节省数小时乃至数天的工作。[官方链接](https://www.crummy.com/software/BeautifulSoup/)

+ **Scrapy**
> Scrapy 是一种高速的高层 Web 爬取和 Web 采集 Python 框架，可用于爬取网站页面，并从页面中抽取结构化数据。Scrapy 的用途广泛，适用于从数据挖掘、监控到自动化测试。Scrapy 设计上考虑了从网站抽取特定的信息，它支持使用CSS 选择器和 XPath 表达式，使开发人员可以聚焦于实现数据抽取。[官方链接](https://scrapy.org/)

+  **Apache Nutch**

> Apache Nutch 是一种高度可扩展、可伸缩的开源 Web 爬虫 Java 软件项目。作为一种用于数据挖掘的高度可扩展、可伸缩的开源代码 Web 数据抽取软件项目，Apache Nutch 得到了广泛的使用。[官方链接](http://nutch.apache.org/)

+ **Crawler4j**

> crawler4j 是一种 Java 编写的开源 Web 爬虫，提供了爬取 Web 网站的基本接口。开发人员可以使用 crawler4j 在数分钟内建立一个多线程 Web 爬虫。[官方网站](https://github.com/yasserg/crawler4j)

+ **NodeCrawler**
> NodeCrawler 是一种广为使用的 Web 爬虫，它基于 NodeJS 实现，具有非常快的爬取速度。Nodecrawler 非常适用于偏爱使用JavaScript 编程或者致力于 JavaScript 项目的开发人员。其安装也非常简单。[官方链接](http://nodecrawler.org/)

+ **Simplecrawler**
> Simplecrawler 设计提供基本的、灵活且稳定的网站爬取 API。Simplecrawler 在实现上考虑了针对特大型 Web 站点的归档、分析和搜索。它可爬取上百万页面，并毫无问题地向磁盘写入数十 GB 数据。[官方链接](https://www.npmjs.com/package/simplecrawler)

+ **gigablast**
> Gigablast 是一种开源的 Web 和企业搜索引擎，也是一种爬虫，使用 C++编写。Gigablast 是自身维护数十亿页面检索索引的数家美国搜索引擎之一。[官方链接](http://www.gigablast.com/)




### 二、 自己动手写爬虫

__________________

#### 任务目标

+ **爬取有问必答网（https://www.120ask.com）中的疾病数据库信息**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;有问必答网是一个医疗服务网站，提供医疗数据信息与医生在线问诊服务。数据量充足且庞大，可以满足多种医学相关信息的需求。同时可以很方便地让数据挖掘人员进行爬虫。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在本次任务中，我们将分析有问必答网的疾病库页面，爬取页面中包含的全部疾病，并将其下载到本地，存储成json格式的文件。

#### 页面分析

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;有问必答网的疾病库页面的样子如下：

![疾病库界面截图](static/疾病库界面截图.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我们查看其HTML元素结构如下：

![HTML界面截图](static/HTML界面截图.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;进入每一科室负责的疾病给出的链接属性 "_href_ "中我们可以访问到对应科室的疾病的页面，里面包含了该科室下全部疾病的名称和对应网页链接。我们可以进入到每一个疾病的信息网页，结果如下：

![疾病症状信息](static/疾病症状信息.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在该网页中我们可以看到我们想要得到的关于疾病的全部信息，如常见症状、治疗方法、好发人群、治愈率等等。

#### 代码实现

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本任务中我们采用的是python的**requests**库提供网络请求功能，并使用**BeautifulSoup**对html页面进行解析，分析页面并应对一些反爬虫机制。

+ 设置user-agent：有问必答网设置了对user-agent的筛选，当我们在爬虫代码中未设置user-agent的时候，会提示requests.exceptions.ConnectionError: HTTPSConnectionPool，会判断出当前操作非通过浏览器访问。因此，我们在代码中添加如下代码块：
```python
header = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:70.0) Gecko/20100101 Firefox/70.0'
}

html = requests.get(dict_info["first_url"],headers=headers)
```
+ 设置代理池：本次任务幸运地未出现限制ip访问次数的问题，经过查询学习，得知可以通过代理池方法防止限制ip对爬虫程序的效果影响。
&nbsp;
+ 一些异常错误：有的时候网页会出现html结构与其他情况不一致的问题，这个时候会阻断我们的程序持久化运行，因此我们需要使用try-except代码抓取异常情况，保证代码可以不由于极少情况的格式问题而停止。
&nbsp;
+ 避免重复爬取：代码中我们设置并记录当前进度情况，当程序意外中断时，我们需要从上次进度处继续进行。
&nbsp;
+ 项目地址：[github链接](https://github.com/heavenbirdxdx/DataProcessHW4)

#### 数据格式

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我设置的数据json存储结构如下(只展示一条信息作为示例)：
```javascript
{
    "data": [
        {
            "分类名称": "0-内科",
            "first_url": "https://tag.120ask.com/jibing/ks/nk.html",
            "疾病类别": [
                {
                    "疾病名称": "高血压",
                    "url": "https://tag.120ask.com/jibing/gxy/",
                    "科室": "内科-心血管内科",
                    "症状": "头晕头痛、恶心呕吐、视物不清、心悸气短",
                    "好发人群": "中老年人尤其是50岁以上人群",
                    "需做检查": "心电图、二维超声心动图、肾脏B超、脑血流图、脑CT、血压检测",
                    "引发疾病": "心梗、肾脏病变、脑水肿、心脏肥大",
                    "治疗方法": "药物治疗、饮食疗法",
                    "常用药物": "降压0号、寿比山、代文、缬沙坦、牛黄降压丸",
                    "是否传染": "否",
                    "患病比例": "12%(50岁以上患病概率30%-50%)",
                    "治愈率": "0.0001%(终身性疾病)",
                    "治疗周期": "1-3个月"
                }
            ]
        }
    ]
}
```

#### 实验结果

爬取了共17个科室的全部疾病信息，每个科室的疾病数量如下所示：
```json
{
    "内科":3595,
    "外科":1860,
    "儿科":969,
    "传染病科":503,
    "妇产科":613,
    "精神心理科":219,
    "皮肤性病科":838,
    "中医科":1224,
    "肿瘤科":779,
    "骨科":627,
    "康复医学科":83,
    "麻醉医学科":119,
    "介入医学科":5,
    "其他科室":2051,
    "营养科":92,
    "五官科":928,
    "医技科":39,
    "医学影像学":10
}
```

#### 后续任务

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;针对收集到的数据我们可以采用统计学习分析方法进行分析，下面列出一些后续完成任务设想：
+ **建立疾病与科室间的知识图谱**：我们仅针对科室进行爬取，但可能存在某种疾病在多个科室之间都存在的情况。我们可以针对疾病和科室这两个实体之间的关系建立知识图谱，方便患者选择针对自己的疾病在哪个科室挂号或查询相关信息。
+ **根据疾病症状判断疾病**：采用文本检索的方法，针对用户输入的自身疾病症状，在保存好的数据库之中进行文本检索，判断与哪一种症状相类似，进行疾病诊断。
+ **爬取更多医生问诊数据，实现医疗问答机器人**：利用深度学习生成式模型，实现医疗问答功能。
+ ……
