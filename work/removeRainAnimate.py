from LineScanFile import LineScanFile
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

verticalAllowance = 0.15
slopeAllowance = 0.3

f = LineScanFile('/home/tristan/Desktop/data/20121227-1530-01.VZ1000.NOFRAME.line.mat')
dataset = f.waterPtsRaw()

def findFirstAvg(dat):
    
    numPtsFound = 0
    i = 0
    firstIndex = 0
    runningTotal = 0.0
    while numPtsFound < 10:
        if not np.isnan(dat[i]):
            runningTotal += dat[i]
            numPtsFound += 1
            if numPtsFound == 1:
                firstIndex = i
        i += 1
    return runningTotal / 10.0

def processTimestepBoth(dat, startingPt, verticalAllowance, slopeAllowance):
    
    dx = 1
    currentLevel = startingPt
    previousSlope = 0.0
    cleanData = []
    
    for val in dat:
        
        if np.isnan(val):
            dx += 1
            cleanData.append(val)
        else:
            slope = (val - currentLevel) / dx
            if abs(val - currentLevel) > verticalAllowance and abs(previousSlope - slope) > slopeAllowance:
                    cleanData.append(np.nan)
                    dx += 1
            else:
                cleanData.append(val)
                dx = 1
                previousSlope = slope
                currentLevel = val

    return cleanData
                

def processTimestepSlope(dat, startingPt, slopeAllowance):
    
    dx = 1
    currentLevel = startingPt
    previousSlope = 0.0
    cleanData = []
    
    for val in dat:
        
        if np.isnan(val):
            dx += 1
            cleanData.append(val)
        else:
            slope = (val - currentLevel) / dx
            if abs(previousSlope - slope) > slopeAllowance:
                cleanData.append(np.nan)
                dx += 1
            else:
                cleanData.append(val)
                dx = 1
                previousSlope = slope
                currentLevel = val
    return cleanData
                

def processTimestep(dat, startingPt, verticalAllowance):
    
    blankSpaces = 0
    currentLevel = startingPt
    cleanData = []
    
    for val in dat:
        
        if np.isnan(val):
            blankSpaces += 1
            cleanData.append(val)
        else:
            if abs(currentLevel - val) > (1+blankSpaces*0.1)*verticalAllowance:
                cleanData.append(np.nan)
                blankSpaces += 1
            else:
                cleanData.append(val)
                blankSpaces = 0
                currentLevel = val
    return cleanData


ts = 0
fig, (ax1, ax2) = plt.subplots(2, 1)
dataStart = dataset[:,0]
line1, = ax1.plot(dataStart)
line2, = ax2.plot(processTimestepSlope(dataStart, findFirstAvg(dataStart),
                    slopeAllowance))

def update(data):
    global ax1, line1, line2, ts, verticalAllowance, slopeAllowance
    ax1.set_title(str(ts))
    line1.set_ydata(data)
    #line2.set_ydata(processTimestepBoth(data, findFirstAvg(data),
    #                verticalAllowance, slopeAllowance))
    line2.set_ydata(processTimestepSlope(data, findFirstAvg(data),
                    slopeAllowance))

def data_gen():
    global ts, dataset
    ts += 1
    yield dataset[:,ts]


anim = animation.FuncAnimation(fig, update, data_gen, interval=20)
plt.show()