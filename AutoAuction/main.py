# This is a sample Python script.
import sys

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QTableWidgetItem, QListWidgetItem
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QTimer, Qt, QDateTime, QObject, QDate

from ui_bot_ch import Ui_Dialog

import json
from datetime import datetime
# import random
# import time
import requests
import threading
import platform
from multiprocessing.pool import ThreadPool

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class BotDlg(QDialog):

    def __init__(self):
        super(BotDlg, self).__init__()
        self.username = 'SMYZMJNY'
        self.token = '353687b4-a896-400b-9232-c9d2637fe649'
        self.target = 'ZYL23030075末煤'
        self.difference = 0
        self.bestPrice = 0
        self.addamount = 0
        self.limitamount = 2222
        self.execution = QDateTime.currentDateTime()
        self.orderoption = 0
        self.orderprice = 1000
        self.orderRun = False
        self.option2timout = 60000

        self.option2first = False
        
        self.timer = QTimer()
        self.timer_list = QTimer()
        self.timer_orderlist = QTimer()
        self.timer_makeorder = QTimer()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.platid = "91"
        self.project_start = ""
        self.project_end = ""
        self.project_status = 1
        self.project_tradeModeId = None
        self.project_tradeTimeId = None
        self.project_companyMargin = 300000
        self.project_maxMatterCount = 30
        self.project_usableMargin = 100000
        self.project_totalstructure = None
        
        # Init Gui
        self.ui.lineEdit_user.setText(self.username)
        self.ui.lineEdit_token.setText(self.token)
        self.ui.lineEdit_target.setText(self.target)
        # self.ui.lineEdit_bestprice.setText(str(self.bestPrice))
        self.ui.lineEdit_addamount.setText(str(self.addamount))
        self.ui.lineEdit_limitedamount.setText(str(self.limitamount))
        self.ui.lineEdit_platid.setText(self.platid)
        self.ui.lineEdit_orderprice.setText(str(self.orderprice))
        self.ui.lineEdit_option2_timeout.setText(str(self.option2timout))
        
        self.ui.pushButton_stop.setEnabled(False)
        # Button Slot Connection
        self.ui.pushButton_test.clicked.connect(self.slot_test)
        self.ui.pushButton_delay.clicked.connect(self.slot_delay)
        self.ui.pushButton_start.clicked.connect(self.slot_start)
        self.ui.pushButton_stop.clicked.connect(self.slot_stop)
        self.ui.pushButton_export.clicked.connect(self.slot_export)
        
        # Radio Button Connection
        self.ui.radioButton_1.clicked.connect(self.slot_radio1)
        self.ui.radioButton_2.clicked.connect(self.slot_radio2)
        
        # Lineedit change text event connection
        self.ui.lineEdit_user.textChanged.connect(self.slot_usertext)
        self.ui.lineEdit_token.textChanged.connect(self.slot_token)
        self.ui.lineEdit_platid.textChanged.connect(self.slot_platid)
        self.ui.lineEdit_addamount.textChanged.connect(self.slot_addamount)
        self.ui.lineEdit_limitedamount.textChanged.connect(self.slot_limitedamount)
        self.ui.lineEdit_orderprice.textChanged.connect(self.slot_orderprice)
        self.ui.lineEdit_option2_timeout.textChanged.connect(self.slot_option2timeout)
        self.ui.timeEdit.timeChanged.connect (self.slot_time)
        
        
        # Timeout connection
        self.timer.timeout.connect(self.timeout)
        self.timer_list.timeout.connect(self.timeout_list)
        self.timer_orderlist.timeout.connect(self.timeout_orderlist)
        self.timer_makeorder.timeout.connect(self.timeout_makeorder)
        
        
    def writeLog(self, _str):
        with open("log.txt", "a") as f:
            now = datetime.now().timestamp()*1000
            f.writelines(str(now) + ' : ' + _str + '\n')
    # Main timer event handler    
    
    def timeout(self):
        _now = datetime.now().timestamp()
        _exec = self.execution.toMSecsSinceEpoch()
        # if(_now > _exec):
        #     print("start scan")
        #     self.scan()
        # else:
        #     print("end scan")
        self.scan()
    
    
    def timeout_list(self):
        _now = datetime.now().timestamp()
        _exec = self.execution.toMSecsSinceEpoch()
        # if(_now > _exec):
        #     print("start scan_list")
        #     self.scan_list()
        # else:
        #     print("end scan_list")
        self.scan_list()
    

    def timeout_orderlist(self):
        _now = datetime.now().timestamp()
        _exec = self.execution.toMSecsSinceEpoch()
        # if(_now > _exec):
        #     print("start scan_orderlist")
        #     self.scan_orderlist()
        # else:
        #     print("end scan_orderlist")
        self.scan_orderlist()
    
    def timeout_makeorder(self):
        if self.project_totalstructure != None and self.project_totalstructure != "":
            if self.project_tradeTimeId != None and self.project_tradeTimeId != "":
                _now = datetime.now().timestamp()
                _exec = self.execution.toMSecsSinceEpoch()
                if self.orderoption == 0:
                    if(_now*1000 < _exec):
                        print("Not Yet timeout_makeorder1")
                    else:
                        self.post_makeorder()
                        print('end timeout_makeorder')
                else:
                    if self.project_start != None and self.project_start != "":
                        _start = datetime.strptime(self.project_start, '%Y-%m-%d %H:%M:%S')
                        _startepoch = _start.timestamp()
                        print('order option 2 ', _startepoch, _now)
                        if(_now*1000 < (_startepoch + int(self.option2timout))):
                            print("Not Yet timeout_makeorder2")
                        else:
                            self.post_makeorder()
                            print('end timeout_makeorder2')

                    else:
                        print('cant get start time, cant make order, sorry')


    # Signal Slot
        
    def slot_usertext(self, text):
        print('username change:', self.username, text)
        outputStr = 'username change: ' + self.username + ' : ' + text
        self.username = text
        self.writeLog(outputStr)
        
        
    def slot_token(self, text):
        print('token change:', self.token, text)
        outputStr = 'token change: ' + self.token + ' : ' + text
        self.token = text
        self.writeLog(outputStr)
        
        
    def slot_platid(self, id):
        print('platid change:', self.platid, id)
        outputStr = 'platid change: ' + self.platid + ' : ' + id
        self.option2first = False
        self.platid = id
        self.writeLog(outputStr)
        
        
    def slot_addamount(self, amount):
        print('change add price', amount)
        outputStr = 'change add price: ' + str(self.addamount) + ' : ' + amount
        self.addamount = int(amount)
        self.writeLog(outputStr)
        
        
    def slot_limitedamount(self, limitamount):
        print('change limit price')
        outputStr = 'change limit price: ' + str(self.limitamount) + ' : ' + limitamount
        self.limitamount = int(limitamount)
        self.writeLog(outputStr)
        
        
    def slot_orderprice(self, orderprice):
        print('change order price')
        outputStr = 'change order price: ' + str(self.orderprice) + ' : ' + orderprice
        self.orderprice = int(orderprice)
        self.writeLog(outputStr)
        
    
    def slot_option2timeout(self, timeout):
        print('change option2 timeout')
        outputStr = 'change option2 timeout: ' + str(self.option2timout) + ' : ' + timeout
        self.option2timout = int(timeout)
        self.writeLog(outputStr)
        
        
    def slot_time(self, settime):
        _tmp = QDateTime()
        _tmp.setDate(QDate.currentDate())
        _tmp.setTime(settime)
        self.execution = _tmp
        print("change execution time", self.execution.toMSecsSinceEpoch())
        outputStr = 'change execution time: ' + str(self.execution.toMSecsSinceEpoch())
        self.writeLog(outputStr)
        # print("now time", datetime.now().timestamp())
        # print("execution time", self.execution.msecsTo(datetime.now()))
        
                
    def scan(self):
        print('getPlatInfor')
        res = self.getPlatInfor()
        if "plateVo" in res:
            # print("getPlatInfor", res)
            if res["plateVo"] != None:
                # self.project_start = res["plateVo"]["startTimeProcess"]
                # self.project_end = res["plateVo"]["endTime"]
                # self.project_status = res["plateVo"]["status"]
                print("platVo")
                outputStr = 'platVo: ' + json.dumps(res["plateVo"])
                self.writeLog(outputStr)
                # print("platVo", res['plateVo'])
                

        if "matterList" in res:
            if res["matterList"] != None:
                if len(res["matterList"]) > 0:
                    # main current plat information get
                    self.project_totalstructure = res["matterList"][0]
                    self.ui.lineEdit_target.setText(self.project_totalstructure['matterCode'])
                    self.bestPrice = str(self.project_totalstructure['bestPrice'])

                    if(self.project_totalstructure['bestPrice'] == None or self.project_totalstructure['bestPrice'] == 0):
                        self.bestPrice = str(self.project_totalstructure['beginPrice'])
                    # self.ui.lineEdit_bestprice.setText(self.bestPrice)
                    if(self.option2first == False):
                        self.ui.lineEdit_orderprice(str(self.bestPrice))
                        self.option2first = True
                        
                    print('main pro auction', self.project_totalstructure)
                    outputStr = 'main pro auction: ' + json.dumps(self.project_totalstructure)
                    self.writeLog(outputStr)


        
    def scan_list(self):
        res = self.get_list()
        if(len(res) > 0):
            # self.platid = str(res[0]['plateId'])
            if(res[0]['tradeTimeId'] != None):
                self.project_tradeTimeId = str(res[0]['tradeTimeId'])
            self.project_start = res[0]['startTimeProcess']
            self.project_end = res[0]['endTime']
            self.project_status = res[0]['status']
            outputStr = 'scan_list: ' + json.dumps(res[0])
            self.writeLog(outputStr)
            # print("scan_list", res[0])


    def scan_orderlist(self):
        res = self.getOrderInfor()
        if(len(res) > 0):
            print("scan_orderlist", res)
            outputStr = 'scan_orderlist' + json.dumps(res)
            self.writeLog(outputStr)
    

    def slot_test(self):
        res = self.get_list()
        if res == None:
            print('test failed')
            return
        
        if "msg" in res:
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(False)
            print("test error", res)
            outputStr = 'test error: ' + json.dumps(res)
            self.writeLog(outputStr)
        else:
            self.ui.pushButton_start.setEnabled(True)
            # self.ui.pushButton_stop.setEnabled(True)
            

    def slot_delay(self):
        dbTime = float(self.get_dbTime())
        now = datetime.now().timestamp()*1000
        # print("difference", now - dbTime)
        self.difference = (now-dbTime)
        # self.ui.lineEdit_delay.setText(str(self.difference) + " ms")
        outputStr = 'delay time: ' + str(self.difference)
        self.writeLog(outputStr)
        

    def slot_start(self):
        self.orderRun = False
        self.timer.start(2000)
        self.timer_list.start(3000)
        self.timer_orderlist.start(5000)
        self.timer_makeorder.start(1000)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)
        
        self.ui.timeEdit.setEnabled(False)
        self.option2first = False
        print('start')
        self.writeLog('start')
        
        
    def slot_stop(self):
        self.orderRun = False
        self.timer.stop()
        self.timer_list.stop()
        self.timer_orderlist.stop()
        self.timer_makeorder.stop()
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)
        
        self.ui.timeEdit.setEnabled(True)
        self.option2first = False
        print('stop')
        self.writeLog('stop')
        
        
    def slot_export(self):
        print('export')
        self.writeLog('export')
        
        
    def slot_radio1(self):
        self.orderoption = 0
        self.ui.timeEdit.setEnabled(True)
        self.ui.lineEdit_option2_timeout.setEnabled(False)
        
        self.ui.lineEdit_addamount.setEnabled(True)
        self.ui.lineEdit_limitedamount.setEnabled(True)
        self.ui.lineEdit_orderprice.setEnabled(False)
        print('order option 0')
        self.writeLog('order option 0')
        
        
    def slot_radio2(self):
        self.orderoption = 1
        self.ui.timeEdit.setEnabled(False)
        self.ui.lineEdit_option2_timeout.setEnabled(True)
        
        self.ui.lineEdit_addamount.setEnabled(False)
        self.ui.lineEdit_limitedamount.setEnabled(False)
        self.ui.lineEdit_orderprice.setEnabled(True)
        self.ui.lineEdit_orderprice.setText(str(self.bestPrice))
        self.option2first = False
        
        print('order option 1, set order price as begin price', self.bestPrice)
        self.writeLog('order option 1')
        self.writeLog('set order price as begin price: ' + str(self.bestPrice))
        
        
    # Request Part
        
    def get_list_offset(self):
        url = "https://jy.yectc.com:16952/frontService/base/message/message/list?offset=1&typeId=10002&standard=151973"
        response = self.getRequest(url)
        _res = json.loads(response.text)
        outputStr = 'get_list_offset : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        return _res
        

    def get_dbTime(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/dbTime"
        response = self.getRequest(url)
        outputStr = 'get_dbTime : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        return response.text
    

    # big trading plate information get
    # third endpoint
    # https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/home/tradingPlate/list
    # Refresh time - 3s
    def get_list(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/home/tradingPlate/list"

        response = self.getRequest(url)
        if response == None:
            print('cant get_list')
            return None
        _res = json.loads(response.text)
        outputStr = 'get_list : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        return _res
    

    # sixth endpoint
    # refresh time - 500ms
    # https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/plate/matter/list?maxCount=30&plateId=75&status=2
    def get_mainList(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/plate/matter/list?maxCount=31&plateId=" + self.platid + "&status=2"
        
        response = self.getRequest(url)
        _res = json.loads(response.text)
        
        outputStr = 'get_mainList : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        
        if "matterGroupList" in _res:
            matterGroupList = _res["matterGroupList"]
            if matterGroupList != None | matterGroupList != 'null':
                if "matterList" in matterGroupList:                     
                    self.tradeInformation = matterGroupList
                            
        return _res
    
    
    def getPlatInfor(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/plate/matter/list?&plateId=" + self.platid +"&status=2"
        response = self.getRequest(url)
        _res = json.loads(response.text)
        
        outputStr = 'getPlatInfor : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        
        return _res
        
    
    def getOrderInfor(self):
        if self.project_tradeTimeId != None:
            url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/match/order?tradeModeId=1&tradeTimeId=" + str(self.project_tradeTimeId)
            response = self.getRequest(url)
            _res = json.loads(response.text)
            outputStr = 'getOrderInfor : ' + url + ' : ' + response.text
            self.writeLog(outputStr)
            return _res
        else:
            return []
    
    
    # Get full list of orders - first endpoint
    # https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/stationRoad/list
    # Desired Response - 15s
    # Many array list - 239
    # [{stationRoadId: 1, stationRoadName: "神树畔矿业", status: 0, createTime: "2021-08-31 10:21:42"}, ......]
    def getList1(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/stationRoad/list"
        response = self.getRequest(url)
        _res = json.loads(response.text)
        outputStr = 'getList1 : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        return _res
    

    # Get active information - second endpoint
    # Desired Response - 1m
    # https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/plate/matter/list?plateId=
    def getList2(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/common/plate/matter/list?plateId=" + self.platid
        response = self.getRequest(url)
        _res = json.loads(response.text)
        outputStr = 'getList2 : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        return _res



    # Not Important - fourth endpoint
    # Desired Response - 3s
    # { companyMargin : 0, maxMatterCount : 30, usableMargin : 0 }
    def getTradeInfor(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/plate/myMatter/trade?plateId=" + self.platid
        response = self.getRequest(url)
        _res = json.loads(response.text)
        outputStr = 'getTradeInfor : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        if "maxMatterCount" in _res:
            self.project_companyMargin = _res["companyMargin"]
            self.project_maxMatterCount = _res["maxMatterCount"]
            self.project_usableMargin = _res["usableMargin"]
            return _res
        else:
            return None


    # get order list - fifth endpoint
    # Desired Response - 3s
    # https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/match/order?tradeModeId=1&tradeTimeId=4666
    def getfullorderlist(self):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/special/match/order?tradeModeId=1&tradeTimeId=4666"
        response = self.getRequest(url)
        _res = json.loads(response.text)
        outputStr = 'getfullorderlist : ' + url + ' : ' + response.text
        self.writeLog(outputStr)
        return _res


    def getdetailofmatter(self):
        if self.project_totalstructure != None:
            if self.project_totalstructure['matterId'] != None:
                url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/open/detail?matterId=" + str(self.project_totalstructure['matterId']) + "&tradeModeId=1"
                response = self.getRequest(url)
                _res = json.loads(response.text)
                outputStr = 'getdetailofmatter : ' + url + ' : ' + response.text
                self.writeLog(outputStr)
                return _res
            else: 
                return None
        else:
            return None
        
        
    def gettradeguantity(self):
        if self.project_totalstructure != None:
            if self.project_totalstructure['matterId'] != None:
                url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/open/tradeQuantity?matterId=" + str(self.project_totalstructure['matterId'])
                response = self.getRequest(url)
                _res = json.loads(response.text)
                outputStr = 'gettradeguantity : ' + url + ' : ' + response.text
                self.writeLog(outputStr)
                return _res
            else:
                return None
        else:
            return None


    def post_makeorder(self):
        if self.orderRun == True:
            print('order is already posted')
            self.writeLog('order is already posted')
            return
        print('order time condition passed')
        self.writeLog('order time condition passed')
        if self.project_totalstructure != None:
            if self.project_totalstructure['matterId'] != None and self.project_totalstructure['bestPrice'] != None and self.project_totalstructure['quantity'] != None:
                my_quantity = self.project_totalstructure['quantity'] - self.project_totalstructure['orderQuantity']
                my_price = self.project_totalstructure['bestPrice'] + self.addamount
                if int(self.project_totalstructure['bestPrice']) == 0:
                    my_price = self.project_totalstructure['beginPrice'] + self.addamount
                if self.orderoption == 1:
                    my_price = self.orderprice
                if(my_price > self.limitamount):
                    print('Current Price is too high')
                    self.writeLog('Current Price is too high')
                    self.slot_stop()
                    return None
                url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/open/order/single"
                payload = {
                    'matterId': str(self.project_totalstructure['matterId']),
                    'tradeModeId': '1',
                    'price': str(my_price),
                    'quantity': str(my_quantity)
                }
                print('order make endpoint', url, payload)
                outputStr = 'order make endpoint : ' + url + ' : ' + json.dumps(payload)
                self.writeLog(outputStr)
                response = self.postRequest(url, payload)
                _res = json.loads(response.text)
                if "msg" in _res:
                    print('order place failed', _res)
                    outputStr = 'order place failed : ' + url + ' : ' + response.text
                    self.writeLog(outputStr)
                elif "responseValue" in _res:
                    print('order place successfully', _res)
                    outputStr = 'order place successfully : ' + url + ' : ' + response.text
                    self.writeLog(outputStr)
                    self.orderRun = True
                    
                else:
                    print('make new order posted', _res)
                    outputStr = 'make new order posted : ' + url + ' : ' + response.text
                    self.writeLog(outputStr)
                    
                return _res
            else:
                return None
        else:
            return None


    def getRequest(self, url):
        # print('get:', url, self.username, self.token)
        payload={}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'jy.yectc.com:16952',
            'Referer': 'https://jy.yectc.com:16952/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Token': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'UserID': self.username
        }
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            return response
        except:
            print('getRequest error: ', url)
            return None
    
    def postRequest(self, url, payload):
        # print('post:', url, self.username, self.token)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'jy.yectc.com:16952',
            'Referer': 'https://jy.yectc.com:16952/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Token': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'UserID': self.username
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            return response
        except:
            print('postRequest error', url)
            return None
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = BotDlg()
    w.exec_()