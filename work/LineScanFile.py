import h5py

class LineScanFile:
    
    def __init__(self, fileLocation):
        
        self.f = h5py.File(fileLocation, 'r')
        
    # coredat data
    def range(self):
        
        return self.f['coredat/range']
        
    def time(self):
        
        return self.f['coredat/T']
          
    # ptdat data
    def Rmat(self):

        return self.f['ptdat/Rmat']
        
    def Tmat(self):
        
        return self.f['ptdat/Tmat']
        
    def Zmat(self):
        
        return self.f['ptdat/Zmat']
        
    def Amat(self):
        
        return self.f['ptdat/Amat']
        
    def Zinterp(self):
        
        return self.f['ptdat/Zinterp']
        
    def Zinterp2(self):
        
        return self.f['ptdat/Zinterp2']
        
    def Ainterp(self):
        
        return self.f['ptdat/Ainterp']
        
    def ZDiff(self):
        
        return self.f['ptdat/ZDiff']
        
    #morphdat data
    def foreshorePtsRaw(self):
        
        return self.f['morphdat/foreshoreptsraw']
        
    def foreshorePtsFilt(self):
        
        return self.f['morphdat/foreshoreptsfilt']
        
    def meanForeshore(self):
        
        return self.f['morphdat/meanforeshore']
        
    def minForeshore(self):
        
        return self.f['morphdat/minforeshore']
        
    def maxForeshore(self):
        
        return self.f['morphdat/maxforeshore']
        
    def foreshoreSlope(self):
        
        return self.f['morphdat/foreshoreslope']
        
    def foreshoreSlopeInfo(self):
        
        return self.f['morphdat/foreshoreslopeinfo']
        
    #waterdat data
    def spectraAmp(self):
        
        return self.f['waterdat/spectraAmp']
        
    def Hsig(self):
        
        return self.f['waterdat/Hsig']
        
    def freq(self):
        
        return self.f['waterdat/Freq']
        
    def meanWaterLevel(self):
        
        return self.f['waterdat/meanwaterlevel']
        
    def waterPtsFilt(self):
        
        return self.f['waterdat/waterptsfilt']
        
    def minWaterLevel(self):
        
        return self.f['waterdat/minwaterlevel']
        
    def Hmo(self):
        
        return self.f['waterdat/Hmo']
        
    def Hsin(self):
        
        return self.f['waterdat/Hsin']
        
    def waterPtsRaw(self):
        
        return self.f['waterdat/waterptsraw']
        
    def peakPeriodIN(self):
        
        return self.f['waterdat/peakPeriodIN']
        
    def maxWaterLevel(self):
        
        return self.f['waterdat/maxwaterlevel']
        
    def peakPeriodIG(self):
        
        return self.f['waterdat/peakPeriodIG']