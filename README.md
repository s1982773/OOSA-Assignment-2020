# OOSA-Assignment-2020-s1982773
OOSA-Assignment-2020-s1982773 created by GitHub Classroom

# OOSA-Assignment-2020

There are 4 tasks in final project. Fit.py is for the Function fitting part,whereas findQuartile_test.py is for Binary search.

## task1.py
### Requirements
* process a flight line to a DEM of any chosen resolution 
* convert DEM to geotiff format 


##### To include the correlation text on the plot, i used `plt.text(x,y,r' '=+str())`
    
    
    plt.text(15, 75, r'Correlation='+str(self.correl), color='red')
  
##### To rescale the y axis, i simply divided `self.wage` by 1000
    
    
    plt.plot(self.age,self.wage/1000,'.')
    plt.plot(x,y/1000)
    

    

## task2.py
### Requirements
 * Adapt the code from task 1 
 * process all of the 2015 data in to a single gap-filled DEM
 * in geotiff format, at a resolution of your choice

##### Add a binary search
I used `zip()` which is to map the similar index of multiple containers so that they can be used just using as single entity.
Also, `map(list())` can help to make sure the type is list and store them in x an y seperately.


    self.sortedWage=np.sort(self.wage)
    self.s = sorted(zip(self.age,self.wage))
    self.x,self.y = map(list,zip(*self.s))



##### plot the sorted array
Create a variable `Index` for the searching.
Therefore, the age can be found by the wage's index was called.


    Index = self.y.index(thisW)
    Age = self.x[Index]
    plt.bar(self.x,self.y)
    plt.bar(Age,thisW)


## task3.py
### Requirements
 * Write a new class to read both DEMs in to RAM 
 * Add a method to produce a new geotiff showing the change in elevation between the two dates

##### Add a binary search
I used `zip()` which is to map the similar index of multiple containers so that they can be used just using as single entity.
Also, `map(list())` can help to make sure the type is list and store them in x an y seperately.


    self.sortedWage=np.sort(self.wage)
    self.s = sorted(zip(self.age,self.wage))
    self.x,self.y = map(list,zip(*self.s))



## task4.py
### Requirements
 * Add a method to calculate contour lines	  
 * user defined interval
 * produce an image of the change in elevation overlayed with “contour lines”	

##### Add a binary search
I used `zip()` which is to map the similar index of multiple containers so that they can be used just using as single entity.
Also, `map(list())` can help to make sure the type is list and store them in x an y seperately.


    self.sortedWage=np.sort(self.wage)
    self.s = sorted(zip(self.age,self.wage))
    self.x,self.y = map(list,zip(*self.s))