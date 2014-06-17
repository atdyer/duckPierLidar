from LineScanFile import LineScanFile
import matplotlib.pyplot as plt

ts = 0
fig = plt.figure()
ax = fig.add_subplot(111)
f = LineScanFile('/home/tristan/Desktop/data/20121227-1530-01.VZ1000.NOFRAME.line.mat')

def keyEvent(event):
    global ts
    global ax
    global f
    plt.clf()
    if event.key == 'right':
        ts += 1
    if event.key == 'left':
        ts -= 1
    plt.plot(f.waterPtsFilt()[:,ts], '.')
    plt.xlim([0,2000])
    plt.ylim([-15,30])
    
fig.canvas.mpl_connect('key_press_event', keyEvent)
ax.plot(f.waterPtsFilt()[:,0], '.')
plt.show()