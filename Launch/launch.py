# -*- coding: utf-8 -*-
'''
# Created on Feb-21-20 11:13
# launch.py
# @author: ss
实现投票发起
'''

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                        QGridLayout, QVBoxLayout, QHBoxLayout,
                        QFrame, QMessageBox, QPushButton,
                        QTextEdit,
                        QTableWidget,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QIntValidator
import sip

import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from APP.util import center
from HE.util import create_primes
from Vote.voteview import Voteview
from KeyGen.keyGen import openKey
from Database.util import md5
from Database.launch import insert_launch, del_launch, insert_votedata


class LaunchWindow(QWidget):

    def __init__(self, usr=None):
        super().__init__()
        self.usr = usr
        self.initUI()
    
    def initUI(self):
        
        title = QLabel('活动标题:')
        title.setFont(QFont('黑体', 10))
        # title.setAlignment(Qt.AlignHCenter)
        self.titleInput = QLineEdit()

        tophbox = QHBoxLayout()
        tophbox.addStretch(1)
        tophbox.addWidget(title)
        tophbox.addWidget(self.titleInput)
        tophbox.addStretch(1)

        choice = QLabel('选项: ')
        choice.setFont(QFont('宋体'))
        self.choiceInput = QLineEdit()

        lefthbox1 = QHBoxLayout()
        lefthbox1.addWidget(choice)
        lefthbox1.addWidget(self.choiceInput)
        
        self.appendButton = QPushButton('添加')
        self.appendButton.setFont(QFont('黑体'))
        self.appendButton.setIcon(QIcon('./image/view.png'))
        self.appendButton.clicked.connect(self.onAppend)

        lefthbox2 = QHBoxLayout()
        lefthbox2.addStretch(1)
        lefthbox2.addWidget(self.appendButton)
        lefthbox2.addStretch(1)

        votelimit = QLabel('个人有效票数: ')
        self.votelimitInput = QLineEdit()
        self.votelimitInput.setPlaceholderText('1')
        intValidator = QIntValidator()
        intValidator.setRange(1, 2147483647)
        self.votelimitInput.setValidator(intValidator)

        lefthbox3 = QHBoxLayout()
        lefthbox3.addWidget(votelimit)
        lefthbox3.addWidget(self.votelimitInput)

        self.viewButton = QPushButton('预览')
        self.viewButton.setIcon(QIcon('./image/view.png'))
        self.viewButton.clicked.connect(self.onView)

        self.saveButton = QPushButton('保存')
        self.saveButton.setIcon(QIcon('./image/save.png'))
        self.saveButton.clicked.connect(self.onSave)

        lefthbox4 = QHBoxLayout()
        lefthbox4.addWidget(self.viewButton)
        lefthbox4.addWidget(self.saveButton)

        leftLayout = QVBoxLayout()
        leftLayout.addLayout(lefthbox1)
        leftLayout.addLayout(lefthbox2)
        leftLayout.addLayout(lefthbox3)
        leftLayout.addLayout(lefthbox4)

        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.WinPanel)
        leftFrame.setLayout(leftLayout)

        self.righLayout = QVBoxLayout()

        self.tabledata = []
        self.rownum = len(self.tabledata)
        self.showtable = None

        self.createTable(self.tabledata)

        downhobx = QHBoxLayout()
        downhobx.addWidget(leftFrame)
        downhobx.addLayout(self.righLayout)
        downhobx.setStretchFactor(leftFrame, 1)
        downhobx.setStretchFactor(self.righLayout, 1)

        self.captchalbl = QLineEdit()
        self.captchalbl.setText('活动邀请码: ')

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(tophbox)
        totalLayout.addLayout(downhobx)
        totalLayout.addWidget(self.captchalbl)

        self.setLayout(totalLayout)

        center(self)
        self.resize(600, 300)
        self.setWindowTitle('发起投票')
        self.setWindowIcon(QIcon('./image/launch.png'))
    
    def getTableData(self):
        data = []
        for i in range(self.rownum):
            tmp = []
            for j in range(self.colnum):
                tmp.append(self.showtable.item(i, 0).text())
            data.append(tmp)
        return data

    def onAppend(self):
        choice = self.choiceInput.text()
        if choice == '':
            QMessageBox.warning(self, 'warning', '选项不能为空', QMessageBox.Yes)
        else:
            if self.rownum:
                self.tabledata = self.getTableData()
            self.tabledata.append([choice])
            self.createTable(self.tabledata)
            QMessageBox.information(self, 'ok', '选项添加成功', QMessageBox.Yes)
            self.choiceInput.clear()

    def Check(self):
        if self.rownum == 0:
            QMessageBox.warning(self, 'warning', '您还没有创建任何候选项', QMessageBox.Yes)
            return False
        if self.rownum < 2:
            QMessageBox.warning(self, 'warning', '投票至少需要两个选项', QMessageBox.Yes)
            return False
        title = self.titleInput.text()
        if title == '':
            QMessageBox.warning(self, 'warning', '请输入活动标题', QMessageBox.Yes)
            return False
        votelimit = self.votelimitInput.text()
        if votelimit == '':
            QMessageBox.warning(self, 'warning', '有效票数不能为零', QMessageBox.Yes)
            return False
        return True

    def onView(self):
        if self.Check() == True:
            title = self.titleInput.text()
            votelimit = self.votelimitInput.text()
            votelimit = int(votelimit)
            primes = create_primes(self.rownum)
            self.tabledata = self.getTableData()
            data = []
            for i in range(self.rownum):
                data.append([self.tabledata[i][0], primes[i]])
            self.voteview = Voteview(self.usr, title, data, votelimit)
            self.voteview.show()
            self.showMinimized()
    
    def onSave(self):
        if self.Check() == True:
            title = self.titleInput.text()
            votelimit = self.votelimitInput.text()
            votelimit = int(votelimit)
            primes = create_primes(self.rownum)
            self.tabledata = self.getTableData()
            data = []
            for i in range(self.rownum):
                data.append([self.tabledata[i][0], primes[i]])
            reply = QMessageBox.question(self, '询问', '确认保存?', 
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                s = self.usr + title + str(votelimit)
                for i in range(len(data)):
                    s = s + data[i][0] + '-' + str(data[i][1])
                captcha = md5(s)
                pubkey = openKey(self, 0)
                if pubkey == False:
                    return
                C = pubkey.encrypt_int(1)
                C = str(C[0]) + ',' + str(C[1])
                flag = insert_launch(self.usr, title, captcha, votelimit, C)
                if flag == 0:
                    QMessageBox.information(self, 'sorry', '后台数据库出了点问题', QMessageBox.Yes)
                elif flag == -1:
                    QMessageBox.warning(self, 'warning', '您已经保存过该活动', QMessageBox.Yes)
                else:
                    for x in data:
                        flag = insert_votedata(captcha, x[0], x[1])
                        if flag == 0:
                            del_launch(captcha)
                            QMessageBox.information(self, 'sorry', '后台数据库出了点问题', QMessageBox.Yes)
                            return 
                        elif flag == -1:
                            QMessageBox.warning(self, 'warning', '生成标记不是素数', QMessageBox.Yes)
                    self.captchalbl.setText('投票邀请码: ' + captcha)
                    QMessageBox.information(self, '恭喜', '保存成功', QMessageBox.Yes)

    def delTable(self):
        if self.showtable is not None:
            self.righLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)
            self.rownum = 0

    def createTable(self, data):
        self.delTable()
        self.rownum = len(data)
        collists = ['候选']
        self.colnum = len(collists)
        self.showtable = QTableWidget(self.rownum, self.colnum)
        self.showtable.setHorizontalHeaderLabels(collists)
        for i in range(self.rownum):
            for j in range(self.colnum):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.righLayout.addWidget(self.showtable)

if __name__ == "__main__":
    usr = 'ss'

    app = QApplication(sys.argv)
    launchWindow = LaunchWindow(usr)
    launchWindow.show()
    sys.exit(app.exec_())

        


