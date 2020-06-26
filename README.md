# OOSA-Assignment-2020
OOSA-Assignment-2020 created by GitHub Classroom

# OOSA-Assignment-2020

There are 4 tasks in final project. Each of them is connected to the previous one.

## task1.py
### Requirements
* process a flight line to a DEM of any chosen resolution 
* convert DEM to geotiff format 


##### To process a flight line, i used `lvisGround(filename,onlyBounds=True)`
    
    
    op = lvisGround(filename,onlyBounds=True)
    #set bounds
    x0=op.bounds[0]
    y0=op.bounds[1]
    x1=(op.bounds[2]-op.bounds[0])/15+op.bounds[0]
    y1=(op.bounds[3]-op.bounds[1])/15+op.bounds[1]
##### To convert DEM to geotiff format, i simply used the function `tiffHandle(filename,maxX,minX,maxY,minY,res,x,y)` 
    
    
    self.minX = x0
    self.minY = y0
    self.maxX = x1
    self.maxY = y1
    self.nX = nx
    self.nY = ny
    self.x = x
    self.y = y

    
##### i also try to make a class
    
    
    class Lvis_to_geoTiff(lvisData,tiffHandle):

## task2.py
### Requirements
 * Adapt the code from task 1 
 * process all of the 2015 data in to a single gap-filled DEM
 * in geotiff format, at a resolution of your choice

##### Adapt the code from task 1 
I didn't create any new codes for task1. but i use different method from task1 to `subset` the data
`range(50)` means i divided the image by 50 pieces



    for i in range(50):
          for j in range(50):
              x0=(b.bounds[2]-b.bounds[0])*i/50 + b.bounds[0]
              y0=(b.bounds[3]-b.bounds[1])*j/50 + b.bounds[1]
              x1=(b.bounds[2]-b.bounds[0])*(i+1)/50+b.bounds[0]
              y1=(b.bounds[3]-b.bounds[1])*(j+1)/50+b.bounds[1]           
              c = lvisGround(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)



##### process all of the 2015 data in to a single gap-filled DEM
process and concatenate the data by boolean


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


## task3.py
### Requirements
 * Write a new class to read both DEMs in to RAM 
 * Add a method to produce a new geotiff showing the change in elevation between the two dates

##### Add overlay function
I wrote `overlay()` to filter unnecessary data and keep what i want.
Also, ` intersection[y,x] = filename1[y,x]-filename2[y,x] ` can help to minus the overaly to get the difference of the elevation

    overlay(self,filename1,filename2)



## task4.py
### Requirements
 * Add a method to calculate contour lines	  
 * user defined interval
 * produce an image of the change in elevation overlayed with “contour lines”	

##### user defined interval
I used `np.where(self.data == 0)` to find the null data and give a new value.
Also, `newblock` is the amount of interval and `eachrange` is the value of each interval


    if(np.where(self.data == 0)):
            return -999.0
        else:
            for i in range(1,self.block):
                newblock = self.block*i
                eachrange = minZ+self.block*i
                self.interval_range= np.where(self.data == newblock, eachrange)
                i = i + 1
                
##### plot_contour_line
I used `plt.contourf` to draw the line but by using this may let the interval i set above function meaningless


    plt.contourf
