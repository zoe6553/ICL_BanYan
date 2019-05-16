import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from RadarWindow import *
from PyQt5.QtCore import pyqtSlot

from CommArithmetic import *
from GestureArithmetic import *

import numpy as np

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setWindowTitle('BanYan Demo')
        
        self.setupUi(self)
        self.widget.setVisible(True)
        self.widget_2.setVisible(True)
        self.Ui_Init()

    def Ui_Init(self):
        ## 设备选择下拉框:USB,UART,文件打开
        self.DevSelectBox.addItem('USB Serial')
        self.DevSelectBox.addItem('COM5')
        self.DevSelectBox.addItem('From File')
        self.DevSelectBox.setCurrentIndex(0)
        self.devSelect = 0
        self.DevSelectBox.currentIndexChanged.connect(self.devchange)

        ## 模式选择：距离-角度；区域检测；手势识别
        self.Module_Box.addItems(['距离-角度','区域检测','手势识别'])
        self.Module_Box.setCurrentIndex(0)
        self.moduleSelect = 0
        self.Module_Box.currentIndexChanged.connect(self.modulechange)

        ## 通道数选择：2； 4
        self.Channel_Box.addItems(['2', '4'])
        self.Channel_Box.setCurrentIndex(0)
        self.channelSelect = 0
        self.Channel_Box.currentIndexChanged.connect(self.channelchange)

## ######################## 自定义槽函数 ###############################
    def devchange(self,index):
        self.devSelect = index
        if index is 0:
            self.bt_connect.setText('连接')
        elif index is 1:
            self.bt_connect.setText('连接')
        elif index is 2:
            self.bt_connect.setText('目录')

    def modulechange(self,index):
        self.moduleSelect = index

    def channelchange(self,index):
        self.channelSelect = index

    def find_chirp(self):
        print('Begin Find Chirp')
        self.timer.stop()
        self.RawData_Martix_I_1, self.RawData_Martix_Q_1, self.RawData_Martix_I_2, self.RawData_Martix_Q_2 = \
            FindChirp(4,self.RawData_I_1, self.RawData_Q_1, self.RawData_I_2, self.RawData_Q_2)
        print('Find Chirp End')
## #####################################################################

## ######################## PyQt槽函数 #################################
    ## 连接/目录 按钮 slot
    @pyqtSlot()
    def on_bt_connect_clicked(self):
        if self.devSelect is 0:
            print('ToDo')
        elif self.devSelect is 1:
            print('ToDo')
        elif self.devSelect is 2:
            file,ok = QFileDialog.getOpenFileName(self, "打开文件", "./", "Data Files (*.dat);;Text Files (*.txt)")
            adcData = np.fromfile(file,dtype = np.int16)
            print('ReadFromFile')
            self.RawData_I_1 = adcData[::4]
            self.RawData_Q_1 = adcData[1::4]
            self.RawData_I_2 = adcData[3::4]
            self.RawData_Q_2 = adcData[4::4]
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.find_chirp)
            self.timer.start(10)  # 触发的时间间隔为10毫秒
            print('ReadFromFile End')

    @pyqtSlot()
    def on_bt_start_clicked(self):
        #if self.devSelect == 2:

        self.widget.setVisible(True)
        self.widget.mpl.plotFileData(4,self.RawData_Martix_I_1, self.RawData_Martix_Q_1, self.RawData_Martix_I_2, self.RawData_Martix_Q_2)
        #self.widget_2.setVisible(True)
        #self.widget_2.mpl.start_dynamic_plot()

    @pyqtSlot()
    def on_bt_finish_clicked(self):
        self.close()
## #####################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    app.exec_()
