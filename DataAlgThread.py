from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from CommArithmetic import *
from GestureArithmetic import *
from queue import Queue
from PreDefine import enum
from PreDefine import RadarParam

import matplotlib.pyplot as plt
import numpy as np


# 雷达参数定义
C               = 3e8                           # 光速：3*10^8m/s
Start_Freq      = 23.5e9                        # 起始频率：23.5GHz
End_Freq        = 27.5e9                        # 截至频率：27.5GHz
Center_Freq     = (Start_Freq+End_Freq)/2       # 中心频率
Lamda           = C/Center_Freq                 # 波长
Saw_Period      = 640e-6                        # 锯齿波时间
CW_Period       = 360e-6                        # 点频连续波时间
Chirp_Period    = Saw_Period + CW_Period        # Chirp周期
AD_Sampling     = 2e6                           # AD采样率
DownSample_Rate = 4                             # 降采样率
dt              = DownSample_Rate/AD_Sampling   # 时间分辨率

FFT_Num         = 256                           # fft 点数
BandWidth       = 3.072e9                       # 带宽
RangeRes        = C/(2*BandWidth)               # 距离分辨率
df              = 1/(FFT_Num * dt)              # 频率分辨率
Range_Axis      = (np.arange(FFT_Num) - (FFT_Num//2)) * RangeRes

FFT_Num_RD      = 32                            # 多普勒FFT点数
Velocity_Res    = Lamda/(2*FFT_Num_RD*Chirp_Period) #速度分辨率
Velocity_Axis   = (np.arange(FFT_Num_RD) - (FFT_Num_RD//2)) * Velocity_Res


class DataAlgThread(QThread):
    def __init__(self, parent=None):
        super(DataAlgThread,self).__init__(parent)
        self.working = True
        self.index = 0

    def SetParam(self, DevSelection,recvQueue, sendQueue, resultQueue,shareFFTBuf):
        self.DevSelection = DevSelection
        self.recvQueue = recvQueue
        self.sendQueue = sendQueue
        self.shareFFTBuf = shareFFTBuf
        self.resultQueue = resultQueue

    def run(self):
        while self.working is True:
            RawDataMartix = self.recvQueue.get()
            
            self.index += 1
            if self.DevSelection == enum.USB_SERIAL:                
                #ChannelNum,ChirpNum = RawDataMartix.shape                
                self.sendQueue.put(RawDataMartix[0][0:1999])
                self.resultQueue.put(RawDataMartix[1][0:1999])

            if self.DevSelection == enum.UART_SERIAL:
                self.sendQueue.put(RawDataMartix)
                RawDataMartix = RawDataMartix - np.mean(RawDataMartix)
                RawData_Range_FFT = np.fft.fft(RawDataMartix*np.hamming(256))
                RawData_Range_FFT_ABS = abs(RawData_Range_FFT)
                self.resultQueue.put(RawData_Range_FFT_ABS[2:32])
            elif self.DevSelection == enum.FILE_SOURCE:
                channelnum, chirpnum, chirplen = RawDataMartix.shape
                if (channelnum == 1) and (chirpnum == 2) and (chirplen == 3):
                    print('send end frame')
                    self.sendQueue.queue.clear()
                    self.sendQueue.put(np.arange(4))
                    self.resultQueue.queue.clear()
                    self.resultQueue.put(np.arange(4))
                    self.working = False
                else:
                    I_1_Martix = RawDataMartix[0]
                    Q_1_Martix = RawDataMartix[1]
                    I_2_Martix = RawDataMartix[2]
                    Q_2_Martix = RawDataMartix[3]

                    ## 降采样
                    RawData_Martix_1 = DownSample(I_1_Martix, Q_1_Martix)
                    RawData_Martix_2 = DownSample(I_2_Martix, Q_2_Martix)

                    ## RangeFFT
                    RawData_Range_FFT_1 = RangeFFT_Module(RawData_Martix_1)
                    RawData_Range_FFT_2 = RangeFFT_Module(RawData_Martix_2)

                    self.shareFFTBuf = RawData_Range_FFT_1.copy()
                    self.sendQueue.put(RawData_Martix_1[0])
                    self.resultQueue.put(abs(RawData_Range_FFT_1[0,2:32]))
                    continue

                    ## Cluster remove
                    K=0.8
                    RawData_Out_1 = ClusterRemove(RawData_Range_FFT_1, K)
                    RawData_Out_2 = ClusterRemove(RawData_Range_FFT_2, K)

                    ## Feature in range domain
                    RangePos, PhaseValue = Feature_in_RangeDomain(RawData_Out_1 , RawData_Out_2 , Lamda )


