import numpy as np

import time
import sys

'''THESE ARE THE EXAMPLE FOR NUMPY'''

#define variable
Size=100000
#define two List
L1= range(Size)
L2= range(Size)
# define two NumPy array
A1= np.arange(Size)
A2= np.arange(Size)

Start = time.time()
#find the sum of list
Result = [(x,y) for x,y in zip(L1,L2)]
#this will give the time of list in order to compute the sum
print((time.time()-Start)*1000)
Start = time.time()
#find the sum of numpy
Result= A1+A2
print((time.time()-Start)*1000)

from pandas.tests.io.parser import skiprows

a=np.array([(1,2,3,5),(2,3,4,6)])
print(a.ndim)# 2 dimensional array
print(a.itemsize) # 4 each element occupy 4 bytes
print(a.dtype)# int32 -  type of data is integer
print(a.size)# size is 6
print(a.shape)# (2, 4) -- 2 rows and 4 columns
b=a.reshape(4, 2)
print(b)# before it was (2, 4) after reshape it become (4, 2) 
# like:
# [[1 2]
#  [3 5]
#  [2 3]
#  [4 6]]"""

'''slicing'''
a=np.array([(1,2,3,4),(3,4,5,6),(7,8,9,10)])
print(a[0,2])# 3 -Here we are accessing the zeroth element with index 2 i,e; 3
print(a[1,2])# 5 -Here we are accessing the first element with index 2 i,e; 5
print(a[0:,3])# [ 4  6 10] =>0: means its include all the rows and print the index 3 i,e;[ 4  6 10]
print(a[0:2,3])#[4 6] Here it will not include the 2nd element it only include the 0 and 1 element

'''linspace'''
a=np.linspace(1,3,5)
print(a)#[1.  1.5 2.  2.5 3. ]
b=np.linspace(1,3,10)
print(b)#[1.   1.22222222 1.44444444 1.66666667 1.88888889 2.11111111  2.33333333 2.55555556 2.77777778 3.  ]"""

'''max,min,sum'''
c=np.array([1,2,3,4])
print(c.max())# 4
print(c.min())# 1
print(c.sum())# 10
print(c.mean())# 2.5
print(c.var())#1.25

'''axis=0 - column and axis=1 -rows'''
a=np.array([(1,2,3),(3,4,5)])
print(a.sum(axis=0))#[4 6 8]
print(a.sum(axis=1))#[ 6 12]

'''square root and standard deviation Both are genric function that's why its it will be written with np'''

print(np.sqrt(a))#[[1.         1.41421356 1.73205081][1.73205081 2.         2.23606798]]-- square root of each of the element
print(np.std(a))#1.2909944487358056 --standard deviation

 
'''Addition,subtraction,multiplication,division, vertical and horizontal stacking'''
a=np.array([(1,2,3),(3,4,5)])
b=np.array([(1,2,3),(3,4,5)])
print(a+b)#[[ 2  4  6]
#           [ 6  8 10]]
print(a*b)#[[ 1  4  9]
#           [ 9 16 25]]
 
print(a-b)#[[0 0 0]
#           [0 0 0]]
 
print(a/b)#[[1. 1. 1.]
#           [1. 1. 1.]]
 
print(np.vstack((a,b)))#[[1 2 3]
                        #[3 4 5]
                        #[1 2 3]
                        #[3 4 5]]
print(np.hstack((a,b)))#[[1 2 3 1 2 3]
#                        [3 4 5 3 4 5]]
 
print(a.ravel())#[1 2 3 3 4 5]-- this will print in single column
 
 
'''This is the format to read the file in NumPy'''
#data=np.loadtxt('data.txt',delimiter=',',dtype=np.int8,skiprow=1)
data=np.genfromtxt('input_data.txt', delimiter=',', dtype=None, names=('sepal length', 'sepal width', 'petal length', 'petal width', 'label','lebel'))
data=np.genfromtxt('input_data21.csv', delimiter=',', dtype=None, names=('sepal length', 'sepal width', 'petal length', 'petal width', 'label','lebel'))
print(data)
 
a = np.arange(30).reshape(5, 6)
print(a)#[[ 0  1  2  3  4  5]
         #[ 6  7  8  9 10 11]
         #[12 13 14 15 16 17]
         #[18 19 20 21 22 23]
         #[24 25 26 27 28 29]]
b = a>6
print(b)#[[False False False False False False]
         #[False  True  True  True  True  True]
         #[ True  True  True  True  True  True]
         #[ True  True  True  True  True  True]
         #[ True  True  True  True  True  True]]
          
'''In this we are giving a index of array a array itself a[b] if we do this we will get all the element which
is true/ element which is a>6 .This is the way of extracting element who is greater than 6 from our original array'''
 
print(a[b])#[ 7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29]
 
'''This is also useful when we want to replace anything with certain number'''
a[b]=-1
print(a)#[ 6 -1 -1 -1 -1 -1]
         #[-1 -1 -1 -1 -1 -1]
         #[-1 -1 -1 -1 -1 -1]
         #[-1 -1 -1 -1 -1 -1]]

