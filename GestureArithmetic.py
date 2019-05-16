import numpy as np

def Feature_in_RangeDomain(RawData_Out_1 , RawData_Out_2 , Lamda, Antenna_Gap):
    RawData_Out_2conj = np.conj(RawData_Out_2)
    RawData_Out = RawData_Out_1*RawData_Out_2conj
    Martix_New = RawData_Out[30:,0:15]
    Phase_Martix = np.angle(RawData_Out[30:,0:15])

    SlowTime_Len, FastTime_Len = Martix_New.shape
    RangePos = np.zeros(SlowTime_Len,dtype=np.uint8)
    PhaseValue = np.zeros(SlowTime_Len,dtype=np.float)

    for SlowTime_index in range(SlowTime_Len):
        RangePos[SlowTime_index] = np.argmax(abs(Martix_New[SlowTime_index,:]))
        PhaseValue[SlowTime_index] = Phase_Martix[SlowTime_index,RangePos[SlowTime_index]]
        if PhaseValue[SlowTime_index] <= 0:
            PhaseValue[SlowTime_index] += np.pi
        else:
            PhaseValue[SlowTime_index] -= np.pi
        PhaseValue[SlowTime_index] = Lamda * PhaseValue[SlowTime_index]/(2*np.pi*Antenna_Gap)

    return RangePos,PhaseValue

def Feature_Extract_in_RD(RD_Data_Martix_1 , RD_Data_Martix_2 , Velocity_Axis , Range_Axis , Lamda, Antenna_Gap):
    RD_Map_Num, SlowTimeLen, FastTimeLen = RD_Data_Martix_1.shape
    FastTime_Len = 128
    Range_Axis_New = Range_Axis[128:128+FastTime_Len]

    AmpValue = np.zeros(RD_Map_Num,dtype=np.uint8)
    Scatters_Num = np.zeros(RD_Map_Num,dtype=np.uint8)
    Velocity_Pos_1 = np.zeros(RD_Map_Num,dtype=np.uint8)
    Range_Pos_1 = np.zeros(RD_Map_Num,dtype=np.uint8)

    Euclidean_Range = np.zeros(RD_Map_Num,dtype=np.float)
    AngleValue = np.zeros(RD_Map_Num,dtype=np.float)
    Velocity_Value = np.zeros(RD_Map_Num,dtype=np.float)

    for RD_Map_index in range(RD_Map_Num):
        RD_Data_1 = np.squeeze(RD_Data_Martix_1[RD_Map_index,:,:32])
        RD_Data_2 = np.squeeze(RD_Data_Martix_2[RD_Map_index,:,:32])
        Amp_RD_1 = abs(RD_Data_1)
        Amp_RD_2 = abs(RD_Data_2)

        Amp_RD_1[Amp_RD_1<1.5e4] = 0
        Amp_RD_2[Amp_RD_2<1.5e4] = 0
        AmpValue[RD_Map_index] = np.sum(Amp_RD_2)

        Amp_RD_1[Amp_RD_1>0] = 1
        Amp_RD_2[Amp_RD_2>0] = 1
        Scatters_Num[RD_Map_index] = np.sum(Amp_RD_1)

        RD_Data_1 = RD_Data_1*Amp_RD_1
        RD_Data_2 = RD_Data_2*Amp_RD_2

        RD_Data = RD_Data_1*np.conj(RD_Data_2)
        
        Ang_Martix = np.angle(RD_Data)

        Value_Max_Amp = np.max(abs(RD_Data_1))
        Velocity_Pos, Range_Pos = np.where(abs(RD_Data_1) == Value_Max_Amp)
        Velocity_Pos_1[RD_Map_index] = Velocity_Pos[0]
        Range_Pos_1[RD_Map_index] = Range_Pos[0]

        AngleValue[RD_Map_index] = Ang_Martix[Velocity_Pos_1[RD_Map_index], Range_Pos_1[RD_Map_index]]
        if AngleValue[RD_Map_index] <= 0:
            AngleValue[RD_Map_index] = AngleValue[RD_Map_index] + np.pi
        else:
            AngleValue[RD_Map_index] = AngleValue[RD_Map_index] - np.pi

        AngleValue[RD_Map_index] =  Lamda * AngleValue[RD_Map_index]/(2*np.pi*Antenna_Gap)
        Euclidean_Range[RD_Map_index] = Range_Axis_New[Range_Pos_1[RD_Map_index]]
        Velocity_Value[RD_Map_index] = Velocity_Axis[Velocity_Pos_1[RD_Map_index]]

    return Scatters_Num  , AngleValue , Euclidean_Range , Velocity_Value

def Move_Statement_Result(Velocity_center , Scatter_Points ,Angle_Value ,Range_center,WinLen):
    DataLen = Scatter_Points.size
    slid_Scatter        = np.zeros(WinLen,dtype=np.float)
    sliding_Angle       = np.zeros(WinLen,dtype=np.float)
    sliding_Velocity    = np.zeros(WinLen,dtype=np.float)
    sliding_Range       = np.zeros(WinLen,dtype=np.float)

    Scatter_Mean        = np.zeros(DataLen,dtype=np.float)
    Range_Var           = np.zeros(DataLen,dtype=np.float)
    Velocity_Mean       = np.zeros(DataLen,dtype=np.float)
    Velocity_Var        = np.zeros(DataLen,dtype=np.float)
    Slope_Angle         = np.zeros(DataLen,dtype=np.float)
    Angle_Var           = np.zeros(DataLen,dtype=np.float)
    MoveCode            = np.zeros(DataLen,dtype=np.int8)

    CountScatter = 0
    CountLeft    = 0
    CountRight   =0

    for Data_index in range(DataLen):
        slid_Scatter[:WinLen-1] = slid_Scatter[1:WinLen]
        slid_Scatter[WinLen-1] = Scatter_Points[Data_index]

        sliding_Angle[:WinLen-1] = sliding_Angle[1:WinLen]
        sliding_Angle[WinLen-1] = Angle_Value[Data_index]

        sliding_Velocity[:WinLen-1] = sliding_Velocity[1:WinLen]
        sliding_Velocity[WinLen-1] = Velocity_center[Data_index]

        sliding_Range[:WinLen-1] = sliding_Range[1:WinLen]
        sliding_Range[WinLen-1] = Range_center[Data_index]

        ##
        Scatter_Mean[Data_index] = np.mean(slid_Scatter)
        Range_Var[Data_index]    = np.std(sliding_Range)

        Velocity_Mean[Data_index]= np.mean(sliding_Velocity)
        Velocity_Var[Data_index] = np.std(sliding_Velocity)

        Slope_Angle[Data_index]  = sliding_Angle[WinLen-1] - sliding_Angle[0]
        Angle_Var[Data_index]    = np.std(sliding_Angle)

        ##
        if Scatter_Mean[Data_index] > 100 and abs(Slope_Angle[Data_index]) < 0.15 \
            and Velocity_Mean[Data_index] < -0.15:
            print('Hand Back')
            MoveCode[Data_index] = 1
        elif Scatter_Mean[Data_index] > 100 and abs(Slope_Angle[Data_index]) < 0.15 \
            and Velocity_Mean[Data_index] > 0.15:
            print('Hand Front')
            MoveCode[Data_index] = -1
        elif Scatter_Mean[Data_index] > 30 and Scatter_Mean[Data_index] < 80 \
            and Slope_Angle[Data_index] > 0.35:
            print('Hand Left')
            MoveCode[Data_index] = 2
        elif Scatter_Mean[Data_index] > 30 and Scatter_Mean[Data_index] < 80 \
            and Slope_Angle[Data_index] < -0.35:
            print('Hand Right')
            MoveCode[Data_index] = -2
        else:
            MoveCode[Data_index] = 0
    return MoveCode