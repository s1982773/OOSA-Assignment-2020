
'''
A class to hold LVIS data
with methods to read
'''

###################################
import numpy as np
import h5py


###################################

class lvisData(object):
  '''
  LVIS data handler
  '''

  def __init__(self,filename,setElev=False,minX=-100000000,maxX=100000000,minY=-1000000000,maxY=100000000,onlyBounds=False,multifiles=False):
    '''
    Class initialiser. Calls a function
    to read LVIS data within bounds
    minX,minY and maxX,maxY
    setElev=1 converts LVIS's stop and start
    elevations to arrays of elevation.
    onlyBounds sets "bounds" to the corner of the area of interest
    '''
    # call the file reader and load in to the self
    self.readLVIS(filename,minX,minY,maxX,maxY,onlyBounds,multifiles)
    if(setElev):     # to save time, only read elev if wanted
      self.setElevations()


  ###########################################

  def readLVIS(self,filename,minX,minY,maxX,maxY,onlyBounds,multifiles):
    '''
    Read LVIS data from multifiles
    '''
    if(multifiles):
      k = 0
      for file in filename:
          print(file)
          f=h5py.File(file,'r')
          k = k + 1
#          print(k)
          if(k==1):
              nBins=f['RXWAVE'].shape[1]
              # read coordinates for subsetting
              lon0=np.array(f['LON0'])       # longitude of waveform top
              lat0=np.array(f['LAT0'])       # lattitude of waveform top
              lonN=np.array(f['LON'+str(nBins-1)]) # longitude of waveform bottom
              latN=np.array(f['LAT'+str(nBins-1)]) # lattitude of waveform bottom
              lfid=np.array(f['LFID'])         # LVIS flight ID number
              lShot=np.array(f['SHOTNUMBER'])  # the LVIS shot number, a label
              waves=np.array(f['RXWAVE'])    # the recieved waveforms. The data
              nBins=waves.shape[1]
              # these variables will be converted to easier variables
              lZN=np.array(f['Z'+str(nBins-1)])      # The elevation of the waveform bottom
              lZ0=np.array(f['Z0'])
          else:
              nBins=f['RXWAVE'].shape[1]
              lon0=np.concatenate([lon0,np.array(f['LON0'])])
              lat0=np.concatenate([lat0,np.array(f['LAT0'])])
              lonN=np.concatenate([lonN,np.array(f['LON'+str(nBins-1)])])
              latN=np.concatenate([latN,np.array(f['LAT'+str(nBins-1)])])
              lfid=np.concatenate([lfid,np.array(f['LFID'])])
              lShot=np.concatenate([lShot,np.array(f['SHOTNUMBER'])])
              waves=np.vstack([waves,np.array(f['RXWAVE'])])
              nBins=waves.shape[1]
              lZN=np.concatenate([lZN,np.array(f['Z'+str(nBins-1)])])
              lZ0=np.concatenate([lZ0,np.array(f['Z0'])])
      print(lZN.size)
      # find a single coordinate per footprint
      tempLon=(lon0+lonN)/2.0
      tempLat=(lat0+latN)/2.0

      # write out bounds and leave if needed
      if(onlyBounds):
        self.lon=tempLon
        self.lat=tempLat
        self.bounds=self.dumpBounds()
        return

      # dertermine which are in region of interest
      useInd=np.where((tempLon>=minX)&(tempLon<maxX)&(tempLat>=minY)&(tempLat<maxY))
      if(len(useInd)>0):
        useInd=useInd[0]

      if(len(useInd)==0):
        print("No data contained in that region")
        return
      

      # save the subset of all data
      self.nWaves=len(useInd)
      self.lon=tempLon[useInd]
      self.lat=tempLat[useInd]

      # load sliced arrays, to save RAM
      self.lfid=np.array(lfid)[useInd]          # LVIS flight ID number
      self.lShot=np.array(lShot)[useInd]   # the LVIS shot number, a label
      self.waves=np.array(waves)[useInd]       # the recieved waveforms. The data
      self.nBins=self.waves.shape[1]
      # these variables will be converted to easier variables
      self.lZ0=np.array(lZ0)[useInd]          # The elevation of the waveform top
      self.lZN=np.array(lZN)[useInd]       # The elevation of the waveform bottom
      
      # close file
      f.close()
      # return to initialiser

      return

    else:
        # open file for reading
        f=h5py.File(filename,'r')
        # determine how many bins
        self.nBins=f['RXWAVE'].shape[1]
        # read coordinates for subsetting
        lon0=np.array(f['LON0'])       # longitude of waveform top
        lat0=np.array(f['LAT0'])       # lattitude of waveform top
        lonN=np.array(f['LON'+str(self.nBins-1)]) # longitude of waveform bottom
        latN=np.array(f['LAT'+str(self.nBins-1)]) # lattitude of waveform bottom
        # find a single coordinate per footprint
        tempLon=(lon0+lonN)/2.0
        tempLat=(lat0+latN)/2.0

        # write out bounds and leave if needed
        if(onlyBounds):
          self.lon=tempLon
          self.lat=tempLat
          self.bounds=self.dumpBounds()
          return

        # dertermine which are in region of interest
        useInd=np.where((tempLon>=minX)&(tempLon<maxX)&(tempLat>=minY)&(tempLat<maxY))
        useInd=useInd[0]
        self.value = 0
#        print(useInd)
#        print(len(useInd))

        
        if(len(useInd)>0):
          #useInd=useInd[0]

          # save the subset of all data
          self.nWaves=len(useInd)
          self.lon=tempLon[useInd]
          self.lat=tempLat[useInd]
    
          # load sliced arrays, to save RAM
          self.lfid=np.array(f['LFID'])[useInd]          # LVIS flight ID number
          self.lShot=np.array(f['SHOTNUMBER'])[useInd]   # the LVIS shot number, a label
          self.waves=np.array(f['RXWAVE'])[useInd]       # the recieved waveforms. The data
          self.nBins=self.waves.shape[1]
          # these variables will be converted to easier variables
          self.lZN=np.array(f['Z'+str(self.nBins-1)])[useInd]       # The elevation of the waveform bottom
          self.lZ0=np.array(f['Z0'])[useInd]          # The elevation of the waveform top
          # close file
          f.close()
          # return to initialiser
          return
      
        else:
          print("No data contained in that region")
          self.value = 'no data'
          return


  ###########################################

  def setElevations(self):
    '''
    Decodes LVIS's RAM efficient elevation
    format and produces an array of
    elevations per waveform bin
    '''
    self.z=np.empty((self.nWaves,self.nBins))
    for i in range(0,self.nWaves):    # loop over waves
      res=(self.lZ0[i]-self.lZN[i])/self.nBins
      self.z[i]=np.arange(self.lZ0[i],self.lZN[i],-1.0*res)   # returns an array of floats


  ###########################################

  def getOneWave(self,ind):
    '''
    Return a single waveform
    '''
    return(self.z[ind],self.waves[ind])


  ###########################################

  def dumpCoords(self):
     '''
     Dump coordinates
     '''
     return(self.lon,self.lat)

  ###########################################

  def dumpBounds(self):
     '''
     Dump bounds
     '''
     return(np.min(self.lon),np.min(self.lat),np.max(self.lon),np.max(self.lat))


###########################################
