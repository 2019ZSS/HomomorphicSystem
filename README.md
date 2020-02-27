## 基于同态加密的匿名电子投票系统

### 项目简介

~~寒假期间闷的慌,突然灵感，做出来消遣时光的产品。~~
保证**投票发起者，公证方，投票人**三方的隐私安全。
包含**密钥生成，发起投票，进行投票，查看结果**四个功能。

**目前**主要只实现了**基于ElGamal算法**乘同态方案
**至于基于全同态**的实现方案，等更(~~咕咕咕~~)

### 项目环境
```
    基于Pyqt5进行可视化开发
    本人环境: win10 python3.7 + mysql
    1.python 包环境安装: pip install requirements.txt
    2.mysql 数据库搭建: create.sql
```

### 项目文件目录
```
    -- APP(程序运行主窗口)
        main.py (项目运行主文件)
        login.py 
        register.py
        util.py
    -- Database(连接数据库)
        launch.py
        vote.py
        view.py
        util.py
    -- KeyGen (密钥生成模块)
        keyGen.py
    -- Launch (发起投票模块)
        launch.py
    -- Vote  (进行投票模块)
        vote.py
        voteview.py
    -- View (结果查看模块)
        view.py
    -- HE (同态加密算法实现)
        ElGamal.py ElGamal算法实现
        MHE.py RSA算法实现
        SWHE.py 手动实现的部分全同台加密算法
        util.py 通用数学函数实现
    -- key(存储生成的密钥)
    -- image (可视化界面图标)
    -- paper (一些实现想法的参考论文)
    -- vscoe (vscode编辑器的编辑环境文件, 可忽略)
    -- venv (python虚拟环境, 可忽略)
```




