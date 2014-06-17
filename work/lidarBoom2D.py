import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Wedge, Polygon
from math import radians, degrees, sin, cos, tan, sqrt, atan2, atan

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
        self.boomLengthVal = 44 * 0.3048
        self.mountAngleVal = 80
        self.hingeAngleVal = 10
        self.mountLengthVal = 0.5
        self.waterLevelVal = 1
        
        # Cabling variables
        self.cableMountHeight = 5 * 0.3048
        self.pulleyALocation = 34 * 0.3048
        
        # Weights
        self.sensorWeight = 500
        
    def drawBoomEnd(self):
        
        # The boom cut
        length = 15
        height = 10
        boomPts = [[0, 0], [length, 0], [length + height/tan(radians(self.mountAngleVal)), height], [0, height]]
        
        x = [i[0] for i in boomPts]
        y = [i[1] for i in boomPts]
        
        self.barAx.cla()
        self.barAx.plot(x, y, 'k')
        fill = Polygon(boomPts, facecolor='k')
        self.barAx.add_patch(fill)

        # The angled hinge
        hingeLength = sqrt((height/tan(radians(self.mountAngleVal)))**2 + height**2)
        angle = self.hingeAngleVal - 90 - (90 - self.mountAngleVal)
        hingePts = [boomPts[2], [boomPts[2][0] + hingeLength*cos(radians(angle)), 
                                 boomPts[2][1] + hingeLength*sin(radians(angle))]]
        
        xh = [i[0] for i in hingePts]
        yh = [i[1] for i in hingePts]
        self.barAx.plot(xh, yh, 'k', lw=2)
        
        self.barAx.set_ylim([-2,12])
        
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
        
        self.oceanRange.setText(QString.number(boomEnd[0] + (boomEnd[1]-self.waterLevelVal)/tan(radians(self.mountAngleVal-60)), 'f', 1))
        
        xb = [i[0] for i in [baseGround, baseTop, boomEnd]]
        yb = [i[1] for i in [baseGround, baseTop, boomEnd]]
        
        self.boomLine, = self.ax.plot(xb, yb)
        straightAngle = self.boomAngleVal - (90-self.mountAngleVal) - 90 + self.hingeAngleVal
        self.wedge = Wedge(boomEnd, 300, straightAngle-40, straightAngle+60, alpha=0.5, color='y')
        self.ax.add_artist(self.wedge)
        
        angle = -30+self.mountAngleVal+self.hingeAngleVal+self.boomAngleVal
        self.oceanRange.setText(QString.number(boomEnd[0] + (boomEnd[1]-self.waterLevelVal)*tan(radians(angle)), 'f', 1))
        
        # Initialize cabling drawing
        cableMountBaseTop = [baseTop[0], baseTop[1] + self.cableMountHeight]
        pulleyA = [baseTop[0] + self.pulleyALocation*cos(radians(self.boomAngleVal)), baseTop[1] + self.pulleyALocation*sin(radians(self.boomAngleVal))]
        
        xc = [i[0] for i in [baseTop, cableMountBaseTop, pulleyA]]
        yc = [i[1] for i in [baseTop, cableMountBaseTop, pulleyA]]
        
        self.calculateCablingForces()
        
        self.cableLine, = self.ax.plot(xc, yc, 'k')
        
        self.fig.subplots_adjust(left=0.1)
        
    def update(self):
        
        # Dune calculations
        crestDrop = [self.crestVal[0], self.crestVal[1]-self.frontDropVal]
        waterPt = [(crestDrop[1]-self.frontHeightVal)/tan(radians(self.frontAngleVal)), self.frontHeightVal]
        landPt = [-(self.crestVal[1]-self.backHeightVal)/tan(radians(self.backAngleVal)), self.backHeightVal]
        
        xDune = [i[0] for i in [landPt, self.crestVal, crestDrop, waterPt]]
        yDune = [i[1] for i in [landPt, self.crestVal, crestDrop, waterPt]]
        
        # Base and boom calculations
        baseGround = [self.crestVal[0] - self.baseOffsetVal, self.crestVal[1] - self.baseDropVal]
        baseTop = [baseGround[0], baseGround[1] + self.baseHeightVal]
        boomEnd = [baseTop[0] + self.boomLengthVal*cos(radians(self.boomAngleVal)), baseTop[1] + self.boomLengthVal*sin(radians(self.boomAngleVal))]
        
        xBoom = [i[0] for i in [baseGround, baseTop, boomEnd]]
        yBoom = [i[1] for i in [baseGround, baseTop, boomEnd]]
                
        # Update drawing
        self.waterLine.set_ydata([self.waterLevelVal, self.waterLevelVal])
        
        self.duneLine.set_xdata(xDune)
        self.duneLine.set_ydata(yDune)
        
        self.boomLine.set_xdata(xBoom)
        self.boomLine.set_ydata(yBoom)
        
        self.wedge.set_center(boomEnd)
        straightAngle = self.boomAngleVal - (90-self.mountAngleVal) - 90 + self.hingeAngleVal
        self.wedge.set_theta1(straightAngle-40)
        
        self.wedge.set_theta2(straightAngle+60)
        
        self.drawBoomEnd()
        
        # Calculate and draw cabling
        cableMountBaseTop = [baseTop[0], baseTop[1] + self.cableMountHeight]
        pulleyA = [baseTop[0] + self.pulleyALocation*cos(radians(self.boomAngleVal)), baseTop[1] + self.pulleyALocation*sin(radians(self.boomAngleVal))]
        
        xc = [i[0] for i in [baseTop, cableMountBaseTop, pulleyA]]
        yc = [i[1] for i in [baseTop, cableMountBaseTop, pulleyA]]
        
        self.cableLine.set_xdata(xc)
        self.cableLine.set_ydata(yc)
        
        self.calculateCablingForces()
        
        # Update the interface
        angle = -30+self.mountAngleVal+self.hingeAngleVal+self.boomAngleVal
        self.oceanRange.setText(QString.number(boomEnd[0] + (boomEnd[1]-self.waterLevelVal)*tan(radians(angle)), 'f', 1))
        
        # Update the canvas
        self.fig.canvas.draw()
        
    def calculateCablingForces(self):
        
        h = self.pulleyALocation*sin(radians(self.boomAngleVal)) - self.cableMountHeight
        l = self.pulleyALocation*cos(radians(self.boomAngleVal))
        innerAngle = abs(atan2(h,l) - radians(self.boomAngleVal))
        f = (self.sensorWeight * sin(radians(90 - self.boomAngleVal)) / sin(innerAngle))
        
        self.pulleyAForce.setText(QString.number(f, 'f', 1))
        
        print degrees(innerAngle)
        
    def updateCrest(self, val):
        
        self.crestVal[1] = val
        self.update()
        
    def updateWaterLevel(self, val):
        
        self.waterLevelVal = val
        self.update()
        
    def updateBaseDrop(self, val):
        
        self.baseDropVal = val
        self.update()
        
    def updateBaseOffset(self, val):
        
        self.baseOffsetVal = val
        self.update()
        
    def updateBaseHeight(self, val):
        
        self.baseHeightVal = val
        self.update()
        
    def updateBoomAngle(self, val):
        
        self.boomAngleVal = val
        self.update()
        
    def updateBoomLength(self, val):
        
        self.boomLengthVal = val
        self.update()
        
    def updateMountAngle(self, val):
        
        self.mountAngleVal = val
        self.update()
        
    def updateHingeAngle(self, val):
        
        self.hingeAngleVal = val
        self.update()
        
    def updateCableTowerHeight(self, val):
        
        self.cableMountHeight = val
        self.update()
        
    def updatePulleyALocation(self, val):
        
        self.pulleyALocation = val
        self.update()
        
    def updateSensorWeight(self, val):
        
        self.sensorWeight = val
        self.update()
    
    def createLayout(self):
        self.mainFrame = QWidget()
        
        # Main horizontal layout
        mainLayout = QHBoxLayout()
        
        # Layouts
        controlLayout = QGridLayout()
        infoLayout = QGridLayout()
        leftLayout = QVBoxLayout()
        viewLayout = QVBoxLayout()
        
        line = QFrame(self.mainFrame)
        line.setFrameStyle(QFrame.HLine | QFrame.Raised)
        
        leftLayout.addLayout(controlLayout)
        leftLayout.addWidget(line)
        leftLayout.addLayout(infoLayout)
        leftLayout.addStretch()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(viewLayout)
        
        # Info List
        infoLayout.addWidget(QLabel('<b>LIDAR</b>'), 0, 0, 1, 2, Qt.AlignCenter)
        infoLayout.addWidget(QLabel('Ocean Sight Range:'), 1, 0)
        infoLayout.addWidget(QLabel('<b>Structural</b>'), 2, 0, 1, 2, Qt.AlignCenter)
        infoLayout.addWidget(QLabel('Force - Pulley A (lb)'), 3, 0)
        
        self.oceanRange = QLabel('-', self.mainFrame)
        self.pulleyAForce = QLabel('-', self.mainFrame)

        infoLayout.addWidget(self.oceanRange, 1, 1)
        infoLayout.addWidget(self.pulleyAForce, 3, 1)
        
        infoLayout.setColumnMinimumWidth(1, 100)
        
        # Control grid
        controlLayout.addWidget(QLabel('<b>Dune/Ocean</b>'), 0, 0, 1, 2, Qt.AlignCenter)
        controlLayout.addWidget(QLabel('Dune Crest'), 1, 0)
        controlLayout.addWidget(QLabel('Water Level'), 2, 0)
        controlLayout.addWidget(QLabel('<b>Boom Geometry</b>'), 3, 0, 1, 2, Qt.AlignCenter)
        controlLayout.addWidget(QLabel('Base Drop'), 4, 0)
        controlLayout.addWidget(QLabel('Base Offset'), 5, 0)
        controlLayout.addWidget(QLabel('Base Height'), 6, 0)
        controlLayout.addWidget(QLabel('Boom Length'), 7, 0)
        controlLayout.addWidget(QLabel('Boom Angle'), 8, 0)
        controlLayout.addWidget(QLabel('<b>Mount Geometry</b>'), 9, 0, 1, 2, Qt.AlignCenter)
        controlLayout.addWidget(QLabel('Mount Cut Angle'), 10, 0)
        controlLayout.addWidget(QLabel('Hinge Angle'), 11, 0)
        controlLayout.addWidget(QLabel('<b>Cabling Geometry</b>'), 12, 0, 1, 2, Qt.AlignCenter)
        controlLayout.addWidget(QLabel('Cable Mount Height'), 13, 0)
        controlLayout.addWidget(QLabel('Pulley A Location'), 14, 0)
        controlLayout.addWidget(QLabel('<b>Loading (lbs)</b>'), 15, 0, 1, 2, Qt.AlignCenter)
        controlLayout.addWidget(QLabel('LIDAR Weight'), 16, 0)
        controlLayout.addWidget(QLabel('Boom Weight'), 17, 0)
        
        self.crestHeight = QDoubleSpinBox(self.mainFrame)
        self.crestHeight.setSingleStep(0.1)
        self.crestHeight.setValue(self.crestVal[1])
        controlLayout.addWidget(self.crestHeight, 1, 1)
        self.connect(self.crestHeight, SIGNAL('valueChanged(double)'), self.updateCrest)
        
        self.waterLevel = QDoubleSpinBox(self.mainFrame)
        self.waterLevel.setSingleStep(0.1)
        self.waterLevel.setValue(self.waterLevelVal)
        controlLayout.addWidget(self.waterLevel, 2, 1)
        self.connect(self.waterLevel, SIGNAL('valueChanged(double)'), self.updateWaterLevel)
        
        self.baseDrop = QDoubleSpinBox(self.mainFrame)
        self.baseDrop.setSingleStep(0.1)
        self.baseDrop.setValue(self.baseDropVal)
        controlLayout.addWidget(self.baseDrop, 4, 1)
        self.connect(self.baseDrop, SIGNAL('valueChanged(double)'), self.updateBaseDrop)
        
        self.baseOffset = QDoubleSpinBox(self.mainFrame)
        self.baseOffset.setSingleStep(0.1)
        self.baseOffset.setValue(self.baseOffsetVal)
        controlLayout.addWidget(self.baseOffset, 5, 1)
        self.connect(self.baseOffset, SIGNAL('valueChanged(double)'), self.updateBaseOffset)
        
        self.baseHeight = QDoubleSpinBox(self.mainFrame)
        self.baseHeight.setSingleStep(0.1)
        self.baseHeight.setValue(self.baseHeightVal)
        controlLayout.addWidget(self.baseHeight, 6, 1)
        self.connect(self.baseHeight, SIGNAL('valueChanged(double)'), self.updateBaseHeight)
        
        self.boomLength = QDoubleSpinBox(self.mainFrame)
        self.boomLength.setSingleStep(0.1)
        self.boomLength.setValue(self.boomLengthVal)
        controlLayout.addWidget(self.boomLength, 7, 1)
        self.connect(self.boomLength, SIGNAL('valueChanged(double)'), self.updateBoomLength)
        
        self.boomAngle = QDoubleSpinBox(self.mainFrame)
        self.boomAngle.setSingleStep(0.5)
        self.boomAngle.setMaximum(360)
        self.boomAngle.setValue(self.boomAngleVal)
        controlLayout.addWidget(self.boomAngle, 8, 1)
        self.connect(self.boomAngle, SIGNAL('valueChanged(double)'), self.updateBoomAngle)
        
        self.mountAngle = QDoubleSpinBox(self.mainFrame)
        self.mountAngle.setSingleStep(0.5)
        self.mountAngle.setMaximum(360)
        self.mountAngle.setValue(self.mountAngleVal)
        controlLayout.addWidget(self.mountAngle, 10, 1)
        self.connect(self.mountAngle, SIGNAL('valueChanged(double)'), self.updateMountAngle)
        
        self.hingeAngle = QDoubleSpinBox(self.mainFrame)
        self.hingeAngle.setSingleStep(0.5)
        self.hingeAngle.setMaximum(360)
        self.hingeAngle.setValue(self.hingeAngleVal)
        controlLayout.addWidget(self.hingeAngle, 11, 1)
        self.connect(self.hingeAngle, SIGNAL('valueChanged(double)'), self.updateHingeAngle)
        
        self.cableTowerHeight = QDoubleSpinBox(self.mainFrame)
        self.cableTowerHeight.setSingleStep(0.1)
        self.cableTowerHeight.setValue(self.cableMountHeight)
        controlLayout.addWidget(self.cableTowerHeight, 13, 1)
        self.connect(self.cableTowerHeight, SIGNAL('valueChanged(double)'), self.updateCableTowerHeight)
        
        self.pulleyADistance = QDoubleSpinBox(self.mainFrame)
        self.pulleyADistance.setSingleStep(0.1)
        self.pulleyADistance.setValue(self.pulleyALocation)
        controlLayout.addWidget(self.pulleyADistance, 14, 1)
        self.connect(self.pulleyADistance, SIGNAL('valueChanged(double)'), self.updatePulleyALocation)
        
        self.lidarWeight = QDoubleSpinBox(self.mainFrame)
        self.lidarWeight.setSingleStep(5)
        self.lidarWeight.setMaximum(9999999)
        self.lidarWeight.setValue(self.sensorWeight)
        controlLayout.addWidget(self.lidarWeight, 16, 1)
        self.connect(self.lidarWeight, SIGNAL('valueChanged(double)'), self.updateSensorWeight)
        
        # Create the axes
        self.fig = Figure((5.0, 4.0))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mainFrame)
        self.ax = self.fig.add_subplot(211, aspect='equal')
        self.barAx = self.fig.add_subplot(212, aspect='equal')
        self.ax.set_xlim([-15,10])
        self.drawBoomEnd()
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