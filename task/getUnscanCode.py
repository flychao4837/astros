#!/usr/bin/python
# coding=UTF-8
import datetime as datetime
import os as os
import time as time
import tushare as ts
import config as config
from readJsonFile import readFile
from getDailyInfo import getDailyData
from writeJsonFile import writeFile
##获取basicjson中未扫描的股票代码

endDate = datetime.datetime.now().strftime("%Y-%m-%d") #以当天为截止日期
basicFile = config.listsRootPath + '\\stockBasic.json'
basicDate = readFile(basicFile)  # timeToMarket 上市日期
scanFile = config.configRootPath+'\\scanData.json'
scanConfigDate = readFile(scanFile)

def getSingleStockDate(stock=""):
    if bool(stock):
        ##获取基本数据
        if basicDate['errcode']==0:
            lists = basicDate['data']
            if  bool(lists) :
                for k in lists:
                    if k ==stock:
                        startBasicDate = str(lists[k]['timeToMarket'])
                        return startBasicDate
                        break
                        #找到code就退出循环
            else:
                return {'errcode': -10000, 'errmsg': "没找到对应code代码", 'data': ''}
        else:
            print basicDate['errcode']
    else:
        return {'errcode': -10000, 'errmsg': "需要code参数", 'data': ''}



def getSingleStockDailyList(stock=""):
    dateStr = getSingleStockDate(stock)
    if bool(dateStr) and len(dateStr) == 8:
        startDate = dateStr[:4] + "-" + dateStr[4:6] + "-" + dateStr[6:]
        # str格式的时间转成datetime，便于时间操作、比较
        startTime = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
        endTime = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
        if scanConfigDate['errcode'] == 0:
            scanData = scanConfigDate['data']

        if(startTime < endTime):

            addDate = startTime + datetime.timedelta(days=0)  # 逐天扫描
            scanDate = addDate.strftime("%Y-%m-%d")

            if stock[0] == "2" or stock[0] == "9":
                pass
            else:
                #打印basic中未扫描的
                compareFile = config.dataRootDailyTrade + "\\" + stock + "\\" + startDate + ".json"
                if os.path.isfile(compareFile):
                    pass
                else:
                    print stock+","


            ##获取间隔天数，遍历这些日期
            totalDays = (endTime - startTime).days
            for num in range(0, totalDays+1):
                addDate = startTime + datetime.timedelta(days=num)
                scanDate = addDate.strftime("%Y-%m-%d")
                getDailyData(stock=stock, date=scanDate)
        else:
            pass

    else:
        pass
        # print "获取的时间不对"
        # print stock
        # print "------------------"


###循环code
def getCodeCircle():
    ##记录已扫描的股票，下次跳过这些
    if scanConfigDate['errcode'] == 0:
        scanData = scanConfigDate['data']
        scanData['date'] = endDate

    if basicDate['errcode'] == 0:
        lists = basicDate['data']
        for k in lists:
            #getSingleStockDailyList(k)
            try:
                isStockScan = scanData['lastScanStock'].index(k)
            except Exception, e:
                isStockScan = False

            if bool(isStockScan):
                # print k+"已经扫描"
                # continue
                getSingleStockDailyList(k)
            else:
                pass
                # lastScanStock = scanData['curScanStock']
                # scanData['curScanStock'] = k
                # scanData['lastScanStock'] = scanData['lastScanStock']+","+lastScanStock
                # writeFile(scanFile, scanData)
                #
                # getSingleStockDailyList(k)


#getSingleStockDailyList("000004") ##执行到那里

def asynDetect():
    counter = 1
    try:
        getCodeCircle()

    except Exception, ex:
        ###这里应该捕获 URIError，IOError
        counter +=1
        print counter
        if counter <5:
            time.sleep(180)
            asynDetect()
        else:
            print "exit"
            exit(1)

#getSingleStockDailyList("000004") ##执行到那里
getCodeCircle()

###捕捉错误，多由网络中断引起，延时后重复多次
#asynDetect()

