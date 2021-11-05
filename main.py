import requests
import os, time
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
headers={
  'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:70.0) Gecko/20100101 Firefox/70.0'
}
'''
DataList
数据格式:   dict
DataList = {
    "data":[
        {
            "分类名称":"0-内科",
            "first_url": "https://tag.120ask.com/jibing/ks/nk.html",
            "疾病类别":[
                {
                    "疾病名称":"",
                    "url":"",
                    "科室":"",
                    "症状":"",
                    "好发人群":"",
                    "引发疾病":"",
                    "是否传染":"",
                    "治疗方法":"",
                    ……
                }
            ]
        }
    ]
}
'''
DataList = {}

def getFirstList(main_url):
    global DataList
    main_html = requests.get(main_url,headers=headers)        #Get方式获取网页数据
    soup = BeautifulSoup(main_html.text, 'lxml')
    data = soup.select('html>body>div.m1200>div.sick_tag>div.sick_box>div.dl.sort.clears>p.tab>a')
    for index,info in enumerate(data):
        if index > 17:
            # 超出设定范围
            break
        local_path = os.path.join("./data/",str(index)+'-'+info.string)
        if os.path.exists(local_path) == 0:
            os.makedirs(local_path)
        DataList["data"].append({
            "分类名称":str(index)+'-'+info.string,
            "first_url":"https:"+info["href"]
        })

def getInfo(url, cls, num, name):
    if os.path.exists(os.path.join("./data/",cls,str(str(num)+'-'+name+".json").replace('/', ' '))):
        disease_info = json.load(open(os.path.join("./data/",cls,str(str(num)+'-'+name+".json").replace('/', ' ')),encoding='utf-8'))
        return disease_info
    disease_info = {}
    url = "https:"+url
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.select('html>body>div.disease-page>div.disease-cont>dl.clears>dd>b>strong')[0].string
    value_list = soup.select('html>body>div.disease-page>div.disease-list-title>div.disease-list-left>ul>li>var')
    disease_info["疾病名称"] = name
    disease_info["url"] = url
    try:
        disease_info["科室"] = value_list[0].string
        disease_info["症状"] = value_list[1].string
        disease_info["好发人群"] = value_list[2].string
        disease_info["需做检查"] = value_list[3].string
        disease_info["引发疾病"] = value_list[4].string
        disease_info["治疗方法"] = value_list[5].string
        value_list2 = soup.select('html>body>div.disease-page>div.disease-list-title>div.disease-list-center>ul>li>var')
        disease_info["常用药物"] = value_list2[0].string
        disease_info["是否传染"] = value_list2[2].string
        disease_info["患病比例"] = value_list2[3].string
        disease_info["治愈率"] = value_list2[4].string
        disease_info["治疗周期"] = value_list2[5].string
    except:
        disease_info["科室"] = "暂无信息"
        disease_info["症状"] = "暂无信息"
        disease_info["好发人群"] = "暂无信息"
        disease_info["需做检查"] = "暂无信息"
        disease_info["引发疾病"] = "暂无信息"
        disease_info["治疗方法"] = "暂无信息"
        value_list2 = soup.select('html>body>div.disease-page>div.disease-list-title>div.disease-list-center>ul>li>var')
        disease_info["常用药物"] = "暂无信息"
        disease_info["是否传染"] = "暂无信息"
        disease_info["患病比例"] = "暂无信息"
        disease_info["治愈率"] = "暂无信息"
        disease_info["治疗周期"] = "暂无信息"
    json_str = json.dumps(disease_info,ensure_ascii=False)
    if name == None:
        name = "暂未识别"
    with open(os.path.join('./data/',cls,str(str(num)+'-'+name+".json").replace('/', ' ')), 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)
    return disease_info

def getInfoList():
    global DataList
    for index,dict_info in tqdm(enumerate(DataList["data"])):
        html = requests.get(dict_info["first_url"],headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        data = soup.select('html>body>div.m1200>div.sick_tag>div.tag_li>p>a')
        DataList["data"][index]["疾病类别"] = []
        print("=====正在进行【{}】类别疾病信息爬取，预计共{}条信息=====".format(dict_info["分类名称"], len(data)))
        start = time.time()
        for ii, info in enumerate(data):
            url = info["href"]
            name = info.string
            if name == None:
                name = "暂未识别"
            DataList["data"][index]["疾病类别"].append(getInfo(url, dict_info["分类名称"], ii,name))
        print("=====【{}】类别疾病信息爬取完毕，花费时间{}s=====".format(dict_info["分类名称"],time.time()-start))

    json_str = json.dumps(DataList, ensure_ascii=False)
    with open(os.path.join('./data/',"allData.json"), 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    DataList['data'] = []
    url = 'https://tag.120ask.com/jibing/ks/nk.html'
    getFirstList(main_url=url)
    # print(DataList)
    getInfoList()