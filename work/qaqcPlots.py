from LineScanFile import LineScanFile
import matplotlib.pyplot as plt
import numpy as np

def makeQuickPtPlot(f):
    
    #rangeValues = f.range()
    
    plt.xlabel("Cross Shore Distance (m)")
    plt.ylabel("Elevation (m NAVD88)")
    plt.xlim([0, 300])
    plt.ylim([-5, 20])
    xDat = f.Rmat(0, 2088, 5)
    yDat = f.Zmat(0, 2088, 5)
    plt.plot(np.ma.masked_array(xDat, np.isnan(xDat)),
             np.ma.masked_array(yDat, np.isnan(yDat)), 'b.')
    plt.show()

def makeWaveStatsPlot(f):
    
    plt.plot(f.range(), f.minForeshore())
    plt.show()

f = LineScanFile('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1530-01.VZ1000.NOFRAME.line.mat')
makeQuickPtPlot(f)
#makeWaveStatsPlot(f)