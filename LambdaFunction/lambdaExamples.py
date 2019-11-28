from _functools import reduce


"""  LAMBDA BY USING FILTER,MAP,REDUCE  """


# Normal Funnction
def square(a):
    return a*a 
res=square(6)

#lambda function for square of any number
f=lambda a : a*a
res=f(6)
print(res)#36

#Getting addition of two numbers with lambda function
f=lambda a,b : a+b
res=f(6, 5)
print(res)#11

#using normal func getting even no from list
def is_even(n):
    return n%2==0
nums = [3,5,2,6,7,9,8,4,2]
even = list(filter(is_even, nums))
print(even)#[2, 6, 8, 4, 2]

#by using lambda getting even numbers by fiter,map and reduce
nums = [3,5,2,6,7,9,8,4,2]
even = list(filter(lambda n:n%2==0, nums))
doubles = list(map(lambda n:n*2,even))
sum = reduce(lambda a,b:a+b,doubles)

print(even)#[2, 6, 8, 4, 2]
print(doubles)#[4, 12, 16, 8, 4]
print(sum)#44
print(reduce(lambda a,b:a+b,doubles))#44

#upercase
def uppercase(string):
    return string.upper()
values = ['abc','def','ghi']
print(list(map(uppercase,values)))#['ABC', 'DEF', 'GHI']
print(list(map(lambda x:x.upper(),values)))#['ABC', 'DEF', 'GHI']