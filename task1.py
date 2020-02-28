from lvisClass import lvisData
from processLVIS import lvisGround
from handleTiff import tiffHandle
from pyproj import Proj, transform # package for reprojecting data
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
from gdal import Warp
import numpy as np



# class Lvis_to_geoTiff(lvisData,tiffHandle):

#     def readData(self,filename,inp,outp):
#         lvisGround(filename,onlyBounds=True)

#         self.x0=lvisGround.bounds[0]
#         self.y0=lvisGround.bounds[1]
#         self.x1=(lvisGround.bounds[2]-lvisGround.bounds[0])/15+lvisGround.bounds[0]
#         self.y1=(lvisGround.bounds[3]-lvisGround.bounds[1])/15+lvisGround.bounds[1]

#         lvisGround.dumpBounds(self)    
#         lvisGround(filename,minX=self.x0,minY=self.y0,maxX=self.x1,maxY=self.y1)
#         lvisGround.reproject(self,inp,outp)   

#         self.x = self.lon
#         self.y = self.lat

#         lvisGround.setElevations(self)

#         self.maxX = np.max(self.x)
#         self.minX = np.min(self.x)
#         self.maxY = np.max(self.y)
#         self.minY = np.min(self.y)

#         self.zG = lvisGround.estimateGround(self)
    
#     def write_geotiff(self,res):
#         tiffHandle.writeTiff(self.zG,self.x,self.y)




if __name__ == '__main__':
    filename = '/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_049700.h5'
    #filename = '/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/ILVIS1B_AQ2015_1017_R1605_069264.h5'

  
    # op = Lvis_to_geoTiff(filename)
    op = lvisGround(filename,onlyBounds=True)
    x0=op.bounds[0]
    y0=op.bounds[1]
    x1=(op.bounds[2]-op.bounds[0])/15+op.bounds[0]
    y1=(op.bounds[3]-op.bounds[1])/15+op.bounds[1]

    
    # read in bounds
    w = lvisGround(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)
    w.reproject(4326,3031)    
    x = w.lon
    y = w.lat
    w.setElevations()
    maxX = np.max(x)
    minX = np.min(x)
    maxY = np.max(y)
    minY = np.min(y)
    zG = w.estimateGround()  
    # insert the resolution
    res =10
    lvis=tiffHandle(filename,maxX,minX,maxY,minY,res,x,y)
    new_filename = 'task1.tiff'
    lvis.writeTiff(zG,x,y,new_filename)
