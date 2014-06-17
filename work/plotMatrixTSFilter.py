from matplotlib import pyplot as plt
from LineScanFile import LineScanFile
import numpy as np

#########################
# Create plotting stuff #
#########################

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

#####################
# Create file stuff #
#####################

ts = 0
f = LineScanFile('/home/tristan/Desktop/data/20121227-1530-01.VZ1000.NOFRAME.line.mat')
dataset = f.waterPtsFilt()

#########################
# The outlier functions #
#########################

def findFirstAvg(dat):
    
    numPtsFound = 0
    i = 0
    runningTotal = 0.0
    while numPtsFound < 10:
        if not np.isnan(dat[i]):
            runningTotal += dat[i]
            numPtsFound += 1
        i += 1
    return runningTotal / 10.0

def removeOutliersDistance(dat, startingPt, verticalAllowance):
    
    dx = 0
    currentLevel = startingPt
    cleanData = []
    
    for val in dat:
        
        dx += 1
        if np.isnan(val):
            cleanData.append(val)
        else:
            verticalDifference = val - currentLevel
            if hasattr(verticalAllowance, '__call__'):
                if abs(verticalDifference) > verticalAllowance(dx):
                    cleanData.append(np.nan)
                else:
                    cleanData.append(val)
                    currentLevel = val
                    dx = 0
            else:
                if abs(verticalDifference) > verticalAllowance:
                    cleanData.append(np.nan)
                else:
                    cleanData.append(val)
                    currentLevel = val
                    dx = 0
    return cleanData

#########################
# The plotting function #
#########################

def plotTS(ts):
    global ax1, ax2
    plt.subplot(211)
    plt.cla()
    plt.subplot(212)
    plt.cla()
    newDat = dataset[:,ts]
    ax1.plot(newDat, '.')
    ax2.plot(removeOutliersDistance(newDat, findFirstAvg(newDat),
            lambda x: 0.1*x*x), '.')
    
#################################
# Create the key event function #
#################################

def keyEvent(event):
    global ts
    if event.key == 'right':
        ts += 1
    if event.key == 'left' and ts > 1:
        ts -= 1
    plotTS(ts)

#########################################################
# Connect the event handler and plot the first timestep #
#########################################################

fig.canvas.mpl_connect('key_press_event', keyEvent)
ax1.plot(dataset[:,0])
ax2.plot(dataset[:,0])
plt.show()