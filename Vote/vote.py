# -*- coding: utf-8 -*-
'''
# Created on Feb-21-20 20:58
# vote.py
# @author: ss
投票程序模块
'''

import sys
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                        QVBoxLayout, QHBoxLayout,
                        QMessageBox, QPushButton,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon

import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from APP.util import center
from Database.launch import check_captcha, getVoteContent
from Database.vote import getVoteData
from Vote.voteview import Voteview

class VoteWindow(QWidget):

    def __init__(self, usr):
        super().__init__()
        self.usr = usr
        self.voteview = None
        self.initUI()

    def initUI(self):

        captcha = QLabel('邀请码: ')
        self.captchaInput = QLineEdit()

        tophbox = QHBoxLayout()
        tophbox.addWidget(captcha)
        tophbox.addWidget(self.captchaInput)

        self.confirmButton = QPushButton('进入')
        self.confirmButton.setFont(QFont('黑体', 12))
        self.confirmButton.setIcon(QIcon('./image/enter.png'))
        self.confirmButton.clicked.connect(self.onConfirm)

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addWidget(self.confirmButton)
        downhbox.addStretch(1)

        totalLayout = QVBoxLayout()
        totalLayout.addLayout(tophbox)
        totalLayout.addLayout(downhbox)

        self.setLayout(totalLayout)

        center(self)
        self.resize(400, 150)
        self.setWindowTitle('参与投票')
        self.setWindowIcon(QIcon('./image/vote.jpg'))
    
    def onConfirm(self):
        
        captcha = self.captchaInput.text()
        if captcha == '':
            QMessageBox.warning(self, 'warning', '请输入邀请码', QMessageBox.Yes)
        else:
            flag = check_captcha(captcha)
            if flag == 0:
                QMessageBox.information(self, 'sorry', '后端数据库出了问题', QMessageBox.Yes)
            elif flag == 1:
                QMessageBox.information(self, 'sorry', '该活动不存在, 请确认验证码是否正确', QMessageBox.Yes)
            else:
                data = getVoteContent(captcha)
                title, votelimit = data[0], data[1]
                data = getVoteData(captcha)
                self.voteview = Voteview(self.usr, title, data, votelimit, captcha)
                self.voteview.show()
                self.showMinimized()

            self.captchaInput.clear()

if __name__ == "__main__":
    usr = 'ss'
    
    app = QApplication(sys.argv)
    voteWindow = VoteWindow(usr)
    voteWindow.show()
    sys.exit(app.exec_())