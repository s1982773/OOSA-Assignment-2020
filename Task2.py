

from pyproj import Proj, transform # package for reprojecting data
from processLVIS import lvisGround
from handleTiff import tiffHandle
from scipy.ndimage.filters import gaussian_filter1d
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
from gdal import Warp
import numpy as np
import h5py

# class RasterProcessing(lvisGround,tiffHandle):




if __name__=="__main__":
  '''Main block'''

  #read several files
  listfile='/home/s1909844/OOSA/OOSA-code-public/assignment_2020/src/x.list'
  files = []
  with open(listfile,'r') as f:
      for line in f:
          filename='/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/' + line
          files.append(filename.strip())
  k = 0
  for filename in files:
#      filename='/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/ILVIS1B_AQ2015_1017_R1605_059744.h5'
      
      #load all the data 
      b=lvisGround(filename,onlyBounds=True)
      
      
      # subset some bounds
      for i in range(50):
          for j in range(50):
              x0=(b.bounds[2]-b.bounds[0])*i/50 + b.bounds[0]
              y0=(b.bounds[3]-b.bounds[1])*j/50 + b.bounds[1]
              x1=(b.bounds[2]-b.bounds[0])*(i+1)/50+b.bounds[0]
              y1=(b.bounds[3]-b.bounds[1])*(j+1)/50+b.bounds[1]           
              c = lvisGround(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)
              
              if(c.value=='no data'):
                  print('no data')                            
              else:
                  k = k + 1
                  epsg = 3031
                  c.reproject(4326,epsg)
                  if(k==1):                                       
                      x = c.lon
                      y = c.lat
                      c.setElevations()
                    
                      data = c.estimateGround()
                      minX=np.min(x)
                      maxX=np.max(x)
                      minY=np.min(y)
                      maxY=np.max(y)
                    
                      res = 100
                    
                      nx=int((maxX-minX)/res+1)
                      ny=int((maxY-minY)/res+1)
                  else:
                      x = np.concatenate([x,c.lon])
                      y = np.concatenate([y,c.lat])
                      c.setElevations()
                      data = np.concatenate([data,c.estimateGround()])
                      
                      minX=np.min(x)
                      maxX=np.max(x)
                      minY=np.min(y)
                      maxY=np.max(y)
                    
                      res = 100
                      
                      nx=int((maxX-minX)/res+1)
                      ny=int((maxY-minY)/res+1)
                
            
  tiff = tiffHandle(filename,minX,minY,maxX,maxY,nx,ny,x,y)
  new_filename = 'task2_map.tif'
  f=h5py.File(filename,'r')
  tiff.writeTiff(data,res,new_filename,epsg)

