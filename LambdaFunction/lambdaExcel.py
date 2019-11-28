import csv
from openpyxl import Workbook
from pandas import DataFrame

wb=Workbook()
ws=wb.active

def main():
    with open('input_data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        
        nameList = []
        isSeniorList = []
        scoreList = []
        
        for row in reader:
            if(len(row) == 0):
                continue;
                
            print(row[0],row[1],(int(row[3]) + int(row[4]) + int(row[5])))
            
            Age = int(row[2]) #Parse the sting to integer
            isSenior = 'No'
            if(Age > 10):
                isSenior = 'Yes'
#                
            Name = row[0] + ' ' + row[1]
            studentScore = int(row[3]) + int(row[4]) + int(row[5])
            
            nameList.append(Name)
            isSeniorList.append(isSenior)
            scoreList.append(studentScore)
        
        df = DataFrame({'Name': nameList, 'Is Senior': isSeniorList, 'Score': scoreList})
        df.to_excel('test.xlsx', sheet_name='sheet2', index=False)
        
#         ws.append(finalList)
#         wb.save('dev.xlsx')
            
#             d=ws.cell(row=4,column=3, value=Age)
    
main()