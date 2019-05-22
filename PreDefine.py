import numpy as np

class enum():
    ######## DEV SELECTION ########
    USB_SERIAL = 0
    FILE_SOURCE = 1
    UART_SERIAL = 2
    ######## PATTERN SELECTION ########
    RANGE_ANGLE_MODE = 0
    AREA_DETECT_MODE = 1
    GESTURE_DETECT_MODE = 2
    ######## CHANNEL NUM SELECTION ########
    #ONE_CHANNEL = 0
    TWO_CHANNEL = 0
    FOUR_CHANNEL = 1

class RadarParam():
    UART_HEAD_LENGTH = 4
    UART_CHECKSUM_LENGTH = 2
    UART_DATA_LENGTH = 512
    UART_PACKET_LENGTH = UART_DATA_LENGTH + UART_CHECKSUM_LENGTH + UART_HEAD_LENGTH ##518 BYTE
    UART_HEAD = np.asarray([0xff,0xff,0x00,0x00])
    

