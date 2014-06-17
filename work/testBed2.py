from LineScanFile import LineScanFile
import statsmodels.api as smapi
import statsmodels.graphics as smg
from statsmodels.formula.api import ols
import numpy as np
import matplotlib.pyplot as plt

f = LineScanFile('/home/tristan/Desktop/data/20121227-1530-01.VZ1000.NOFRAME.line.mat')
dataset = f.waterPtsRaw()[:,1000:1005]
x = np.arange(len(dataset))

timestepRange = 5
timestepShadow = []

def isOutlier(dat, index):
    
    if np.isnan(dat[index]):
        return True
    test = ols("data ~ x", data=dict(data=dat, x=np.arange(len(dat)))).fit().outlier_test()
    return test.icol(2)[index] < 1
    

timestepToPlot = 0

outlier = []
for i in range(len(dataset)):
    outlier.append(isOutlier(dataset[i], timestepToPlot))
    
cleanData = []
for i in range(len(dataset)):
    if outlier[i]:
        cleanData.append(np.nan)
    else:
        cleanData.append(dataset[i][timestepToPlot])

plt.figure(1)
plt.subplot(211)
plt.plot(dataset[:,0])

plt.subplot(212)
plt.plot(cleanData)
plt.show()

## Fit the data
#regression = ols("data ~ x", data=dict(data=dataset, x=x)).fit()
#
## Find outliers
#outX = []
#outY = []
#test = regression.outlier_test()
#for i, t in enumerate(test.icol(2)):
#    if t < 1:
#        outX.append(i)
#        outY.append(dataset[i])
#print 'Outliers: ', zip(outX, outY)
#
## Plot
#plt.plot(dataset, 'b.')
#plt.plot(outX, outY, 'r.')
#plt.show()

#figure = smg.regressionplots.plot_fit(regression, 1)
#smg.regressionplots.abline_plot(model_results=regression, ax=figure.axes[0])
#figure.show()