import ICL_USB
import numpy as np

class UsbSerial():
    def __init__(self, parent=None):
        self.usb = ICL_USB.ICL_USB()

    def StartRadar(self):
        self.usb.WriteRegister(3, 0)
        self.usb.WriteRegister(2, 1)
        self.usb.StartTransfer()

    def StopRadar(self):
        self.usb.WriteRegister(2, 0)
        self.usb.FinishTransfer()

    def ReadRawData(self):
        return self.usb.ReadRawData()

    def WrtieRadarRegister(self, address, value):
        radaraddr = (address+128).astype(np.uint16)
        self.usb.WriteRegister(radaraddr, value)

    def ReadRadarRegister(self, address):
        radaraddr = (address + 0xC0).astype(np.uint16)
        print(type(radaraddr))
        return self.usb.ReadRegister(radaraddr)

    def Is_Radar_Connect(self):
        return self.usb.Is_Radar_Connect()