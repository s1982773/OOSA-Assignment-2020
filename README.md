# OOSA-Assignment-2020-s1982773
OOSA-Assignment-2020-s1982773 created by GitHub Classroom

# OOSA-Assignment-2020

There are 4 tasks in final project. Fit.py is for the Function fitting part,whereas findQuartile_test.py is for Binary search.

## Fit.py
### Requirements
* modifying to include the correlation on the plot 
* Rescale the y axis to something more sensible 
* What other error metrics could you extract?


##### To include the correlation text on the plot, i used `plt.text(x,y,r' '=+str())`
    
    
    plt.text(15, 75, r'Correlation='+str(self.correl), color='red')
  
##### To rescale the y axis, i simply divided `self.wage` by 1000
    
    
    plt.plot(self.age,self.wage/1000,'.')
    plt.plot(x,y/1000)
    

    

## findQuartile_test.py
### Requirements
 * Add a binary search to the dataSorter() class from last week 
 * Add a method to plot the sorted array along with a line to show the crossing point found by a binary search

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

