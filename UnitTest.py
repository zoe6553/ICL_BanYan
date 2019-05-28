import numpy as np

RegisterTable = np.loadtxt('chuanpin.txt',dtype=str)
RegisterTableLen = RegisterTable.size

Register = np.zeros(RegisterTableLen,dtype=np.uint32)
RegisterValue = np.zeros(RegisterTableLen,dtype=np.uint32)

for index in range(RegisterTableLen):
    Register[index] = int(RegisterTable[index][0:2],16)
    RegisterValue[index] = int(RegisterTable[index][3:],16)


print(Register,RegisterValue)
print(RegisterTable)
