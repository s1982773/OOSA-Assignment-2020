import gdal, ogr, osr, os
import numpy as np

def raster2array(rasterfn):
    '''
    Convert Raster to array
    '''

    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.ReadAsArray()

def getNoDataValue(rasterfn):
    '''
    Get no data value of array
    '''

    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.GetNoDataValue()

def array2raster(rasterfn,newRasterfn,array):
    '''
    Write updated array to new raster
    '''

    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()
    print("Image written to",newRasterfn)

rasterfn = 'task2_map2.tif'
newValue = 0
newRasterfn = 'SlopeNew.tif'

# Convert Raster to array
rasterArray = raster2array(rasterfn)

#print(rasterArray.shape)
# Get no data value of array
noDataValue = getNoDataValue(rasterfn)

# Updata no data value in array with new value
rasterArray[rasterArray == noDataValue] = newValue

Location = np.argwhere(rasterArray == 0)

for i in Location:
    lonx = i[1]
    laty = i[0]
    Vleft = rasterArray[laty,lonx-1]
    Vright = rasterArray[laty,lonx+1]
    Vup = rasterArray[laty+1,lonx]
    Vdown = rasterArray[laty-1,lonx]


    if(lonx<=1 or laty<=1 or lonx>=rasterArray.shape[1]-1 or laty>=rasterArray.shape[0]-1):
        continue

    elif((Vdown!=0 and Vup!=0) or (Vleft!=0 and Vright!=0) or (Vup!=0 and Vleft!=0) or (Vup!=0 and Vright!=0) or (Vleft!=0 and Vdown!=0) or (Vright!=0 and Vdown!=0)):

        s1 = s2 = s3 = s4 = 1
        s5 = s6 = s7 = s8 = 1.414
        print(rasterArray[laty,lonx])


        if(rasterArray[laty-1,lonx-1]==0):
            s5=0
        if(rasterArray[laty+1,lonx-1]==0):
            s6=0
        if(rasterArray[laty-1,lonx+1]==0):
            s7=0
        if(rasterArray[laty+1,lonx+1]==0):
            s8=0
        S=s1+s2+s3+s4+s5+s6+s7+s8
#            print(laty)

        rasterArray[laty,lonx] = ((Vdown*s1+Vup*s2+Vleft*s3+Vright*s4+rasterArray[laty-1,lonx-1]*s5+rasterArray[laty+1,lonx-1]*s6+rasterArray[laty-1,lonx+1]*s7+rasterArray[laty+1,lonx+1]*s8)/S)





# Write updated array to new raster
array2raster(rasterfn,newRasterfn,rasterArray)
