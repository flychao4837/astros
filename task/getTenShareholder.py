#!/usr/bin/python
# coding=UTF-8

#获取前十大股东、十大流通股东、十大机构持股名单
import sys
import os
import time
import tushare as ts
import datetime as datetime
import config as config
from readJsonFile import readFile
from writeJsonFile import writeFile

import urllib
import urllib2
import re
from bs4 import BeautifulSoup

basicFile = os.path.join(config.listsRootPath, 'stockBasic.json')
basicDate = readFile(basicFile)
scanFile = os.path.join(config.configRootPath, 'scanData.json')
scanConfigDate = readFile(scanFile)


# 页面爬虫类
# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

class SPIDER:
    # 初始化，传入基地址
    def __init__(self):
        # HTML标签剔除工具类对象
        self.tool = Tool()
        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.file = None

        self.defaultTitle = u"page"
        # 文件起始目录
        self.pageroot = config.dataRoottenShareholder


    # 传入页码，获取该页的代码
    def getPage(self,baseUrl=None):
        try:
            # 构建URL
            if baseUrl is not None:
                url = baseUrl
                request = urllib2.Request(url)
                response = urllib2.urlopen(request)
                # 返回UTF-8格式编码内容
                return response.read().decode('utf-8')
            else:
                pass
        # 无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败,错误原因", e.reason
                return None


    # 获取页面内容
    def getContent(self, file):
        if os.path.isfile(file):
            reload(sys)
            sys.setdefaultencoding('utf-8')

            soup = BeautifulSoup(open(file), 'lxml')
            section = soup.select(".section")

            if section[0]:
                gdrs = section[0]
                table = gdrs.select("table")
                if table[0]:
                    rows = table[0].select("tr")
                    times = rows[0].select(".tips-dataL")
                    numbers = rows[1].select(".tips-dataL") #股东人数
                    pernumberchanges = rows[2].select(".tips-dataL") #股东人数变化
                    pershares = rows[3].select(".tips-dataL") #人均流通持股
                    persharechanges = rows[4].select(".tips-dataL") #人均流通股变化
                    scr = rows[5].select(".tips-dataL") #筹码集中度 Stock Convergence Rate
                    prices = rows[6].select(".tips-dataL") #股价
                    perprice = rows[7].select(".tips-dataL") #人均持股金额
                    tenshare = rows[8].select(".tips-dataL") #十大股东
                    tencirshare = rows[9].select(".tips-dataL") #十大流通股东

                    data = dict()
                    data['gdrs'] = dict()

                    for i in range(1, len(times)):
                        idx = times[i].get_text().decode()
                        data['gdrs'][idx] = dict()
                        data['gdrs'][idx]['number'] = numbers[i].get_text().decode()
                        data['gdrs'][idx]['numcg'] = pernumberchanges[i].get_text().decode()
                        data['gdrs'][idx]['pershare'] = pershares[i].get_text().decode()
                        data['gdrs'][idx]['sharecg'] = persharechanges[i].get_text().decode()
                        data['gdrs'][idx]['scr'] = scr[i].get_text().decode()
                        data['gdrs'][idx]['price'] = prices[i].get_text().decode()
                        data['gdrs'][idx]['perprice'] = perprice[i].get_text().decode()

                    for i in tenshare:
                        t = i.get_text().decode()
                        if t is not None and t !="--":
                            data['tenshare'] = t
                            break

                    for i in tencirshare:
                        t = i.get_text().decode()
                        if t is not None and t !="--":
                            data['tencirshare'] = t
                            break

                    jsonFile = os.path.join(self.pageroot, '002334')
                    jsonFile = os.path.join(jsonFile, "gdrs.json")
                    writeFile(jsonFile, data, 'records', False)

            if section[1]:
                sdltgd = section[1]

            if section[2]:
                sdgd = section[2]

            if section[3]:
                sdgdcgbd = section[3]

            if section[4]:
                jjcc = section[4]

            if section[5]:
                xsjj = section[5]

        else:
            print "error"
            pass

    ###抓取的页面先暂存，便于后期处理、查阅
    def writeData(self, name=None, content=None):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if content is not None and name is not None:
            self.file = open(name, "w+")
            self.file.write(content)
            self.file.close()
        else:
            print "文件名或内容为空"
            pass

    def start(self):
        contdir = os.path.join(self.pageroot, '002334')
        filename = os.path.join(contdir, "002334htmlContent.txt")
        self.getContent(filename)
        #遍历目录
        # if basicDate['errcode'] == 0:
        #     lists = basicDate['data']
        #     for k in lists:
        #         contdir = os.path.join(self.pageroot, k)
        #         print contdir
        #         if os.path.isdir(contdir):
        #             pass
        #         else:
        #             os.mkdir(contdir)
        #
        #         filename = os.path.join(contdir, k+"htmlContent.txt");
        #         url ="http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=sz"+k
        #         try:
        #             indexPage = self.getPage(url)
        #             self.writeData(filename, indexPage)
        #         # 出现写入异常
        #         except IOError, e:
        #             print "写入异常，原因" + e.message
        #         finally:
        #             print "写入任务完成"
        #             self.getContent(filename)

bdtb = SPIDER()
bdtb.start()