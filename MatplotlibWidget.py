import numpy as np
import random
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        #self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    '''绘制静态图，可以在这里定义自己的绘图逻辑'''

    def start_static_plot(self):
        print("start_static_plot")
        self.fig.suptitle('测试静态图')
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)
        self.axes.set_ylabel('静态图：Y轴')
        self.axes.set_xlabel('静态图：X轴')
        self.axes.grid(True)

    '''启动绘制动态图'''

    def start_dynamic_plot(self, *args, **kwargs):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)  # 每隔一段时间就会触发一次update_figure函数。
        timer.start(1000)  # 触发的时间间隔为1秒。

    '''动态图的绘图逻辑可以在这里修改'''

    def update_figure(self):
        self.fig.suptitle('测试动态图')
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.axes.set_ylabel('动态图：Y轴')
        self.axes.set_xlabel('动态图：X轴')
        self.axes.grid(True)
        self.draw()

    def plotFileData(self, ChannelNum, RawData_Martix_I_1, RawData_Martix_Q_1=None, RawData_Martix_I_2=None, RawData_Martix_Q_2=None):
        self.ChannelNum = ChannelNum
        self.RawData_Martix_I_1 = RawData_Martix_I_1
        self.RawData_Martix_Q_1 = RawData_Martix_Q_1
        self.RawData_Martix_I_2 = RawData_Martix_I_2
        self.RawData_Martix_Q_2 = RawData_Martix_Q_2
        self.ChirpNum, self.ChirpLen = RawData_Martix_I_1.shape
        self.curPlotChirp = 0

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_FileData_Figure)
        timer.start(1)

    def plotData(self, sendqueue):
        self.sendQueue = sendqueue
        self.curPlotChirp = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_FileData_Figure)
        self.timer.start(100)

    def update_FileData_Figure(self):
        result = self.sendQueue.get()
        if result.size == 4:
            print('will stop')
            self.timer.stop()
        else:
            self.sendQueue.queue.clear()
            self.fig.suptitle('Chirp图形: ')
            result_abs = abs(result[1])
            #print(self.curPlotChirp)
            self.axes.cla()
            self.axes.plot(result_abs[2:])
            self.curPlotChirp += 1
            self.axes.set_ylabel('Y轴')
            self.axes.set_xlabel('X轴')
            self.axes.grid(True)
            self.draw()



class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        # self.mpl.start_static_plot() # 如果你想要初始化的时候就呈现静态图，请把这行注释去掉
        #self.mpl.start_dynamic_plot() # 如果你想要初始化的时候就呈现动态图，请把这行注释去掉
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
