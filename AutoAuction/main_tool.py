# This is a sample Python script.
import sys

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QTableWidgetItem, QListWidgetItem
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QTimer, Qt, QDateTime, QObject, QDate, QTime

from ui_tool import Ui_Dialog

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
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.autoorder = False
        
        self.username = 'SMYZMJNY'
        self.token = '10c35168-4b2f-47f9-8614-a74bb8ce1d8a'
        self.platid = "131"
        
        self.difference = 0
        self.responseTime = 0

        self.curLabel = None
        self.curFirstOrder = None
        self.curLastOrder = None
        self.actualEnd = None
        self.actualStart = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

        # Init Gui
        self.ui.lineEdit_user.setText(self.username)
        self.ui.lineEdit_token.setText(self.token)
        self.ui.lineEdit_platid.setText(self.platid)
        
        # Button Slot Connection
        self.ui.pushButton_test.clicked.connect(self.slot_test)
        self.ui.pushButton_start.clicked.connect(self.slot_start)
        self.ui.pushButton_stop.clicked.connect(self.slot_stop)
        self.ui.pushButton.clicked.connect(self.slot_makeOrder)
        
        # Lineedit change text event connection
        self.ui.lineEdit_user.textChanged.connect(self.slot_usertext)
        self.ui.lineEdit_token.textChanged.connect(self.slot_token)
        self.ui.lineEdit_platid.textChanged.connect(self.slot_platid)
        
        self.ui.radioButton.clicked.connect(self.slot_manual)
        self.ui.radioButton_2.clicked.connect(self.slot_auto)
    
    def slot_manual(self):
        self.autoorder = False
        print('manual')
        
    def slot_auto(self):
        self.autoorder = True
        print('auto')
        
    def writeLog(self, _str):
        with open("log-tool.txt", "a") as f:
            now = datetime.now().timestamp()*1000
            f.writelines(str(now) + ' : ' + _str + '\n')
    # Main timer event handler   
    #  
    
    def timeout(self):
        self.scan()


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
        self.platid = id
        self.writeLog(outputStr)
        
    def slot_makeOrder(self):
        if(self.curLabel != None):
            res = self.getPlatInfor()
            if "matterList" in res:
                if res["matterList"] != None:
                    if len(res["matterList"]) > 0:
                        # main current plat information get
                        self.project_totalstructure = res["matterList"][0]
                        self.bestPrice = str(self.project_totalstructure['bestPrice'])

                        if(self.project_totalstructure['bestPrice'] == None or self.project_totalstructure['bestPrice'] == 0):
                            self.bestPrice = str(self.project_totalstructure['beginPrice'])
                        self.ui.lineEdit_bestPrice.setText(self.bestPrice)
                        # self.ui.lineEdit_bestprice.setText(self.bestPrice)
                        # print('main pro auction', self.project_totalstructure)
                        outputStr = 'manual make order: ' + json.dumps(self.project_totalstructure)
                        self.writeLog(outputStr)

                        _status = self.project_totalstructure['status']
                        _label = self.project_totalstructure['matterCode']

                        if(_status == 2):
                            _documentary_time = QTime.currentTime()
                            bestPrice = self.project_totalstructure['bestPrice']
                            bestQuantity = self.project_totalstructure['bestQuantity']
                            matterId = self.project_totalstructure['matterId']
                            if(bestPrice == 0):
                                bestPrice = self.project_totalstructure['beginPrice']
                            self.writeLog('make new order by manual: ' + _documentary_time.toString('hh:mm:ss:zzz') + ', matterId: ' + str(matterId) + ', bestPrice: ' + str(bestPrice) + ', bestQuantity: '+ str(bestQuantity))
                            _res = self.post_makeorder(matterId, bestPrice, bestQuantity)

                            if(_res != None):
                                _spentTime = _res.elapsed.total_seconds()
                                _first_order_time = QTime.currentTime()
                                _local_echo_time = QTime.currentTime()
                                _server_echo_time = _local_echo_time.addMSecs(-_spentTime/2-self.difference)
                                if(self.curFirstOrder == None):
                                    self.updateItem(_label, 2, _first_order_time.toString('hh:mm:ss:zzz'))
                                self.updateItem(_label, 6, _documentary_time.toString('hh:mm:ss:zzz'))
                                self.updateItem(_label, 7, _local_echo_time.toString('hh:mm:ss:zzz'))
                                self.updateItem(_label, 8, _server_echo_time.toString('hh:mm:ss:zzz'))
                                self.curFirstOrder = True
                
    def scan(self):
        print('getPlatInfor')
        res = self.getPlatInfor()

        project_start = None
        project_end = None

        _start_time = None
        _end_time = None
        _spent_time = None

        _first_order_time = None
        _last_order_time = None
        _estimate_end_time = None
        _documentary_time = None
        _local_echo_time = None
        _server_echo_time = None
        _recommended_time = None

        if "plateVo" in res:
            if res["plateVo"] != None:
                
                project_start = res["plateVo"]["startTimeProcess"]
                if project_start != None:
                    project_start = project_start.split(' ')[1]
                    _start_time = QTime.fromString(project_start)
                    _start_time = _start_time.addMSecs(int(self.difference))
                    project_start = _start_time.toString('hh:mm:ss:zzz')
                    
                project_end = res["plateVo"]["endTime"]
                if project_end != None:
                    project_end = project_end.split(' ')[1]
                    _end_time = QTime.fromString(project_end)
                    _end_time = _end_time.addMSecs(int(self.difference))
                    
                    _recommended_time = _end_time.addMSecs(-int(self.responseTime))
                    # _documentary_time = _recommended_time.addMSecs(-240)
                    # _local_echo_time = _documentary_time

                    project_end = _end_time.toString('hh:mm:ss:zzz')

                    _spent_time = _start_time.msecsTo(_end_time)

                print("platVo")
                outputStr = 'platVo: ' + json.dumps(res["plateVo"])
                self.writeLog(outputStr)

                _status = res["plateVo"]["status"]
                if(_status == 3):
                    if(self.curLabel != None):
                        if(self.actualEnd == None):
                            _curTime = QTime.currentTime()
                            self.updateItem(self.curLabel, 5, _curTime.toString('hh:mm:ss:zzz'))
                            self.actualEnd = True
                else:
                    self.actualEnd = None

                if(_status != 2):
                    self.actualStart = None

        if "matterList" in res:
            if res["matterList"] != None:
                if len(res["matterList"]) > 0:
                    # main current plat information get
                    self.project_totalstructure = res["matterList"][0]
                    self.bestPrice = str(self.project_totalstructure['bestPrice'])

                    if(self.project_totalstructure['bestPrice'] == None or self.project_totalstructure['bestPrice'] == 0):
                        self.bestPrice = str(self.project_totalstructure['beginPrice'])
                    self.ui.lineEdit_bestPrice.setText(self.bestPrice)
                    outputStr = 'main pro auction: ' + json.dumps(self.project_totalstructure)
                    self.writeLog(outputStr)

                    _status = self.project_totalstructure['status']
                    _label = self.project_totalstructure['matterCode']
                    
                    if(self.actualStart == None):
                        if(_status == 2):
                            _cur_time = QTime.currentTime()
                            _cur_end_time = _cur_time.addMSecs(_spent_time)
                            self.updateItem(_label, 1, _cur_time.toString('hh:mm:ss:zzz'))
                            self.updateItem(_label, 4, _cur_end_time.toString('hh:mm:ss:zzz'))
                            # self.updateItem(_label, 5, project_end)
                            _a = QTime(0,0,0,0)
                            _a = _a.addMSecs(abs(int(self.difference)))
                            self.updateItem(_label, 10, _a.toString('hh:mm:ss:zzz'))
                            self.actualStart = True

                    if(_start_time != None):
                        self.updateItem(_label, 9, _recommended_time.toString('hh:mm:ss:zzz'))
                        # self.updateItem(_label, 3, _recommended_time.toString('hh:mm:ss:zzz'))
                        # self.updateItem(_label, 6, _documentary_time.toString('hh:mm:ss:zzz'))
                        # self.updateItem(_label, 7, _local_echo_time.toString('hh:mm:ss:zzz'))

                    if(_label != self.curLabel):
                        self.curLabel = _label
                        self.curFirstOrder = None
                        self.curLastOrder = None

                    if(_status == 2 and self.autoorder == True):
                        if(self.curFirstOrder != None):
                            _documentary_time = QTime.currentTime()
                            bestPrice = self.project_totalstructure['bestPrice']
                            bestQuantity = self.project_totalstructure['bestQuantity']
                            matterId = self.project_totalstructure['matterId']
                            if(bestPrice == 0):
                                bestPrice = self.project_totalstructure['beginPrice']
                            self.writeLog('make new order: ' + _documentary_time.toString('hh:mm:ss:zzz') + ', matterId: ' + str(matterId) + ', bestPrice: ' + str(bestPrice) + ', bestQuantity: '+ str(bestQuantity))
                            _res = self.post_makeorder(matterId, bestPrice, bestQuantity)

                            if(_res != None):
                                _spentTime = _res.elapsed.total_seconds()
                                _first_order_time = QTime.currentTime()
                                _local_echo_time = QTime.currentTime()
                                _server_echo_time = _local_echo_time.addMSecs(-_spentTime/2-self.difference)
                                self.updateItem(_label, 2, _first_order_time.toString('hh:mm:ss:zzz'))
                                self.updateItem(_label, 6, _documentary_time.toString('hh:mm:ss:zzz'))
                                self.updateItem(_label, 7, _local_echo_time.toString('hh:mm:ss:zzz'))
                                self.updateItem(_label, 8, _server_echo_time.toString('hh:mm:ss:zzz'))
                                self.curFirstOrder = True

                    # if(self.curFirstOrder == None):
                    #     _bestPrice = self.project_totalstructure['bestPrice']
                    #     if(_bestPrice != None):
                    #         _price = int(_bestPrice)
                    #         if(_price == 0):
                    #             _beginPrice = self.project_totalstructure['beginPrice']
                    #             if(_beginPrice != None):
                    #                 self.curFirstOrder = _beginPrice
                    #                 self.curLastOrder = _beginPrice
                    #                 _curTime = QTime.currentTime()
                    #                 if(_curTime.msecsSinceStartOfDay() > _start_time.msecsSinceStartOfDay()):
                    #                     self.updateItem(_label, 2, _curTime.toString('hh:mm:ss:zzz'))
                    #                     self.updateItem(_label, 3, _curTime.toString('hh:mm:ss:zzz'))
                    #                 else:
                    #                     self.updateItem(_label, 2, _start_time.toString('hh:mm:ss:zzz'))
                    #                     self.updateItem(_label, 3, _start_time.toString('hh:mm:ss:zzz'))
                    #     else:
                    #         self.curFirstOrder = _bestPrice
                    #         self.curLastOrder = _bestPrice
                    #         _curTime = QTime.currentTime()
                    #         if(_curTime.msecsSinceStartOfDay() > _start_time.msecsSinceStartOfDay()):
                    #             self.updateItem(_label, 2, _curTime.toString('hh:mm:ss:zzz'))
                    #             self.updateItem(_label, 3, _curTime.toString('hh:mm:ss:zzz'))
                    #         else:
                    #             self.updateItem(_label, 2, _start_time.toString('hh:mm:ss:zzz'))
                    #             self.updateItem(_label, 3, _start_time.toString('hh:mm:ss:zzz'))
                                    
                    # _bestPrice = self.project_totalstructure['bestPrice']
                    # if(_bestPrice != None):
                    #     if(self.curLastOrder != _bestPrice):
                    #         self.curLastOrder = _bestPrice
                    #         _curTime = QTime.currentTime()
                    #         self.updateItem(_label, 3, _curTime.toString('hh:mm:ss:zzz'))



    def updateItem(self, _label, _col, _content):
        _totalrow = self.ui.tableWidget.rowCount()
        curRow = 0
        isContain = False
        if(_totalrow > 0):
            for i in range(_totalrow):
                item = self.ui.tableWidget.item(i, 0)
                if item != None:
                    itemstr = item.text()
                    if(itemstr == _label):
                        isContain = True
                        curRow = i
                        break

        if _totalrow == 0 or isContain == False:
            self.ui.tableWidget.setRowCount(_totalrow + 1)
            _item1 = QTableWidgetItem(_label)
            self.ui.tableWidget.setItem(_totalrow, 0, _item1)
            curRow = _totalrow

        if _content != None:
            _item = self.ui.tableWidget.item(curRow, _col)
            if(_item == None):
                _item = QTableWidgetItem(_content)
                self.ui.tableWidget.setItem(curRow, _col, _item)
            else:
                _itemstr = _item.text()
                if(_itemstr != _content):
                    _item.setText(_content)

        
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
            self.ui.pushButton.setEnabled(False)
            print("test error", res)
            outputStr = 'test error: ' + json.dumps(res)
            self.writeLog(outputStr)
        else:
            self.ui.pushButton_start.setEnabled(True)
            # self.ui.pushButton_stop.setEnabled(True)
            
            dbTime = float(self.get_dbTime())
            now = datetime.now().timestamp()*1000
            self.difference = (now-dbTime)

            outputStr = 'delay time: ' + str(self.difference)
            self.writeLog(outputStr)
            print('delay time', self.difference)
        

            

    def slot_start(self):
        self.orderRun = False
        self.timer.start(10)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)
        self.ui.pushButton.setEnabled(True)
        
        print('start')
        self.writeLog('start')
        
        
    def slot_stop(self):
        self.orderRun = False
        self.timer.stop()
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton.setEnabled(False)
        print('stop')
        self.writeLog('stop')
        
        
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
        _mytime = response.elapsed.total_seconds()
        print("mytime", _mytime)
        print('dbtime', response.text)
        self.responseTime = _mytime * 1000
        realDelay = int(response.text) - self.responseTime
        self.ui.lineEdit_response.setText(str(_mytime*1000))
        return str(realDelay)
    

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


    def post_makeorder(self, matterId, price, quantity):
        url = "https://jy.yectc.com:16952/frontService/ylmt/vendue/trade/open/order/single"
        payload = {
            'matterId': str(matterId),
            'tradeModeId': '1',
            'price': str(price),
            'quantity': str(quantity)
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
            return None
        elif "responseValue" in _res:
            print('order place successfully', _res)
            outputStr = 'order place successfully : ' + url + ' : ' + response.text
            self.writeLog(outputStr)
            return response
        else:
            print('make new order posted', _res)
            outputStr = 'make new order posted : ' + url + ' : ' + response.text
            self.writeLog(outputStr)
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