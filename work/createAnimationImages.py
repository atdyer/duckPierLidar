from LineScanFile import LineScanFile
import matplotlib.pyplot as plt

def createAnimationImage(f, directory, ts):
    
    print "Creating image: " + str(ts)
    
    plt.clf()
    plt.xlabel("Cross Shore Distance (m)")
    plt.ylabel("Elevation (m NAVD88)")
    plt.xlim([0, 300])
    plt.ylim([-5, 20])
    plt.title("t = %7.10f" % f.time()[0][ts])
    xDat = f.Rmat()[:,ts]
    yDat = f.Zmat()[:,ts]

    plt.plot(xDat, yDat, 'o', color="0.0")
    
    plt.savefig(directory+str(ts)+".png", bbox_inches='tight')
    #plt.show()



print "Opening File"
targetDir = '/home/tristan/Desktop/images/'
f = LineScanFile('/home/tristan/Desktop/data/20121227-1530-01.VZ1000.NOFRAME.line.mat')

print "Starting to create images"
#createAnimationImage(f, targetDir, 0)
for ts in range(0,100, 10):
    createAnimationImage(f, targetDir, ts)