import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from RadarWindow import *
from PyQt5.QtCore import pyqtSlot

from CommArithmetic import *
from GestureArithmetic import *
from DataRecvThread import *
from DataAlgThread import *
from queue import Queue
from PreDefine import enum

import numpy as np
import serial


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.fftShareBuf = np.zeros([32,256],dtype=np.complex)
        self.setWindowTitle('BanYan Demo')
        self.algThread = DataAlgThread()
        self.recvThread = DataRecvThread()
        self.recvQueue = Queue(10)
        self.sendQueue = Queue(50)
        self.algThread.SetParam(self.recvQueue,self.sendQueue,self.fftShareBuf)
        
        self.setupUi(self)
        self.widget.setVisible(True)
        self.widget_2.setVisible(True)
        self.Ui_Init()

    def Ui_Init(self):
        ## 设备选择下拉框:USB,UART,文件打开
        self.DevSelectBox.addItem('USB Serial')
        self.DevSelectBox.addItem('From File')
        self.SerialList = self.FindCom()

        for i in range(len(self.SerialList)):
            self.DevSelectBox.addItem(self.SerialList[i])
        
        self.DevSelectBox.setCurrentIndex(0)
        self.devSelect = enum.USB_SERIAL
        self.DevSelectBox.currentIndexChanged.connect(self.devchange)

        ## 模式选择：距离-角度；区域检测；手势识别
        self.Module_Box.addItems(['距离-角度','区域检测','手势识别'])
        self.Module_Box.setCurrentIndex(0)
        self.moduleSelect = enum.RANGE_ANGLE_MODE
        self.Module_Box.currentIndexChanged.connect(self.modulechange)

        ## 通道数选择：2； 4
        self.Channel_Box.addItems(['2', '4'])
        self.Channel_Box.setCurrentIndex(0)
        self.channelSelect = enum.TWO_CHANNEL
        self.Channel_Box.currentIndexChanged.connect(self.channelchange)

    def FindCom(self):
        seriallist = []
        for i in range(40):
            name = 'COM'+str(i)
            try:
                ser = serial.Serial(name)
                ser.open
                if ser.is_open is True:
                    seriallist.append(name)
                    ser.close
            except serial.serialutil.SerialException:
                pass
        return seriallist

## ######################## 自定义槽函数 ###############################
    def devchange(self,index):
        self.devSelect = index
        if index is enum.USB_SERIAL:
            self.bt_connect.setText('连接')
        elif index is enum.FILE_SOURCE:
            self.bt_connect.setText('目录')
        elif index > enum.UART_SERIAL:
            self.bt_connect.setText('连接')

    def modulechange(self,index):
        self.moduleSelect = index

    def channelchange(self,index):
        self.channelSelect = index

    def find_chirp(self):
        print('Begin Find Chirp')
        self.RawData_Martix_I_1, self.RawData_Martix_Q_1, self.RawData_Martix_I_2, self.RawData_Martix_Q_2 = \
            FindChirp(4,self.RawData_I_1, self.RawData_Q_1, self.RawData_I_2, self.RawData_Q_2)
        print('Find Chirp End')
## #####################################################################

## ######################## PyQt槽函数 #################################
    ## 连接/目录 按钮 slot
    @pyqtSlot()
    def on_bt_connect_clicked(self):
        self.algThread.start()
        if self.devSelect is enum.USB_SERIAL:
            print('ToDo')
        elif self.devSelect is enum.FILE_SOURCE:
            file,ok = QFileDialog.getOpenFileName(self, "打开文件", "./", "Data Files (*.dat);;Text Files (*.txt)")
            self.recvThread.SetParam(enum.FILE_SOURCE,file,self.recvQueue)
        elif self.devSelect >= enum.UART_SERIAL:
            SerialName = self.SerialList[self.devSelect-2]
            self.serial = serial.Serial()
            self.serial.baudrate    = 115200
            self.serial.port        = SerialName
            self.serial.timeout     = 2
            self.recvThread.SetParam(enum.UART_SERIAL,self.serial,self.recvQueue)
            #if self.serial.is_open:
            #    self.serial.close()
            #self.serial.open()
            #if self.serial.is_open:
            #    print('Serial Open Success!')
            #    self.recvThread.SetParam(enum.UART_SERIAL,self.serial,self.recvQueue)
            #else:
            #    print('Serial Open Fail')

    @pyqtSlot()
    def on_bt_start_clicked(self):
        #if self.devSelect == 2:
        self.recvThread.start()
        self.widget.setVisible(True)
        #self.widget.mpl.plotFileData(4,self.RawData_Martix_I_1, self.RawData_Martix_Q_1, self.RawData_Martix_I_2, self.RawData_Martix_Q_2)
        self.widget.mpl.plotData(self.sendQueue)
        #self.widget_2.setVisible(True)
        #self.widget_2.mpl.start_dynamic_plot()

    @pyqtSlot()
    def on_bt_finish_clicked(self):
        self.algThread.working = False
        self.algThread.quit()
        self.algThread.wait()

        self.recvThread.working = False
        self.recvThread.quit()
        self.recvThread.wait()

        self.close()
## #####################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    app.exec_()
