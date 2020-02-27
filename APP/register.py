# -*- coding: utf-8 -*-
'''
# Created on Feb-20-20 13:55
# register.py
# @author: ss
'''

'''
用户注册界面设计
'''

import sys
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QWidget, QWidget, QLabel, QLineEdit,
                        QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
                        QFrame, QMessageBox, QPushButton,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import util
import login
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from Database.util import register

class RegisterWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.loginWindow = None
        self.initUI()
    
    def initUI(self):

        user = QLabel('账号: ')
        pwd = QLabel('密码: ')
        cpwd = QLabel('确认：')

        self.userInput = QLineEdit()
        self.userInput.setPlaceholderText('自定义您的用户名')

        self.pwdInput = QLineEdit()
        self.pwdInput.setPlaceholderText('请输入您的密码')
        self.pwdInput.setEchoMode(QLineEdit.Password) #密码不以明文显示

        self.cpwdInput = QLineEdit()
        self.cpwdInput.setPlaceholderText('请再次输入密码')
        self.cpwdInput.setEchoMode(QLineEdit.Password)

        self.registerButton = QPushButton('注册', self)
        self.registerButton.setIcon(QIcon('./image/register.png'))
        self.registerButton.clicked.connect(self.onRegister)

        self.loginButton = QPushButton('登录', self)
        self.loginButton.setFont(QFont('黑体'))
        self.loginButton.setIcon(QIcon('./image/start.png'))
        self.loginButton.clicked.connect(self.onLogin)

        formlayout = QFormLayout()
        formlayout.addRow(user, self.userInput)
        formlayout.addRow(pwd, self.pwdInput)
        formlayout.addRow(cpwd, self.cpwdInput)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.registerButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(formlayout)
        vbox.addLayout(hbox)

        centerFrame = QFrame(self)
        centerFrame.setFrameShape(QFrame.WinPanel)
        centerFrame.setLayout(vbox)

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addStretch(1)
        downhbox.addWidget(self.loginButton)

        totalLayout = QVBoxLayout()
        totalLayout.addWidget(centerFrame)
        totalLayout.addLayout(downhbox)

        self.setLayout(totalLayout)
        self.resize(350, 250)
        util.center(self)
        self.setFont(QFont('宋体', 10))
        self.setWindowTitle('注册')
        self.setWindowIcon(QIcon('./image/record.png'))


    def onRegister(self):
        print(233)
    
    def onLogin(self):
        if self.loginWindow is not None:
            self.userInput.clear()
            self.pwdInput.clear()
            self.cpwdInput.clear()
            self.close()
            self.loginWindow.show()
    
    def onRegister(self):

        usr = self.userInput.text()
        pwd = self.pwdInput.text()
        cpwd = self.cpwdInput.text()

        if usr == '':
            QMessageBox.warning(self, 'warning', '用户名不能为空', QMessageBox.Yes)
        elif pwd == '':
            QMessageBox.warning(self, 'warning', '请输入您的密码', QMessageBox.Yes)
        elif cpwd == '':
            QMessageBox.warning(self, 'warning', '请再次输入您的密码', QMessageBox.Yes)
        elif cpwd != pwd:
            QMessageBox.warning(self, 'warning', '两次输入的密码不一致', QMessageBox.Yes)
        else:
            flag = register(usr, pwd)
            if flag == 1:
                QMessageBox.information(self, '恭喜', '注册成功')
                self.onLogin()
            elif flag == 0:
                QMessageBox.information(self, 'sorry', '程序出了点bug', QMessageBox.Yes)
            elif flag == -1:
                QMessageBox.information(self, 'sorry', '用户名已存在', QMessageBox.Yes)

        self.userInput.clear()
        self.pwdInput.clear()
        self.cpwdInput.clear()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    registerWindow = RegisterWindow()
    registerWindow.show()
    sys.exit(app.exec_())


    
