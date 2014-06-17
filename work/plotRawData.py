import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py
    
def getRange(f):
    
    return f['coredat/range']

def getRawData(ts):
    
    dat = f['ptdat/Rmat']
    return dat[ts]

def plotRawData(f, ts, rangeMin=0, rangeMax=0):
    
    r = getRange(f)
    
    if rangeMax == 0:
        rangeMax = r.shape[0]
    
    print "Reading data"
    xvals = r[rangeMin:rangeMax]
    yvals = getRawData(ts)[rangeMin:rangeMax]
    
    print "Plotting from " + str(rangeMin) + " to " + str(rangeMax)
    plt.plot(xvals, yvals)
    plt.show()

def readFrame(ts, rawDat, rangeMin, rangeMax):
    
    return rawDat[ts][rangeMin:rangeMax]

def animateRawData(f, startTS, endTS, rangeMin=0, rangeMax=0):
    
    r = getRange(f)
    
    if (rangeMax == 0):
        rangeMax = r.shape[0]
        
    print "Reading data"
    xvals = r[rangeMin:rangeMax]
    yvals = getRawData(startTS)
    
    print "Starting animation"
    plt.xlim(xvals[0], xvals[len(xvals)-1])
    
    numFrames = endTS-startTS
    animation.FuncAnimation(plt.figure(), readFrame, numFrames, fargs=(

#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1530-01.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1830-07.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1900-01.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1930-05.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0700-00.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0730-00.VZ1000.NOFRAME.line.mat', 'r')
f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0800-00.VZ1000.NOFRAME.line.mat', 'r')

plotRawData(f, 10)
