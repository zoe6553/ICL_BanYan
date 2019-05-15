import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from RadarWindow import *
from PyQt5.QtCore import pyqtSlot

import numpy as np

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setWindowTitle('BanYan Demo')
        
        self.setupUi(self)
        self.widget.setVisible(False)
        self.widget_2.setVisible(False)
        self.Ui_Init()

    def Ui_Init(self):
        ## 设备选择下拉框:USB,UART,文件打开
        self.DevSelectBox.addItem('USB Serial')
        self.DevSelectBox.addItem('COM5')
        self.DevSelectBox.addItem('From File')
        self.DevSelectBox.setCurrentIndex(0)
        self.devselect = 0
        self.DevSelectBox.currentIndexChanged.connect(self.selectionchange)

    def selectionchange(self,index):
        self.devselect = index
        if index is 0:
            self.bt_connect.setText('连接')
        elif index is 1:
            self.bt_connect.setText('连接')
        elif index is 2:
            self.bt_connect.setText('目录')

    ## 连接/目录 按钮 slot
    @pyqtSlot()
    def on_bt_connect_clicked(self):
        if self.devselect is 0:
            print('ToDo')
        elif self.devselect is 1:
            print('ToDo')
        elif self.devselect is 2:
            file,ok = QFileDialog.getOpenFileName(self, "打开文件", "./", "Data Files (*.dat);;Text Files (*.txt)")
            self.data = np.fromfile(file,dtype = np.int16)

    @pyqtSlot()
    def on_bt_start_clicked(self):
        """
        Slot documentation goes here.
        """
        print('start')
        self.widget.setVisible(True)
        self.widget.mpl.start_static_plot()
        self.widget_2.setVisible(True)
        self.widget_2.mpl.start_dynamic_plot()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    app.exec_()
