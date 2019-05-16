### 此文件用于提供通用的雷达信号处理算法

import numpy as np
import math

## 降采样
def DownSample(RawData_Martix_I, RawData_Martix_Q):
    FIR_Result_I_Down = RawData_Martix_I[:,::4]
    FIR_Result_Q_Down = RawData_Martix_Q[:,::4]
    RawData_Martix = FIR_Result_I_Down + 1j*FIR_Result_Q_Down
    return RawData_Martix

## 一维FFT
def RangeFFT_Module(RawData_Martix):
    ChirpNum,ChirpLen = RawData_Martix.shape
    RangeFFTResult = np.zeros([ChirpNum,ChirpLen],dtype=np.complex64)

    for i in range(ChirpNum):
        RawData_Martix[i,:] = RawData_Martix[i,:] - np.mean(RawData_Martix[i,:])
        RangeFFTResult[i,:] = np.fft.fft(RawData_Martix[i,:256]*np.hamming(256))
        #RawData_FFTABS[i,:] = abs(RawData_FFT[i,:])
    return RangeFFTResult

## 二维FFT
def DopplerFFT_Module(RangeFFTResult, ChirpNumOfFrame):
    ChirpNum,ChirpLen = RangeFFTResult.shape
    HalfFFTPointNum = ChirpLen//2
    FrameNum = ChirpNum//ChirpNumOfFrame
    RD_Data_Martix = np.zeros([FrameNum, ChirpNumOfFrame, ChirpLen], dtype=np.complex)
    RawData_Clean = RawData_Out[:,:HalfFFTPointNum]

    for RD_Map_index in range(FrameNum):
        RD_Data = RawData_Clean[RD_Map_index*ChirpNumOfFrame : (RD_Map_index+1)*ChirpNumOfFrame,:]
        for index in range(HalfFFTPointNum):
            RD_Data[:,index] = np.fft.fftshift(np.fft.fft(RD_Data[:,index]))
        RD_Data_Martix[RD_Map_index,:,:] = RD_Data

    return RD_Data_Martix

## 去杂波
def ClusterRemove(RawData_Range_FFT,K):
    Chirp_Num,Chirp_Len=RawData_Range_FFT.shape
    W = np.zeros([Chirp_Num,Chirp_Len], dtype=np.complex64)
    RawData_Out = np.zeros([Chirp_Num,Chirp_Len], dtype=np.complex64)
    for ChirpIndex in range(1,Chirp_Num):
        RawData_Out[ChirpIndex,:] = RawData_Range_FFT[ChirpIndex,:] - (1-K)*W[ChirpIndex-1,:]
        W[ChirpIndex,:] = RawData_Out[ChirpIndex,:] + W[ChirpIndex-1,:]
    return RawData_Out

## 平滑
def smooth(a,WSZ):
    # a:原始数据，NumPy 1-D array containing the data to be smoothed
    # 必须是1-D的，如果不是，请使用 np.ravel()或者np.squeeze()转化 
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
    out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ
    r = np.arange(1,WSZ-1,2)
    start = np.cumsum(a[:WSZ-1])[::2]/r
    stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
    return np.concatenate((start,out0,stop))

## 找Chirp头
def FindChirp(ChannelNum, RawData_I_1, RawData_Q_1, RawData_I_2=None, RawData_Q_2=None):
    Threshold = 300
    MAX_DIFFCOUNT = 400

    if ChannelNum != 2 and ChannelNum != 4:
        print('Error!!!channel num must 2 or 4')
        return
    print('==== 1 ====')
    RawData_I_1 = RawData_I_1[19999:]
    RawData_Q_1 = RawData_Q_1[19999:]

    if ChannelNum is 4:
        RawData_I_2 = RawData_I_2[19999:]
        RawData_Q_2 = RawData_Q_2[19999:]

    DataLen = RawData_I_1.size
    CountDiffer = 0
    Delayer_Num = 32
    Differ_Data_1 = np.zeros(RawData_I_1.size, dtype=np.int16)
    print('==== 2 ====')
    for DataIndex in range(Delayer_Num,3000):
        Differ_Data_1[DataIndex] = RawData_I_1[DataIndex] - RawData_I_1[DataIndex - Delayer_Num]
        if abs(Differ_Data_1[DataIndex]) < Threshold:
            CountDiffer = CountDiffer + 1
            if CountDiffer > MAX_DIFFCOUNT:
                Differ_Count = CountDiffer
                Begin_Index  = DataIndex
                ChirpBegin = Begin_Index + 250
                Chirp_End = ChirpBegin + 1024
                break
        else:
            CountDiffer = 0

    adcData_I_1 = RawData_I_1[ChirpBegin:]
    adcData_Q_1 = RawData_Q_1[ChirpBegin:]
    print('==== 3 ====')
    if ChannelNum is 4:
        adcData_I_2 = RawData_I_2[ChirpBegin:]
        adcData_Q_2 = RawData_Q_2[ChirpBegin:]
    DataLen = adcData_I_1.size

    ChirpNum = math.floor(DataLen/2000.32)
    AccData = np.zeros(ChirpNum,dtype=np.int16)
    ChirpPosition = np.zeros(ChirpNum,dtype=np.uint32)
    CountChirp = np.zeros(ChirpNum,dtype = np.uint16)
    print('==== 4 ====')
    # 初始化Chirp数组
    RawData_Martix_I_1 = np.zeros([ChirpNum, 1024])
    RawData_Martix_Q_1 = np.zeros([ChirpNum, 1024])

    if ChannelNum is 4:
        RawData_Martix_I_2 = np.zeros([ChirpNum, 1024])
        RawData_Martix_Q_2 = np.zeros([ChirpNum, 1024])

    # 初始化Chirp位置参数
    AccData[0] = 33
    ChirpPosition[0] = 0
    CountChirp[0] = 1999
    print('==== 5 ====')
    for ChirpIndex in range(1,ChirpNum):
        # 确认当前chirp的点数
        AccData[ChirpIndex] = AccData[ChirpIndex-1] + 33;
        if AccData[ChirpIndex] > 100:
            AccData[ChirpIndex] -= 100
            CountChirp[ChirpIndex] = 2000
        else:
            CountChirp[ChirpIndex] = 1999
        ChirpPosition[ChirpIndex] = ChirpPosition[ChirpIndex-1] + CountChirp[ChirpIndex-1]

        RawData_Martix_I_1[ChirpIndex,:] = adcData_I_1[ChirpPosition[ChirpIndex]:ChirpPosition[ChirpIndex]+1024]
        RawData_Martix_Q_1[ChirpIndex,:] = adcData_Q_1[ChirpPosition[ChirpIndex]:ChirpPosition[ChirpIndex]+1024]

        if ChannelNum is 4:
            RawData_Martix_I_2[ChirpIndex,:] = adcData_I_2[ChirpPosition[ChirpIndex]:ChirpPosition[ChirpIndex]+1024]
            RawData_Martix_Q_2[ChirpIndex,:] = adcData_Q_2[ChirpPosition[ChirpIndex]:ChirpPosition[ChirpIndex]+1024]
    print('==== 6 ====')
    #for i in range(ChirpNum):
    #    plt.plot(np.arange(1024),RawData_Martix_I_1[i],'r')
    #    plt.plot(np.arange(1024),RawData_Martix_Q_1[i],'g')
    #    plt.plot(np.arange(1024),RawData_Martix_I_2[i],'b')
    #    plt.plot(np.arange(1024),RawData_Martix_Q_2[i],'c')
    #    plt.pause(0.01)
    
    return RawData_Martix_I_1,RawData_Martix_Q_1,RawData_Martix_I_2,RawData_Martix_Q_2






