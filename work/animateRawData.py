import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py
import math

#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1530-01.VZ1000.NOFRAME.line.mat', 'r')
f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1830-07.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1900-01.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121227-1930-05.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0700-00.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0730-00.VZ1000.NOFRAME.line.mat', 'r')
#f = h5py.File('C:\\Users\\USACE\\Desktop\\ForTristan\\20121230-0800-00.VZ1000.NOFRAME.line.mat', 'r')

rangeMin = 0
rangeMax = 0
zMin = 13.5
zMax = 14.5
startTS = 1000
endTS = 1100


def getRange(f):
    
    return f['coredat/range']

def getRawData():
    
    return f['ptdat/Rmat']

# Get x-values
r = getRange(f)
if rangeMax == 0:
    rangeMax = r.shape[0]-1

# Get raw data
rawData = getRawData()

# Create the empty plot
fig = plt.figure()
ax = plt.axes(xlim=(r[rangeMin][0], r[rangeMax][0]), ylim=(zMin, zMax))
line, = ax.plot([], [], lw=1)

# Animation initialization function
def init():
    line.set_data([], [])
    return line,

# Animation function
def animate(ts):
    #xDat = []
    #yDat = []
    #for i in range(rangeMin, rangeMax):
    #    rdat = rawData[ts][i]
    #    if not math.isnan(rdat):
    #        xDat.append(r[i])
    #        yDat.append(rdat)
    #line.set_data(xDat, yDat)
    line.set_data(r[rangeMin:rangeMax], rawData[ts][rangeMin:rangeMax])
    return line,

# Create animation
if endTS == 0:
    endTS = rawData.shape[0]
numTS = endTS-startTS

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=numTS, interval=100, blit=True)

#Save animation
#animWriter = animation.FFMpegWriter()
#anim.save('test_animation.mp4', writer=animWriter, fps=30, extra_args=['-vcodec', 'libx264'])

#Show animation
plt.show()