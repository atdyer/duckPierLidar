from matplotlib import pyplot as plt
from math import degrees, radians, atan2, sin, cos
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np

###################################################### General settings
useEqualAxes = True     # Angles look funny without equal axes
lw = 3.0                # Width of tower lines

baseDistance = 12           #### Distance from the dune peak in meters
baseDrop = 1                #### Elevation below the dune peak in meters
baseHeight = 4 * 0.3048     #### The height of the base

boomLength = 40 * 0.3048        #### Boom length in meters
boomAngle = 20                  #### Boom angle in degrees (from horizontal)

mountAngle = -63         #### Angle of the mount in degrees (from horizontal)

f1 = open('/home/tristan/Desktop/data/survey/AWAC_line_topo.txt', 'r')
f2 = open('/home/tristan/Desktop/data/survey/AWAC_10m_north_topo.txt', 'r')
f3 = open('/home/tristan/Desktop/data/survey/AWAC_15m_south_topo.txt', 'r')

x1 = []
y1 = []
z1 = []

x2 = []
y2 = []
z2 = []

x3 = []
y3 = []
z3 = []

for line in f1:
    dat = line.split(',')
    x1.append(float(dat[0]))
    y1.append(float(dat[1]))
    z1.append(float(dat[2]))

for line in f2:
    dat = line.split(',')
    x2.append(float(dat[0]))
    y2.append(float(dat[1]))
    z2.append(float(dat[2]))

for line in f3:
    dat = line.split(',')
    x3.append(float(dat[0]))
    y3.append(float(dat[1]))
    z3.append(float(dat[2]))

fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
ax = Axes3D(fig)
ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

ax.plot(x1, y1, z1)
ax.plot(x2, y2, z2)
ax.plot(x3, y3, z3)


###################################################### Calculate dune peaks
mM = max(z1)
peakM = [x1[z1.index(mM)], y1[z1.index(mM)], mM]
mN = max(z2)
peakN = [x2[z2.index(mN)], y2[z2.index(mN)], mN]
mS = max(z3)
peakS = [x3[z3.index(mS)], y3[z3.index(mS)], mS]

print "Dune peaks: ", peakM[2], peakN[2], peakS[2]

peakX = [peakN[0], peakS[0]]
peakY = [peakN[1], peakS[1]]
peakZ = [peakN[2], peakS[2]]
ax.plot(peakX, peakY, peakZ)

# Create bounding box for equal axis ranges
if useEqualAxes:
    xs = np.array(x1 + x2 + x3)
    ys = np.array(y1 + y2 + y3)
    zs = np.array(z1 + z2 + z3)
    maxrange = np.array([xs.max()-xs.min(), ys.max()-ys.min(), zs.max()-zs.min()]).max() / 2.0
    meanx = xs.mean()
    meany = ys.mean()
    meanz = zs.mean()
    ax.set_xlim(meanx - maxrange, meanx + maxrange)
    ax.set_ylim(meany - maxrange, meany + maxrange)
    ax.set_zlim(meanz - maxrange, meanz + maxrange)

###################################################### Calculate dune angle

xN = peakN[0]
yN = peakN[1]
xM = peakM[0]
yM = peakM[1]
xS = peakS[0]
yS = peakS[1]

duneAngle = atan2(yN-yS, xN-xS)

print "Dune angle: ", degrees(duneAngle), " degrees"

###################################################### Draw the base



# Returns 3 drawing objects and 3 points (which are the top of each base)
def drawBase(baseDistanceN, baseDistanceM, baseDistanceS, 
             baseDropN, baseDropM, baseDropS,
             baseHeightN, baseHeightM, baseHeightS):
             
    duneAnglePerp = duneAngle-radians(90)
    baseNorth = [xN - baseDistanceN*cos(duneAnglePerp), yN - baseDistanceN*sin(duneAnglePerp)]
    baseMiddle = [xM - baseDistanceM*cos(duneAnglePerp), yM - baseDistanceM*sin(duneAnglePerp)]
    baseSouth = [xS - baseDistanceS*cos(duneAnglePerp), yS - baseDistanceS*sin(duneAnglePerp)]
    baseN = [[baseNorth[0], baseNorth[0]], [baseNorth[1], baseNorth[1]], [mN - baseDropN, mN - baseDropN + baseHeightN]]
    baseM = [[baseMiddle[0], baseMiddle[0]], [baseMiddle[1], baseMiddle[1]], [mM - baseDropM, mM - baseDropM + baseHeightM]]
    baseS = [[baseSouth[0], baseSouth[0]], [baseSouth[1], baseSouth[1]], [mS - baseDropS, mS - baseDropS + baseHeightS]]
    endN = [baseN[0][1], baseN[1][1], baseN[2][1]]
    endM = [baseM[0][1], baseM[1][1], baseM[2][1]]
    endS = [baseS[0][1], baseS[1][1], baseS[2][1]]
    nLine, = ax.plot(baseN[0], baseN[1], baseN[2], 'k', linewidth=lw)
    mLine, = ax.plot(baseM[0], baseM[1], baseM[2], 'k', linewidth=lw)
    sLine, = ax.plot(baseS[0], baseS[1], baseS[2], 'k', linewidth=lw)
    return nLine, mLine, sLine, endN, endM, endS


###################################################### Draw the boom



def drawBoom(nLength, mLength, sLength,
             nAngle, mAngle, sAngle,
             nBaseTop, mBaseTop, sBaseTop):
    
    duneAnglePerp = duneAngle-radians(90)
    boomAngleN = radians(nAngle)
    boomAngleM = radians(mAngle)
    boomAngleS = radians(sAngle)
    
    boomDistNorth = nLength*cos(boomAngleN)
    boomDistMid = mLength*cos(boomAngleM)
    boomDistSouth = sLength*cos(boomAngleS)
    
    nBoomEnd = [nBaseTop[0] + boomDistNorth*cos(duneAnglePerp), 
                nBaseTop[1] + boomDistNorth*sin(duneAnglePerp), 
                nBaseTop[2] + nLength*sin(boomAngleN)]
    mBoomEnd = [mBaseTop[0] + boomDistMid*cos(duneAnglePerp), 
                mBaseTop[1] + boomDistMid*sin(duneAnglePerp), 
                mBaseTop[2] + mLength*sin(boomAngleM)]
    sBoomEnd = [sBaseTop[0] + boomDistSouth*cos(duneAnglePerp), 
                sBaseTop[1] + boomDistSouth*sin(duneAnglePerp), 
                sBaseTop[2] + sLength*sin(boomAngleS)]

    boomNorth = [[nBaseTop[0], nBoomEnd[0]], [nBaseTop[1], nBoomEnd[1]], [nBaseTop[2], nBoomEnd[2]]]
    boomMid = [[mBaseTop[0], mBoomEnd[0]], [mBaseTop[1], mBoomEnd[1]], [mBaseTop[2], mBoomEnd[2]]]
    boomSouth = [[sBaseTop[0], sBoomEnd[0]], [sBaseTop[1], sBoomEnd[1]], [sBaseTop[2], sBoomEnd[2]]]
    
    print sBoomEnd

    nLine, = ax.plot(boomNorth[0], boomNorth[1], boomNorth[2], 'k', linewidth=lw)
    mLine, = ax.plot(boomMid[0], boomMid[1], boomMid[2], 'k', linewidth=lw)
    sLine, = ax.plot(boomSouth[0], boomSouth[1], boomSouth[2], 'k', linewidth=lw)
    
    return nLine, mLine, sLine, nBoomEnd, mBoomEnd, sBoomEnd
    

###################################################### Draw the angle mount



def drawMount(nBoomEnd, mBoomEnd, sBoomEnd,
              nAngle, mAngle, sAngle):
    
    mountLen = 1
    duneAnglePerp = duneAngle-radians(90)
    nAngle = radians(nAngle)
    mAngle = radians(mAngle)
    sAngle = radians(sAngle)
    
    mountDistNorth = mountLen*cos(nAngle)
    mountDistMid = mountLen*cos(mAngle)
    mountDistSouth = mountLen*cos(sAngle)
    
    mountEndNorth = [nBoomEnd[0] - mountDistNorth*cos(duneAnglePerp),
                     nBoomEnd[1] - mountDistNorth*sin(duneAnglePerp),
                     nBoomEnd[2] - mountLen*sin(nAngle)]
    mountEndMid = [mBoomEnd[0] - mountDistMid*cos(duneAnglePerp),
                   mBoomEnd[1] - mountDistMid*sin(duneAnglePerp),
                   mBoomEnd[2] - mountLen*sin(mAngle)]
    mountEndSouth = [sBoomEnd[0] - mountDistSouth*cos(duneAnglePerp),
                     sBoomEnd[1] - mountDistSouth*sin(duneAnglePerp),
                     sBoomEnd[2] - mountLen*sin(sAngle)]
    
    mountNorth = [[nBoomEnd[0], mountEndNorth[0]], [nBoomEnd[1], mountEndNorth[1]], [nBoomEnd[2], mountEndNorth[2]]]
    mountMid = [[mBoomEnd[0], mountEndMid[0]], [mBoomEnd[1], mountEndMid[1]], [mBoomEnd[2], mountEndMid[2]]]
    mountSouth = [[sBoomEnd[0], mountEndSouth[0]], [sBoomEnd[1], mountEndSouth[1]], [sBoomEnd[2], mountEndSouth[2]]]
    
    nLine, = ax.plot(mountNorth[0], mountNorth[1], mountNorth[2], 'k', linewidth=lw)
    mLine, = ax.plot(mountMid[0], mountMid[1], mountMid[2], 'k', linewidth=lw)
    sLine, = ax.plot(mountSouth[0], mountSouth[1], mountSouth[2], 'k', linewidth=lw)
    
    return nLine, mLine, sLine
    
###################################################### Draw the linescan

def drawLinescan(nBoomEnd, mBoomEnd, sBoomEnd,
                 nAngle, mAngle, sAngle):
    
    topAngle = 60
    bottomAngle = 40
    sightDistance = 50
    dTheta = 5
    numScans = (topAngle+bottomAngle)/dTheta
    duneAnglePerp = duneAngle-radians(90)
    
    for scan in range(numScans):
        scanAngle = scan*dTheta
        
        nTheta = radians(nAngle + topAngle - scanAngle)
        mTheta = radians(mAngle + topAngle - scanAngle)
        sTheta = radians(sAngle + topAngle - scanAngle)
        
        nDist = sightDistance*cos(nTheta)
        mDist = sightDistance*cos(mTheta)
        sDist = sightDistance*cos(sTheta)
        
        scanEndN = [nBoomEnd[0] + nDist*cos(duneAnglePerp),
                    nBoomEnd[1] + nDist*sin(duneAnglePerp),
                    nBoomEnd[2] + sightDistance*sin(nTheta)]
        scanEndM = [mBoomEnd[0] + mDist*cos(duneAnglePerp),
                    mBoomEnd[1] + mDist*sin(duneAnglePerp),
                    mBoomEnd[2] + sightDistance*sin(mTheta)]
        scanEndS = [sBoomEnd[0] + sDist*cos(duneAnglePerp),
                    sBoomEnd[1] + sDist*sin(duneAnglePerp),
                    sBoomEnd[2] + sightDistance*sin(sTheta)]
        
        scanNorth = [[nBoomEnd[0], scanEndN[0]], [nBoomEnd[1], scanEndN[1]], [nBoomEnd[2], scanEndN[2]]]
        scanMid = [[mBoomEnd[0], scanEndM[0]], [mBoomEnd[1], scanEndM[1]], [mBoomEnd[2], scanEndM[2]]]
        scanSouth = [[sBoomEnd[0], scanEndS[0]], [sBoomEnd[1], scanEndS[1]], [sBoomEnd[2], scanEndS[2]]]
        
        #ax.plot(scanNorth[0], scanNorth[1], scanNorth[2], 'y')
        #ax.plot(scanMid[0], scanMid[1], scanMid[2], 'y')
        ax.plot(scanSouth[0], scanSouth[1], scanSouth[2], 'y')
    

###################################################### Drawing tests

# Draw the bases [horizontal distance from dune peak, vertical distance from dune peak, base height]
baseN, baseM, baseS, topN, topM, topS = drawBase(baseDistance, baseDistance, baseDistance, baseDrop, baseDrop, baseDrop, baseHeight, baseHeight, baseHeight)

# Draw the booms [boom length, boom angle, 3d point top of base]
boomN, boomM, boomS, endN, endM, endS = drawBoom(boomLength, boomLength, boomLength, boomAngle, boomAngle, boomAngle, topN, topM, topS)

# Draw the mounts
mountN, mountM, mountS = drawMount(endN, endM, endS, mountAngle, mountAngle, mountAngle)

# Draw the scanlines
drawLinescan(endN, endM, endS, mountAngle, mountAngle, mountAngle)

plt.show()
