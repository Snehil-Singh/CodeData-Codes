import pandas as pd

"""Reading the csv file with Pandas Dataframe"""
df= pd.read_csv("C:\\Users\\rahul\\Desktop\\Practice\\PandasEx\\input1.csv",encoding='utf-8',index_col=0)
# print(df)

'''Use "split" with "str[0]" for select first lists and replace by datetime 
converted to strings by "Timestamp.strftime:"'''

now = pd.datetime.now().strftime('%d/%m/%Y')
df['Date/Time'] = df['Date/Time'].str.split(':').str[0].fillna(now)


'''Alternative is convert column "to_datetime", replace missing values 
to now and last convert it to strings by "Series.dt.strftime:"'''

df['Date/Time'] = (pd.to_datetime(df['Date/Time'], format='%d/%m/%Y').fillna(pd.datetime.now()).dt.strftime('%d/%m/%Y'))

'''this will give full date+time'''
# df1['Date/Time'] = (pd.to_datetime(df['Date/Time'], format='%d/%m/%Y').fillna(pd.datetime.now()).dt.strftime('%d/%m/%Y:%H:%M:%S'))

'''And then use "factorize" with "apply" for processes multiple columns:'''

cols = ['Name','Address','Email']
df[cols] = df[cols].apply(lambda x: pd.factorize(x)[0] + 1)
print (df)

'''writing in different csv file '''
df.to_csv("pandas.csv")
