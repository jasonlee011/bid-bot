# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tool_ch.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1085, 405)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton_stop = QtWidgets.QPushButton(Dialog)
        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.gridLayout.addWidget(self.pushButton_stop, 2, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 3)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_user = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.gridLayout.addWidget(self.lineEdit_user, 0, 1, 1, 1)
        self.pushButton_test = QtWidgets.QPushButton(Dialog)
        self.pushButton_test.setObjectName("pushButton_test")
        self.gridLayout.addWidget(self.pushButton_test, 0, 2, 1, 1)
        self.pushButton_start = QtWidgets.QPushButton(Dialog)
        self.pushButton_start.setEnabled(False)
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout.addWidget(self.pushButton_start, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEdit_token = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_token.setObjectName("lineEdit_token")
        self.gridLayout.addWidget(self.lineEdit_token, 1, 1, 1, 1)
        self.lineEdit_platid = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_platid.setEnabled(True)
        self.lineEdit_platid.setObjectName("lineEdit_platid")
        self.gridLayout.addWidget(self.lineEdit_platid, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.lineEdit_response = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_response.setEnabled(False)
        self.lineEdit_response.setObjectName("lineEdit_response")
        self.gridLayout.addWidget(self.lineEdit_response, 4, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Token :"))
        self.pushButton_stop.setText(_translate("Dialog", "结束"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "标号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "开始时间"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "首次下单"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "末次下单"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "预计结束"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "实际结束"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "跟单时间"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "本地回显"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "服务器回显"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Dialog", "推荐下单时间"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Dialog", "差时"))
        self.label.setText(_translate("Dialog", "用户 :"))
        self.pushButton_test.setText(_translate("Dialog", "连接"))
        self.pushButton_start.setText(_translate("Dialog", "开始"))
        self.label_4.setText(_translate("Dialog", "场次 :"))
        self.label_3.setText(_translate("Dialog", "切换跟单模式 :"))
        self.radioButton_2.setText(_translate("Dialog", "自动"))
        self.radioButton.setText(_translate("Dialog", "手动"))
        self.pushButton.setText(_translate("Dialog", "跟单"))
        self.label_5.setText(_translate("Dialog", "Response Time :"))