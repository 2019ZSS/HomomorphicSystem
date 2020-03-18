# -*- coding: utf-8 -*-
'''
# Created on Feb-21-20 14:30
# voteview.py
# @author: ss
投票窗口动态演示
'''

import sys
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                        QVBoxLayout, QHBoxLayout,
                        QFrame, QMessageBox, QPushButton,
                        QCheckBox, 
                        QApplication)
from PyQt5.QtGui import QFont, QIcon

import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from APP.util import center
from KeyGen.keyGen import openKey
from Database.vote import getVotenum, getVoteData, updataUsrRecord
from Database.launch import updateTotal

class Voteview(QWidget):
    '''
    usr: 当前用户
    title（str): 活动标题
    data(choice(str), tag(int)): 投票活动数据
    votelimt(int): 一个人最多可以投多少票
    '''
    def __init__(self, usr, title, data, votelimit=1, captcha=None):
        super().__init__()
        self.usr = usr 
        self.votelimit = votelimit
        self.captcha = captcha
        self.initUI(title, data)

    def initUI(self, title, data):

        title = QLabel(title)
        title.setFont(QFont('微软雅黑', 15))
        
        tophbox = QHBoxLayout()
        tophbox.addStretch(1)
        tophbox.addWidget(title)
        tophbox.addStretch(1)

        self.checkBox = []
        self.num = len(data)
        self.createCheckBox(data)
        
        midvbox = QVBoxLayout()
        for x in self.checkBox:
            midvbox.addWidget(x)
        
        midhbox = QHBoxLayout()
        midhbox.addStretch(1)
        midhbox.addLayout(midvbox)
        midhbox.addStretch(1)
        midhbox.setStretchFactor(midhbox, 2)

        midFrame = QFrame()
        midFrame.setFrameShape(QFrame.WinPanel)
        midFrame.setLayout(midhbox)

        voteuse = QLabel('当前可投票数: ')
        self.voteuseLine = QLineEdit()
        self.voteuseLine.setReadOnly(True)
        self.getVotenum()

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addWidget(voteuse)
        downhbox.addWidget(self.voteuseLine)
        downhbox.addStretch(1)

        self.confirmButton = QPushButton('投票')
        self.confirmButton.setFont(QFont('黑体', 12))
        self.confirmButton.setIcon(QIcon('./image/ok.png'))
        self.confirmButton.clicked.connect(self.onConfirm)

        bottomhbox = QHBoxLayout()
        bottomhbox.addStretch(1)
        bottomhbox.addWidget(self.confirmButton)
        bottomhbox.addStretch(1)

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(tophbox)
        totalLayout.addWidget(midFrame)
        totalLayout.addLayout(downhbox)
        totalLayout.addLayout(bottomhbox)

        self.setLayout(totalLayout)

        center(self)
        self.resize(400, 300)
        self.setWindowTitle('投票')
        self.setWindowIcon(QIcon('./image/voteview.png'))

    def createCheckBox(self, data):
        for x in data:
            text = x[0] + '-' + str(x[1])
            checkBox = QCheckBox(text)
            checkBox.setFont(QFont('宋体', 16))
            self.checkBox.append(checkBox)

    def getVotenum(self):
        if self.captcha is None:
            self.voteuseLine.setText(str(self.votelimit))
        else:
            votenum = getVotenum(self.captcha, self.usr, self.votelimit)
            self.voteuseLine.setText(str(votenum))

    def onConfirm(self):
        if self.captcha is None:
            QMessageBox.warning(self, 'warning', '这只是一个预览效果', QMessageBox.Yes)
            return 
        if int(self.voteuseLine.text()) == 0:
            QMessageBox.information(self, 'soryy', '您的投票次数已经用光', QMessageBox.Yes)
            return None
        cnt = 0
        m = 1
        for x in self.checkBox:
            if x.isChecked() == True:
                cnt = cnt + 1
                if cnt > int(self.voteuseLine.text()):
                    QMessageBox.warning(self, 'warning', '您的票数不足够, 请重新勾选', QMessageBox.Yes)
                    return None
                text = x.text()
                data = text.split('-')
                m = m * int(data[1])
        if cnt == 0:
            QMessageBox.warning(self, 'warning', '您选选择任何选项进行投票', QMessageBox.Yes)
            return None                
        QMessageBox.information(self, '提示', '请准备好加载加密公钥', QMessageBox.Yes)
        pubkey = openKey(self, 0)
        if pubkey == False:
            QMessageBox.information(self, '提示', '您已取消本次加密', QMessageBox.Yes)
            return None
        C = pubkey.encrypt_int(m)
        updateTotal(self.captcha, pubkey, C)
        votenum = int(self.voteuseLine.text()) - cnt
        updataUsrRecord(self.captcha, self.usr, votenum)
        self.getVotenum()
        QMessageBox.information(self, '提示', '投票成功', QMessageBox.Yes)

if __name__ == "__main__":
    
    usr = 'ss'
    title = 'vote'
    data = [['ss', 2], ['ff', 3], ['zz', 5], ['yy', '7']]
    votelimit = 3
    captcha = 'c3d509ebd011c4428abad04c1f171ac0'
    data = getVoteData(captcha)

    app = QApplication(sys.argv)
    voteview = Voteview(usr=usr, title=title, data=data, votelimit=votelimit, captcha=captcha)
    voteview.show()
    sys.exit(app.exec_())
