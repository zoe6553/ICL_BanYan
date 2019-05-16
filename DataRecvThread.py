from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from CommArithmetic import *
from queue import Queue

import numpy as np



class DataRecvThread(QThread):
    def __init__(self, parent=None):
        super(DataRecvThread,self).__init__(parent)
        self.working = True

    def SetParam(self,DevSelection,Param, recvQueue):
        self.recvQueue = recvQueue
        if DevSelection == 0:
            ## USB SERIAL
            self.DevSelection = 0
        elif DevSelection == 1:
            ## UART
            self.DevSelection = 1
        elif DevSelection == 2:
            ## Data From File
            self.DevSelection = 2
            file = Param
            print(file)
            adcData = np.fromfile(file,dtype = np.int16)
            self.RawData_I_1 = adcData[::4]
            self.RawData_Q_1 = adcData[1::4]
            self.RawData_I_2 = adcData[2::4]
            self.RawData_Q_2 = adcData[3::4]
            #self.timer = QtCore.QTimer(self)
            #self.timer.timeout.connect(self.find_chirp)
            #self.timer.start(10)  # 触发的时间间隔为10毫秒
            return True
        else:
            self.DevSelection = -1
            return false

    def run(self):
        if self.DevSelection == 0:
            print('ToDo')
        elif self.DevSelection == 1:
            print('ToDo')
        elif self.DevSelection == 2:
            self.runWithFileData()

        else:
            print('ToDo')

    def runWithFileData(self):
        currentFrameIndex = 0
        RawData_I_1_Martix, RawData_Q_1_Martix, RawData_I_2_Martix, RawData_Q_2_Martix = \
                FindChirp(4, self.RawData_I_1, self.RawData_Q_1, self.RawData_I_2, self.RawData_Q_2)
        ChirpNum,ChirpLen = RawData_I_1_Martix.shape
        FrameNum = ChirpNum//32 - 1

        #self.RawData_I_1_Martix = RawData_I_1_Martix[:FrameNum*32*ChirpLen]
        #self.RawData_Q_1_Martix = RawData_Q_1_Martix[:FrameNum*32*ChirpLen]
        #self.RawData_I_2_Martix = RawData_I_2_Martix[:FrameNum*32*ChirpLen]
        #self.RawData_Q_2_Martix = RawData_Q_2_Martix[:FrameNum*32*ChirpLen]

        RawData_I_1_Martix = RawData_I_1_Martix[:FrameNum*32].reshape(FrameNum,32,ChirpLen)
        RawData_Q_1_Martix = RawData_Q_1_Martix[:FrameNum*32].reshape(FrameNum,32,ChirpLen)
        RawData_I_2_Martix = RawData_I_2_Martix[:FrameNum*32].reshape(FrameNum,32,ChirpLen)
        RawData_Q_2_Martix = RawData_Q_2_Martix[:FrameNum*32].reshape(FrameNum,32,ChirpLen)
        RawDataFrame = np.zeros([4,32,ChirpLen])
        while (self.working and currentFrameIndex < FrameNum):
            RawDataFrame[0] = RawData_I_1_Martix[currentFrameIndex]
            RawDataFrame[1] = RawData_Q_1_Martix[currentFrameIndex]
            RawDataFrame[2] = RawData_I_2_Martix[currentFrameIndex]
            RawDataFrame[3] = RawData_Q_2_Martix[currentFrameIndex]
            currentFrameIndex += 1
            self.recvQueue.put(RawDataFrame)
            self.msleep(50) #50毫秒发一帧
        end_frame = np.zeros([1,2,3])
        self.recvQueue.put(end_frame) ##发送结束帧0，1，2，3
        print('Recv Finish!')

