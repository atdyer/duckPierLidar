import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Wedge
from math import radians, sin, cos, tan

class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        self.setWindowTitle('Lidar Boom Geometry')
        self.initializeValues()
        self.createLayout()
        self.initializeDrawing()
    
    def initializeValues(self):
        
        self.crestVal = [0.0, 6.5]
        self.backAngleVal = 2
        self.backHeightVal = 4
        self.frontAngleVal = 3
        self.frontHeightVal = 1
        self.frontDropVal = 1
        self.baseDropVal = 1
        self.baseOffsetVal = 12
        self.baseHeightVal = 4 * 0.3048
        self.boomAngleVal = 20
        self.boomLengthVal = 40 * 0.3048
        self.mountAngleVal = 63
        self.mountLengthVal = 0.5
        self.waterLevelVal = 1
        
    def initializeDrawing(self):
        
        self.waterLine, = self.ax.plot([0.0, 300.0], [self.waterLevelVal, self.waterLevelVal])
        
        crestDrop = [self.crestVal[0], self.crestVal[1]-self.frontDropVal]
        waterPt = [(crestDrop[1]-self.frontHeightVal)/tan(radians(self.frontAngleVal)), self.frontHeightVal]
        landPt = [-(self.crestVal[1]-self.backHeightVal)/tan(radians(self.backAngleVal)), self.backHeightVal]
        
        x = [i[0] for i in [landPt, self.crestVal, crestDrop, waterPt]]
        y = [i[1] for i in [landPt, self.crestVal, crestDrop, waterPt]]
        
        self.duneLine, = self.ax.plot(x, y)
        
        baseGround = [self.crestVal[0] - self.baseOffsetVal, self.crestVal[1] - self.baseDropVal]
        baseTop = [baseGround[0], baseGround[1] + self.baseHeightVal]
        boomEnd = [baseTop[0] + self.boomLengthVal*cos(radians(self.boomAngleVal)), baseTop[1] + self.boomLengthVal*sin(radians(self.boomAngleVal))]
        mountEnd = [boomEnd[0] - self.mountLengthVal*cos(radians(self.mountAngleVal)), boomEnd[1] + self.mountLengthVal*sin(radians(self.mountAngleVal))]
        
        xb = [i[0] for i in [baseGround, baseTop, boomEnd, mountEnd]]
        yb = [i[1] for i in [baseGround, baseTop, boomEnd, mountEnd]]
        
        self.boomLine, = self.ax.plot(xb, yb)
        self.wedge = Wedge(boomEnd, 300, -self.mountAngleVal-40, -self.mountAngleVal+60, alpha=0.5, color='y')
        self.ax.add_artist(self.wedge)
        
        self.fig.subplots_adjust(left=0.1)
        
    def getDuneValues(self):
        
        crestDrop = [self.crestVal[0], self.crestVal[1]-self.frontDropVal]
        waterPt = [(crestDrop[1]-self.frontHeightVal)/tan(radians(self.frontAngleVal)), self.frontHeightVal]
        landPt = [-(self.crestVal[1]-self.backHeightVal)/tan(radians(self.backAngleVal)), self.backHeightVal]
        
        x = [i[0] for i in [landPt, self.crestVal, crestDrop, waterPt]]
        y = [i[1] for i in [landPt, self.crestVal, crestDrop, waterPt]]
        
        return x, y
        
    def getBoomValues(self):
        
        baseGround = [self.crestVal[0] - self.baseOffsetVal, self.crestVal[1] - self.baseDropVal]
        baseTop = [baseGround[0], baseGround[1] + self.baseHeightVal]
        boomEnd = [baseTop[0] + self.boomLengthVal*cos(radians(self.boomAngleVal)), baseTop[1] + self.boomLengthVal*sin(radians(self.boomAngleVal))]
        mountEnd = [boomEnd[0] - self.mountLengthVal*cos(radians(self.mountAngleVal)), boomEnd[1] + self.mountLengthVal*sin(radians(self.mountAngleVal))]
        
        x = [i[0] for i in [baseGround, baseTop, boomEnd, mountEnd]]
        y = [i[1] for i in [baseGround, baseTop, boomEnd, mountEnd]]
        
        self.wedge.set_center(boomEnd)
        self.wedge.set_theta1(-self.mountAngleVal-40)
        self.wedge.set_theta2(-self.mountAngleVal+60)
        
        return x, y
        
    def updateCrest(self, val):
        
        self.crestVal[1] = val
        x, y = self.getDuneValues()
        self.duneLine.set_xdata(x)
        self.duneLine.set_ydata(y)
        self.fig.canvas.draw()
        
    def updateWaterLevel(self, val):
        
        self.waterLevelVal = val
        self.waterLine.set_ydata([self.waterLevelVal, self.waterLevelVal])
        self.fig.canvas.draw()
        
    def updateBaseDrop(self, val):
        
        self.baseDropVal = val
        x, y = self.getBoomValues()
        self.boomLine.set_xdata(x)
        self.boomLine.set_ydata(y)
        self.fig.canvas.draw()
        
    def updateBaseOffset(self, val):
        
        self.baseOffsetVal = val
        x, y = self.getBoomValues()
        self.boomLine.set_xdata(x)
        self.boomLine.set_ydata(y)
        self.fig.canvas.draw()
        
    def updateBaseHeight(self, val):
        
        self.baseHeightVal = val
        x, y = self.getBoomValues()
        self.boomLine.set_xdata(x)
        self.boomLine.set_ydata(y)
        self.fig.canvas.draw()
        
    def updateBoomAngle(self, val):
        
        self.boomAngleVal = val
        x, y = self.getBoomValues()
        self.boomLine.set_xdata(x)
        self.boomLine.set_ydata(y)
        self.fig.canvas.draw()
        
    def updateBoomLength(self, val):
        
        self.boomLengthVal = val
        x, y = self.getBoomValues()
        self.boomLine.set_xdata(x)
        self.boomLine.set_ydata(y)
        self.fig.canvas.draw()
        
    def updateMountAngle(self, val):
        
        self.mountAngleVal = val
        x, y = self.getBoomValues()
        self.boomLine.set_xdata(x)
        self.boomLine.set_ydata(y)
        self.fig.canvas.draw()
    
    def createLayout(self):
        self.mainFrame = QWidget()
        
        # Main horizontal layout
        mainLayout = QHBoxLayout()
        
        # Two vertical layouts
        controlLayout = QGridLayout()
        viewLayout = QVBoxLayout()
        mainLayout.addLayout(controlLayout)
        mainLayout.addLayout(viewLayout)
        
        # Control grid
        controlLayout.addWidget(QLabel('Dune Crest'), 0, 0)
        controlLayout.addWidget(QLabel('Water Level'), 1, 0)
        controlLayout.addWidget(QLabel('Base Drop'), 2, 0)
        controlLayout.addWidget(QLabel('Base Offset'), 3, 0)
        controlLayout.addWidget(QLabel('Base Height'), 4, 0)
        controlLayout.addWidget(QLabel('Boom Angle'), 5, 0)
        controlLayout.addWidget(QLabel('Boom Length'), 6, 0)
        controlLayout.addWidget(QLabel('Mount Angle'), 7, 0)
        #controlLayout.setRowStretch(7, 0)
        
        self.crestHeight = QDoubleSpinBox(self.mainFrame)
        self.crestHeight.setSingleStep(0.1)
        self.crestHeight.setValue(self.crestVal[1])
        controlLayout.addWidget(self.crestHeight, 0, 1)
        self.connect(self.crestHeight, SIGNAL('valueChanged(double)'), self.updateCrest)
        
        self.waterLevel = QDoubleSpinBox(self.mainFrame)
        self.waterLevel.setSingleStep(0.1)
        self.waterLevel.setValue(self.waterLevelVal)
        controlLayout.addWidget(self.waterLevel, 1, 1)
        self.connect(self.waterLevel, SIGNAL('valueChanged(double)'), self.updateWaterLevel)
        
        self.baseDrop = QDoubleSpinBox(self.mainFrame)
        self.baseDrop.setSingleStep(0.1)
        self.baseDrop.setValue(self.baseDropVal)
        controlLayout.addWidget(self.baseDrop, 2, 1)
        self.connect(self.baseDrop, SIGNAL('valueChanged(double)'), self.updateBaseDrop)
        
        self.baseOffset = QDoubleSpinBox(self.mainFrame)
        self.baseOffset.setSingleStep(0.1)
        self.baseOffset.setValue(self.baseOffsetVal)
        controlLayout.addWidget(self.baseOffset, 3, 1)
        self.connect(self.baseOffset, SIGNAL('valueChanged(double)'), self.updateBaseOffset)
        
        self.baseHeight = QDoubleSpinBox(self.mainFrame)
        self.baseHeight.setSingleStep(0.1)
        self.baseHeight.setValue(self.baseHeightVal)
        controlLayout.addWidget(self.baseHeight, 4, 1)
        self.connect(self.baseHeight, SIGNAL('valueChanged(double)'), self.updateBaseHeight)
        
        self.boomAngle = QDoubleSpinBox(self.mainFrame)
        self.boomAngle.setSingleStep(0.5)
        self.boomAngle.setMaximum(360)
        self.boomAngle.setValue(self.boomAngleVal)
        controlLayout.addWidget(self.boomAngle, 5, 1)
        self.connect(self.boomAngle, SIGNAL('valueChanged(double)'), self.updateBoomAngle)
        
        self.boomLength = QDoubleSpinBox(self.mainFrame)
        self.boomLength.setSingleStep(0.1)
        self.boomLength.setValue(self.boomLengthVal)
        controlLayout.addWidget(self.boomLength, 6, 1)
        self.connect(self.boomLength, SIGNAL('valueChanged(double)'), self.updateBoomLength)
        
        self.mountAngle = QDoubleSpinBox(self.mainFrame)
        self.mountAngle.setSingleStep(0.5)
        self.mountAngle.setMaximum(360)
        self.mountAngle.setValue(self.mountAngleVal)
        controlLayout.addWidget(self.mountAngle, 7, 1)
        self.connect(self.mountAngle, SIGNAL('valueChanged(double)'), self.updateMountAngle)
        
        # Create the axes
        self.fig = Figure((5.0, 4.0))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mainFrame)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.ax.set_ylim([-20,300])
        self.toolBar = NavigationToolbar(self.canvas, self.mainFrame)
        viewLayout.addWidget(self.canvas)
        viewLayout.addWidget(self.toolBar)
        
        # Set the main layout
        self.mainFrame.setLayout(mainLayout)
        self.setCentralWidget(self.mainFrame)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()

if __name__ == "__main__":
    main()