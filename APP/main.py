# -*- coding: utf-8 -*-
'''
# Created on Feb-20-20 15:05
# main.py
# @author: ss
'''

'''
应用窗口主程序
'''
import sys
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit,
                        QGridLayout, QVBoxLayout, QHBoxLayout,
                        QFrame, QMessageBox, QPushButton,
                        QAction,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon

import login
import register
import util
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from KeyGen.keyGen import KeyGenWindow
from Launch.launch import LaunchWindow
from Vote.vote import VoteWindow
from View.view import ViewWindow

class CenterWidget(QWidget):
    
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI(parent)
        self.keyGenWindows = []
        self.launchWindows = []
        self.voteWindows = []
        self.viewWindows = []
    
    def initUI(self, parent):

        keyGenButton = QPushButton('密钥生成', self)
        keyGenButton.setIcon(QIcon('./image/keyGen.png'))
        keyGenButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        keyGenButton.clicked.connect(lambda: self.onkeyGen(parent))

        launchButton = QPushButton('发起投票', self)
        launchButton.setIcon(QIcon('./image/launch.png'))
        launchButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        launchButton.clicked.connect(lambda: self.onLaunch(parent))

        voteButton = QPushButton('进行投票', self)
        voteButton.setIcon(QIcon('./image/vote.jpg'))
        voteButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        voteButton.clicked.connect(lambda : self.onVote(parent))

        viewButton = QPushButton('查看投票', self)
        viewButton.setIcon(QIcon('./image/view.png'))
        viewButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        viewButton.clicked.connect(lambda: self.onView(parent))

        vbox = QVBoxLayout()
        vbox.addWidget(keyGenButton)
        vbox.addWidget(launchButton)
        vbox.addWidget(voteButton)
        vbox.addWidget(viewButton)

        midhobx = QHBoxLayout()
        midhobx.addStretch(1)
        midhobx.addLayout(vbox)
        midhobx.addStretch(1)

        centerFrame = QFrame(self)
        centerFrame.setFrameShape(QFrame.WinPanel)
        centerFrame.setLayout(midhobx)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(centerFrame)
        hbox.addStretch(1)
        hbox.setStretchFactor(centerFrame, 6)
        self.setLayout(hbox)

    def onkeyGen(self, parent):
        if parent is not None:
            self.keyGenWindows.append(KeyGenWindow())
            self.keyGenWindows[-1].show()
            parent.showMinimized()

    def onLaunch(self, parent):
        if parent is not None:
            self.launchWindows.append(LaunchWindow(parent.usr))
            self.launchWindows[-1].show()
            parent.showMinimized()
    
    def onVote(self, parent):
        if parent is not None:
            self.voteWindows.append(VoteWindow(parent.usr))
            self.voteWindows[-1].show()
            parent.showMinimized()

    def onView(self, parent):
        if parent is not None:
            self.viewWindows.append(ViewWindow(parent.usr))
            self.viewWindows[-1].show()
            parent.showMinimized()

class MainWindow(QMainWindow):

    def __init__(self, usr=None):
        super().__init__()
        self.usr = usr
        self.loginWindow = None 
        self.initUI()
    
    def initUI(self):
        
        #中心布局
        self.setCentralWidget(CenterWidget(self))

        #菜单栏设置
        menu = self.menuBar().addMenu('账号中心')

        signoutAct = QAction('注销', self) 
        signoutAct.triggered.connect(self.onSignout)
        menu.addAction(signoutAct)

        exitAct = QAction('退出', self)
        exitAct.triggered.connect(self.onExit)
        menu.addAction(exitAct)

        #整体布局
        self.resize(450, 300)
        util.center(self)
        self.setFont(QFont("Microsoft YaHei", 11))
        self.setWindowTitle('电子投票系统')
        self.setWindowIcon(QIcon('./image/user.png'))
        
        self.bottomlbl = QLabel()
        self.bottomlbl.setFont(QFont("宋体"))
        self.statusBar().addPermanentWidget(self.bottomlbl)
        self.showbottom()

    def showbottom(self):
        #设置底部状态栏, 显示当前登录的用户
        if self.usr is not None:
            s = "欢迎你: " + self.usr
            self.bottomlbl.setText(s)
        
    #注销重新登录
    def onSignout(self):
        if self.loginWindow is not None:
            self.close()
            self.loginWindow.show()
    
    def onExit(self):
        self.close()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    loginWindow = login.LoginWindow()
    registerWindow = register.RegisterWindow()
    mainWindow = MainWindow()
    mainWindow.loginWindow = loginWindow 
    registerWindow.loginWindow = loginWindow
    loginWindow.registerWindow = registerWindow
    loginWindow.mainWindow = mainWindow
    loginWindow.show()
    sys.exit(app.exec_())