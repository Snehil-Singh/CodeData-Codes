import os

import pymysql # to communicate with database
from flask import Flask, render_template, request,Response, redirect, make_response
from openpyxl import Workbook
    
import csv
from pandas import DataFrame


#defined the flask app
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

tempFile = ""
destination_fileName = ""
tar_file = ""
source_file = ""

#defined the flask route
@app.route("/")
def index():
    print("Loading the root file")
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload():
    '''
        Check for the source and target and invoke the actions accordingly
    '''
    source_op = request.form.get('Source')
    target_op = request.form.get('Target')
    
    if source_op == 'File':
        target = os.path.join(APP_ROOT, 'csvfile/')
        print(target)
    
        if not os.path.isdir(target):
            os.mkdir(target)
    
        for file in request.files.getlist("source_fileName"):
            print(file)
            filename = file.filename
            
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
            global tempFile
            tempFile = destination
            print("tempFile - " + tempFile)
        
    if target_op == 'File':
        #define global scope and reference it
        global destination_fileName
        destination_fileName = request.form.get('target_fileName')
        
    if (source_op == 'File'): 
        return applyLambdaOnFiledataAndPushToTarget(target_op)
    
    if (source_op == 'Database'):
        return applyLambdaOnDBdataAndPushToTarget(target_op)
    
""" Uses Lambda expressions for evaluation """
    
Name_lambda_function = lambda x, y: x + ' ' + y
Is_Senior_lambda_function = lambda x: x > 10 
studentScore_lambda_function = lambda x, y, z: x + y + z 

def applyLambdaOnFiledataAndPushToTarget(target_op):
    '''
    This method holds the logic for reading the contents of the file
    and apply lambda functions and store the result to target file(database). 
    '''
    with open(tempFile, 'r') as csvfile:
        readerForRowCheck = csv.reader(csvfile, delimiter=',')
         
        for row in readerForRowCheck:       
            if (len(row) != 6):
                return render_template("incomplete.html")
 
            #We will parse only when there are 6 columns and minimum one row
            headerColumn1 = row[0];
            headerColumn2 = row[1];
            headerColumn3 = row[2];
            headerColumn4 = row[3];
            headerColumn5 = row[4];
            headerColumn6 = row[5];
             
            if (headerColumn1 != "firstname") or (headerColumn2 != "lastname") \
                or (headerColumn3 != "Age") or (headerColumn4 != "Maths")or (headerColumn5 != "Science") \
                or (headerColumn6 != "English"):
                return render_template("incomplete.html")        
            break;
         
        nameList = []
        isSeniorList = []
        scoreList = []
         
        for row in readerForRowCheck:
            if(len(row) == 0):
                continue;
                 
            print(row[0],row[1],(int(row[3]) + int(row[4]) + int(row[5])))
             
            Age = int(row[2]) #Parse the sting to integer
            
#             isSenior = 'No'
#             if(Age > 10):
#                 isSenior = 'Yes'

            
            Is_Senior = Is_Senior_lambda_function(Age)
            Name = Name_lambda_function(row[0],row[1])
            studentScore =studentScore_lambda_function(int(row[3]), int(row[4]), int(row[5]))
               
#             Name = row[0] + ' ' + row[1]
#             studentScore = int(row[3]) + int(row[4]) + int(row[5])
             
            nameList.append(Name)
            isSeniorList.append(Is_Senior)
            scoreList.append(studentScore)
             
        df = DataFrame({'Name': nameList, 'Is_Senior': isSeniorList, 'Score': scoreList})
         
        if(target_op == 'File'):

            resp = make_response(df.to_csv(index=False))
            resp.headers["Content-Disposition"] = "attachment; filename="+destination_fileName
            resp.headers["Content-Type"] = "text/csv"
            return resp
        else:
            conn = pymysql.connect(host="localhost",user="root",password="root",db="sqlPython")
            tempCursor = conn.cursor()
 
            # Create the INSERT INTO sql query
            query = "INSERT INTO target_table(Name, Is_Senior, Score) VALUES (%s, %s, %s)"
         
            # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
            for index, row in df.iterrows():
                print (row['Name'])
                values = (row['Name'], row['Is_Senior'], row['Score'])
                print(values)
                 
                # Execute sql Query
                tempCursor.execute(query, values)
 
            # Close the cursor
            tempCursor.close()
 
            # Commit the transaction
            conn.commit()
 
            # Close the database connection
            conn.close()
            return render_template("complete.html")
             

def applyLambdaOnDBdataAndPushToTarget(target_op):
    '''
    This method holds the logic for reading the contents of the database
    and apply lambda functions and store the result to the database. 
    '''

    wb=Workbook()
    ws=wb.active
    conn = pymysql.connect(host="localhost",user="root",password="root",db="sqlPython")
    tempCursor = conn.cursor()
    sql = "select * from Source_table"
    tempCursor.execute(sql)
    countrow= tempCursor.execute(sql)
    print("Number of rows:",countrow)
    readerForRowCheck=tempCursor.fetchall()
    for row in readerForRowCheck:
        ws.append(row)


    nameList = []
    isSeniorList = []
    scoreList = []
         
    for row in readerForRowCheck:
        if(len(row) == 0):
            continue;
                 
        print(row[0],row[1],(int(row[3]) + int(row[4]) + int(row[5])))
        
        #Parse the sting to integer
        """ This is another way of getting the evalution other than using Lambda function"""
             
#         Age = int(row[2]) 
#         Is_Senior = 'No'
#         if(Age > 10):
#             Is_Senior = 'Yes'
#                 
#         Name = row[0] + ' ' + row[1]
#         studentScore = int(row[3]) + int(row[4]) + int(row[5])

        """ Invoking Lambda function"""
        
        Is_Senior = Is_Senior_lambda_function(Age)
        Name = Name_lambda_function(row[0],row[1])
        studentScore =studentScore_lambda_function(int(row[3]), int(row[4]), int(row[5]))
        
        nameList.append(Name)
        isSeniorList.append(Is_Senior)
        scoreList.append(studentScore)
             
          
    df = DataFrame({'Name': nameList, 'Is_Senior': isSeniorList, 'Score': scoreList})
    if(target_op == 'File'):
        resp = make_response(df.to_csv(index=False))    
        resp.headers["Content-Disposition"] = "attachment; filename="+destination_fileName
        resp.headers["Content-Type"] = "text/csv"
        return resp
    else:
        conn = pymysql.connect(host="localhost",user="root",password="root",db="sqlPython")
        tempCursor = conn.cursor()
 
        # Create the INSERT INTO sql query
        query = "INSERT INTO target_table(Name, Is_Senior, Score) VALUES (%s, %s, %s)"
         
        # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
        for index, row in df.iterrows():
            print (row['Name'])
            values = (row['Name'], row['Is_Senior'], row['Score'])
            print(values)
                 
                # Execute sql Query
            tempCursor.execute(query, values)
 
            # Close the cursor
        tempCursor.close()
 
            # Commit the transaction
        conn.commit()
 
            # Close the database connection
        conn.close()
        return render_template("complete.html")

@app.route("/compute")
def compute():
    print("tempFile - " +tempFile )
    with open(tempFile, 'r') as csvfile:
        readerForRowCheck = csv.reader(csvfile, delimiter=',')
            
        #Check for header content and return if invalid
        for row in readerForRowCheck:       
             
             
            if (len(row) != 6):
                return render_template("incomplete.html")
 
            #We will parse only when there are 6 columns and minimum one row
            headerColumn1 = row[0];
            headerColumn2 = row[1];
            headerColumn3 = row[2];
            headerColumn4 = row[3];
            headerColumn5 = row[4];
            headerColumn6 = row[5];
             
             
            if (headerColumn1 != "firstname") or (headerColumn2 != "lastname") or (headerColumn3 != "Age") or (headerColumn4+headerColumn5+headerColumn5 != "studentScore"):
                return render_template("incomplete.html")        
            break;
         
        nameList = []
        isSeniorList = []
        scoreList = []
         
        for row in readerForRowCheck:
            if(len(row) == 0):
                continue;
                 
            print(row[0],row[1],(int(row[3]) + int(row[4]) + int(row[5])))
            
            #Parse the sting to integer 
            Age = int(row[2]) 
            Is_Senior = 'No'
            if(Age > 10):
                Is_Senior = 'Yes'
                
            Name = row[0] + ' ' + row[1]
            studentScore = int(row[3]) + int(row[4]) + int(row[5])
             
            nameList.append(Name)
            isSeniorList.append(isSenior)
            scoreList.append(studentScore)
             
          
        df = DataFrame({'Name': nameList, 'Is_Senior': isSeniorList, 'Score': scoreList})
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename="+destination_fileName
        resp.headers["Content-Type"] = "text/csv"
        return resp
    
        return Response( df, content_type="text/csv", headers={ "Content-Disposition": "attachment;filename=dev.csv"})
             
              

if __name__ == "__main__":
    app.run(debug=True)
#     app.run(port=4555, debug=True)