# -*- coding: utf-8 -*-
'''
# Created on Feb-22-20 20:54
# view.py
# @author: ss
'''

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                        QGridLayout, QVBoxLayout, QHBoxLayout,
                        QFrame, QMessageBox, QPushButton,
                        QTextEdit,
                        QTableWidget,
                        QRadioButton,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QIntValidator
import sip

import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from APP.util import center
from KeyGen.keyGen import openKey
from Database.view import getVoteActivities, delVoteActivity, showVoteResult, drawResult
from Database.launch import getTotal

class ViewWindow(QWidget):

    def __init__(self, usr):
        super().__init__()
        self.usr = usr 
        self.initUI()
    
    def initUI(self):

        self.showtable = None
        self.radioButtons = []
        self.rownum = 0
        self.colnum = 2

        self.cenerLayout = QVBoxLayout()
        self.createTable(getVoteActivities(self.usr))

        self.showButton = QPushButton('查看结果')
        self.showButton.setFont(QFont('微软雅黑'))
        self.showButton.setIcon(QIcon('./image/search.png'))
        self.showButton.clicked.connect(self.onShow)
        
        self.delButton = QPushButton('删除活动')
        self.delButton.setFont(QFont('微软雅黑'))
        self.delButton.setIcon(QIcon('./image/delete.jpg'))
        self.delButton.clicked.connect(self.onDel)

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addWidget(self.showButton)
        downhbox.addWidget(self.delButton)
        downhbox.addStretch(1)

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(self.cenerLayout)
        totalLayout.addLayout(downhbox)
        totalLayout.setStretchFactor(self.cenerLayout, 3)
        totalLayout.setStretchFactor(downhbox, 1)

        self.setLayout(totalLayout)

        center(self)
        self.resize(600, 270)
        self.setWindowTitle('投票查看')
        self.setWindowIcon(QIcon('./image/view.png'))

    def delTable(self):
        if self.rownum:
            self.cenerLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)
            self.rownum = 0

    def createTable(self, data):
        self.delTable()
        self.rownum = len(data)
        collists = ['', '活动名称', '邀请码']
        self.colnum = len(collists)
        self.showtable = QTableWidget(self.rownum, self.colnum)
        self.showtable.setHorizontalHeaderLabels(collists)
        self.radioButtons = []
        for i in range(self.rownum):
            self.radioButtons.append(QRadioButton())
            self.showtable.setCellWidget(i, 0, self.radioButtons[i])
            for j in range(1, self.colnum):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j - 1]))
        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.showtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.cenerLayout.addWidget(self.showtable)

    def onShow(self):
        for i in range(self.rownum):
            if self.radioButtons[i].isChecked() == True:
                QMessageBox.information(self, '提示', '请准备加载解密的私钥', QMessageBox.Yes)
                prikey = openKey(self, 1)
                if prikey == False:
                    return 
                captcha = self.showtable.item(i, 2).text()
                total = getTotal(captcha)
                res = showVoteResult(captcha, total, prikey)
                drawResult(res)

    def onDel(self):
        for i in range(self.rownum):
            if self.radioButtons[i].isChecked() == True:
                reply = QMessageBox.question(self, '警告', '您确认删除该活动?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    captcha = self.showtable.item(i, 2).text()
                    delVoteActivity(captcha)
                    self.createTable(getVoteActivities(self.usr))
                return 

if __name__ == "__main__":
    usr = 'ss'

    app = QApplication(sys.argv)
    viewWindow = ViewWindow(usr)
    viewWindow.show()
    sys.exit(app.exec_())

