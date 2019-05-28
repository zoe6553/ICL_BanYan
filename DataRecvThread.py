from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from CommArithmetic import *
from queue import Queue
from PreDefine import enum
from PreDefine import RadarParam
import matplotlib.pyplot as plt

import numpy as np



class DataRecvThread(QThread):
    def __init__(self, parent=None):
        super(DataRecvThread,self).__init__(parent)
        self.working = True

    def SetParam(self,DevSelection,Param, recvQueue):
        self.recvQueue = recvQueue
        if DevSelection == enum.USB_SERIAL:
            ## USB SERIAL
            self.DevSelection = enum.USB_SERIAL
            self.usb = Param
        elif DevSelection == enum.FILE_SOURCE:
            ## Data From File
            self.DevSelection = enum.FILE_SOURCE
            file = Param
            print(file)
            adcData = np.fromfile(file,dtype = np.int16)
            self.RawData_I_1 = adcData[::4]
            self.RawData_Q_1 = adcData[1::4]
            self.RawData_I_2 = adcData[2::4]
            self.RawData_Q_2 = adcData[3::4]
            return True
        elif DevSelection == enum.UART_SERIAL:
            ## UART
            self.DevSelection = enum.UART_SERIAL
            self.uart = Param
            self.CollectingData = np.zeros(RadarParam.UART_PACKET_LENGTH*3, dtype=np.uint8) ##收集中的package
            self.CollectedData = np.zeros(RadarParam.UART_DATA_LENGTH, dtype=np.uint8)  ##收集完成并校验通过的package
        else:
            self.DevSelection = -1
            return false

    def run(self):
        if self.DevSelection == enum.USB_SERIAL:
            self.RunWithUSB()
        elif self.DevSelection == enum.FILE_SOURCE:
            self.RunWithFileData()
        elif self.DevSelection == enum.UART_SERIAL:
            self.RunWithUart()
        else:
            print('ToDo')

    def RunWithFileData(self):
        currentFrameIndex = 0
        RawData_I_1_Martix, RawData_Q_1_Martix, RawData_I_2_Martix, RawData_Q_2_Martix = \
                FindChirp(4, self.RawData_I_1, self.RawData_Q_1, self.RawData_I_2, self.RawData_Q_2)
        ChirpNum,ChirpLen = RawData_I_1_Martix.shape
        FrameNum = ChirpNum//32 - 1

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

    def RunWithUart(self):
        # 已经组包的数据量
        self.uartDataIndex = 0
        UartSamplePacket = np.zeros(RadarParam.UART_DATA_LENGTH//2,dtype=np.int16)
        if self.uart.is_open:
            self.uart.close()
        self.uart.open()
        if self.uart.is_open:
            print('open success')
        while (self.working):
            RawDataBytes = self.uart.read(RadarParam.UART_PACKET_LENGTH)
            RawData = np.frombuffer(RawDataBytes,dtype=np.uint8)

            UartPacket = self.CollectPack(RawData)
            if UartPacket is None:
                continue
            else:
                for i in range(RadarParam.UART_DATA_LENGTH//2):
                    UartSamplePacket[i] = (UartPacket[2*i] << 8) + UartPacket[2*i+1]
                self.recvQueue.put(UartSamplePacket)

    def CollectPack(self,RawData):
        HeadCount = 0    
        if self.uartDataIndex == 0:
            #第一包
            self.CollectingData[:RadarParam.UART_PACKET_LENGTH] = RawData
            self.uartDataIndex = RadarParam.UART_PACKET_LENGTH
            return None
        else:
            #非第一包
            self.CollectingData[self.uartDataIndex:RadarParam.UART_PACKET_LENGTH + self.uartDataIndex] = RawData
            self.uartDataIndex += RadarParam.UART_PACKET_LENGTH
            # 寻找数据中包头的位置
            UartHeadIndex = np.asarray([-1,-1,-1])
            for index in range(RadarParam.UART_PACKET_LENGTH*2 - 4):
                if ((self.CollectingData[index:index+RadarParam.UART_HEAD_LENGTH] == RadarParam.UART_HEAD).all()):
                    UartHeadIndex[HeadCount] = index
                    HeadCount += 1

            if (UartHeadIndex[1] - UartHeadIndex[0] == RadarParam.UART_PACKET_LENGTH):
                self.CollectedData = self.CollectingData[UartHeadIndex[0]+4:UartHeadIndex[1]-2].copy()
                self.CollectingData[:UartHeadIndex[1]] = 0 #np.zeros(UartHeadIndex[1])
            elif (HeadCount == 3) and (UartHeadIndex[2] - UartHeadIndex[1] == RadarParam.UART_PACKET_LENGTH):
                print('skip one error buffer')
                self.CollectedData = self.CollectingData[UartHeadIndex[1]+4:UartHeadIndex[2]-2].copy()
                self.CollectingData[:UartHeadIndex[2]] = 0# np.zeros(UartHeadIndex[2])

            self.CollectingData[:self.uartDataIndex-UartHeadIndex[HeadCount-1]] = self.CollectingData[UartHeadIndex[HeadCount-1]:self.uartDataIndex]
            self.CollectingData[self.uartDataIndex-UartHeadIndex[HeadCount-1]:] = 0
            self.uartDataIndex = self.uartDataIndex-UartHeadIndex[HeadCount-1]

            return self.CollectedData

    def RunWithUSB(self):
        self.usb.StartRadar()
        while(self.working):
            RawData = self.usb.ReadRawData()
            RawDataLen = RawData.size
            RawDataChannel = np.zeros((4,RawDataLen//4), dtype=np.int16)
            for i in range(4):
                RawDataChannel[0] = RawData[::4]
                RawDataChannel[1] = RawData[1::4]
                RawDataChannel[2] = RawData[2::4]
                RawDataChannel[3] = RawData[3::4]

            plt.plot(RawDataChannel[0],'r')
            plt.plot(RawDataChannel[1],'g')
            plt.plot(RawDataChannel[2],'b')
            plt.plot(RawDataChannel[3],'r')
            plt.show()

            #print('recv queue: %d' % self.recvQueue.qsize())
            self.recvQueue.put(RawDataChannel)


