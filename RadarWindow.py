# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RadarWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1345, 975)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = MatplotlibWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(150, 10, 921, 471))
        self.widget.setObjectName("widget")
        self.widget_2 = MatplotlibWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(150, 500, 921, 411))
        self.widget_2.setObjectName("widget_2")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1080, 80, 261, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(92, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.Channel_Box = QtWidgets.QComboBox(self.layoutWidget)
        self.Channel_Box.setMinimumSize(QtCore.QSize(161, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Channel_Box.setFont(font)
        self.Channel_Box.setObjectName("Channel_Box")
        self.horizontalLayout_4.addWidget(self.Channel_Box)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(1080, 860, 254, 53))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.bt_start = QtWidgets.QPushButton(self.layoutWidget1)
        self.bt_start.setMinimumSize(QtCore.QSize(80, 51))
        self.bt_start.setMaximumSize(QtCore.QSize(80, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_start.setFont(font)
        self.bt_start.setObjectName("bt_start")
        self.horizontalLayout_2.addWidget(self.bt_start)
        self.bt_start_2 = QtWidgets.QPushButton(self.layoutWidget1)
        self.bt_start_2.setMinimumSize(QtCore.QSize(80, 51))
        self.bt_start_2.setMaximumSize(QtCore.QSize(80, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_start_2.setFont(font)
        self.bt_start_2.setObjectName("bt_start_2")
        self.horizontalLayout_2.addWidget(self.bt_start_2)
        self.bt_finish = QtWidgets.QPushButton(self.layoutWidget1)
        self.bt_finish.setMinimumSize(QtCore.QSize(80, 51))
        self.bt_finish.setMaximumSize(QtCore.QSize(80, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_finish.setFont(font)
        self.bt_finish.setObjectName("bt_finish")
        self.horizontalLayout_2.addWidget(self.bt_finish)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(1080, 50, 261, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.layoutWidget2.setFont(font)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget2)
        self.label.setMinimumSize(QtCore.QSize(92, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Module_Box = QtWidgets.QComboBox(self.layoutWidget2)
        self.Module_Box.setMinimumSize(QtCore.QSize(161, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Module_Box.setFont(font)
        self.Module_Box.setObjectName("Module_Box")
        self.horizontalLayout.addWidget(self.Module_Box)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(1080, 10, 259, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.widget1.setFont(font)
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.DevSelectBox = QtWidgets.QComboBox(self.widget1)
        self.DevSelectBox.setMinimumSize(QtCore.QSize(150, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DevSelectBox.setFont(font)
        self.DevSelectBox.setObjectName("DevSelectBox")
        self.horizontalLayout_3.addWidget(self.DevSelectBox)
        spacerItem = QtWidgets.QSpacerItem(20, 23, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.bt_connect = QtWidgets.QPushButton(self.widget1)
        self.bt_connect.setMinimumSize(QtCore.QSize(75, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_connect.setFont(font)
        self.bt_connect.setObjectName("bt_connect")
        self.horizontalLayout_3.addWidget(self.bt_connect)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1345, 23))
        self.menubar.setObjectName("menubar")
        self.menu_F = QtWidgets.QMenu(self.menubar)
        self.menu_F.setObjectName("menu_F")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.OpenRegFile_action = QtWidgets.QAction(MainWindow)
        self.OpenRegFile_action.setObjectName("OpenRegFile_action")
        self.NewRegFile_action = QtWidgets.QAction(MainWindow)
        self.NewRegFile_action.setObjectName("NewRegFile_action")
        self.DelRegFile_action = QtWidgets.QAction(MainWindow)
        self.DelRegFile_action.setObjectName("DelRegFile_action")
        self.menu_F.addAction(self.OpenRegFile_action)
        self.menu_F.addAction(self.NewRegFile_action)
        self.menu_F.addAction(self.DelRegFile_action)
        self.menubar.addAction(self.menu_F.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "通道数量："))
        self.bt_start.setText(_translate("MainWindow", "开始"))
        self.bt_start_2.setText(_translate("MainWindow", "配置"))
        self.bt_finish.setText(_translate("MainWindow", "停止"))
        self.label.setText(_translate("MainWindow", "模式选择："))
        self.bt_connect.setText(_translate("MainWindow", "连接"))
        self.menu_F.setTitle(_translate("MainWindow", "文件(&F)"))
        self.OpenRegFile_action.setText(_translate("MainWindow", "打开寄存器文件"))
        self.OpenRegFile_action.setShortcut(_translate("MainWindow", "Alt+O"))
        self.NewRegFile_action.setText(_translate("MainWindow", "新建寄存器文件"))
        self.NewRegFile_action.setShortcut(_translate("MainWindow", "Alt+N"))
        self.DelRegFile_action.setText(_translate("MainWindow", "删除寄存器文件"))

from MatplotlibWidget import MatplotlibWidget
