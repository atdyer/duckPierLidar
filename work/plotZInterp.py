import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import h5py

def X(f):
    
    return f['coredat/X']

def Y(f):
    
    return f['coredat/Y']

def T(f):
    
    return f['coredat/T']
    
def getRange(f):
    
    return f['coredat/range']

def getRawData(ts):
    
    dat = f['ptdat/Rmat']
    return dat[ts]

def plotSparsity(data, xmin=0, ymin=0, xmax=0, ymax=0):
    
    if xmax == 0:
        xmax = data.shape[0]
    if ymax == 0:
        ymax = data.shape[1]
        
    plt.spy(data[xmin:xmax, ymin:ymax])
    plt.show()

def plotRawData(f, ts, rangeMin=0, rangeMax=0):
    
    r = getRange(f)
    
    if rangeMax == 0:
        rangeMax = r.shape[0]
    
    print "Reading data"
    xvalsFull = getRange(f)
    yvalsFull = getRawData(ts)
    
    print "Slicing data"
    xvals = xvalsFull[rangeMin:rangeMax]
    yvals = yvalsFull[rangeMin:rangeMax]
    
    print "Plotting from " + str(rangeMin) + " to " + str(rangeMax)
    plt.plot(xvals, yvals)
    plt.show()

def plotSparseContours(xdat, ydat, data, xmin=0, ymin=0, xmax=0, ymax=0):
    
    if xmax == 0:
        xmax = data.shape[0]
    if ymax == 0:
        ymax = data.shape[1]
    
    xvals = []
    yvals = []
    zvals = []
    #zmin = 99999
    #zmax = -99999
    
    count = 0
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            z = data[x][y]
            if not math.isnan(z):
                count += 1
                xvals.append(xdat[x])
                yvals.append(ydat[y])
                zvals.append(z)
                
                #if z < zmin:
                #    zmin = z
                #elif z > zmax:
                #    zmax = z
    print count
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(xvals, yvals, zvals)
    plt.show()

#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1530-01.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1830-07.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1900-01.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1930-05.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0700-00.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0730-00.VZ1000.NOFRAME.line.mat', 'r')
f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0800-00.VZ1000.NOFRAME.line.mat', 'r')

plotRawData(f, 10)

#print "Reading data..."
#data = f['ptdat/Zinterp2'][:]

#print "Plotting data..."
#plotSparsity(data, 1000, 1000, 1100, 1100)
#plotSparseContours(X(f), Y(f), data, 0, 0, 200, 200)
#plt.pcolormesh(np.arange(xmin,xmax), np.arange(ymin,ymax), data[xmin:xmax, ymin:ymax], cmap='RdBu')
