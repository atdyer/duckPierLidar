from LineScanFile import LineScanFile
import matplotlib.pyplot as plt
import matplotlib.animation as animation

f = LineScanFile('/home/tristan/Desktop/data/20121227-1530-01.VZ1000.NOFRAME.line.mat')
ts = 0
mat = f.waterPtsFilt()

fig, ax = plt.subplots()
line, = ax.plot(mat[:,0])

def update(data):
    global ax, ts
    ax.set_title(str(ts))
    line.set_ydata(data)
    return line,

def data_gen():
    global ts, mat
    ts += 1
    yield mat[:,ts] 

anim = animation.FuncAnimation(fig, update, data_gen, interval=9)
plt.show()