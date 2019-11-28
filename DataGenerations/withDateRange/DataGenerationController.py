# import logging
from io import StringIO   
import pandas as pd
import numpy as np
import random
import os
import logging.config
from random import randint
from flask import Flask, render_template, request, redirect, make_response
import json
from botocore.client import Config
import boto3
import functools
# from flask.logging import default_handler
from datetime import datetime

ACCESS_KEY_ID = 'AKIAIGVTZC3DHUARWKUA'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'codas3bucket'

fp = open('..\\withDateRange\\config\\logging.json')
logging.config.dictConfig(json.load(fp))
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger("__name__")
# logger.removeHandler(default_handler)
fp.close()

def exception(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in "
            err += function.__name__
            logger.exception(err)
            # re-raise the exception
            raise
    return wrapper
app = Flask(__name__)
 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

'''This commented line is for the INI file which is named as "logging.ini" '''
#
tempFile =""
@app.route("/")
def index():
    startTime = datetime.now()
#     print(logging.Logger.manager.loggerDict.keys())
    '''
    This is invoked when the application launches. We will load the UploadFile.html file.
    '''
    logger.info("Loading the Home page for generating large set of data")
    logger.debug("Total Time Taken to Load the Home page- " + format(datetime.now() - startTime))
    return render_template("UploadFile.html")
 
@app.route("/UploadFile", methods=['POST'])
def upload():
    startTime = datetime.now()
    '''
    This method uploads the file from the browser to the server for processing.
    '''
    
    global targetLocation
    targetLocation = request.form.get("target")
    print("targetLocation-",targetLocation)
    
    logger.info("File upload operation initiated")
    
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())
    logger.debug('Request Arguments: %s',request.values)
    
    '''
    In target we store the csv file in a folder name called 'InputFile' 
    if not found will create it with same name 
    '''
    target = os.path.join(APP_ROOT, 'input/')
 
    if not os.path.isdir(target):
        os.mkdir(target)
    
    global sourceHeader
    sourceHeader = request.values.getlist("sourceHeaderFields")
    print("sourceHeader-",sourceHeader)
    
    global targetHeader
    targetHeader = request.values.getlist("targetHeaderFields")
    print("targetHeader-",targetHeader)
        
    ''''recordCount' will take the input from the user for dataGeneration"'''  
    global recordCount
    recordCount = int(request.values.get("records"))
    
    global fromYear
    fromYear = int(request.values.get("fromYear"))
     
    global toYear
    toYear = int(request.values.get("toYear"))
    
    # "abs_path_list" is path of files uploaded with the file name
    abs_path_files=[]  
    for file in request.files.getlist("source_fileName"):
#         print("file-",file)
        filename = file.filename
#         print("filename-",filename)
         
        destination = "/".join([target, filename])
#         print("destination-",destination)
        
        file.save(destination)
#         print("file--",file)
        logger.debug("File saved to destination folder")
        tempFile = os.path.abspath(destination)
        abs_path_files.append(tempFile)
        print("abs_path_files - " ,abs_path_files)
        global files_list
        files_list=abs_path_files
        print("files_list-",files_list)  
#         global tempFile
#         tempFile = destination
#         print("tempFile-",tempFile)
        
    global destination_fileName
    destination_fileName = request.form.get('target_fileName')
#     print("destination_fileName-",destination_fileName)
    
#     s3 = boto3.resource('s3',
#     aws_access_key_id=ACCESS_KEY_ID,
#     aws_secret_access_key=ACCESS_SECRET_KEY,
#     config=Config(signature_version='s3v4'))
#      
#     s3.Bucket(BUCKET_NAME).put_object(Key="DataLarge1.csv",Body =request.files['source_fileName'])
#     
    logger.info("File upload operation completed")
    logger.debug("TOtal Time Taken for upload operation- " + format(datetime.now() - startTime))
    return redirect("/compute", )
 
def segment():
    startTime = datetime.now()
    logger.info("Segmentation process started")
    '''
    This will break the record count into segments based on the years selected. 
    Later we will split the individual value to 12 random segments 
    (12 indicates months).
    '''
    partitions = 12
    
    assert recordCount >= partitions >= 1
     
    segmentValues = []
    
    """This for loop will break the record count into segments"""
    for idx in range(partitions-1):
        segmentValues.append(randint(1,recordCount-sum(segmentValues)-partitions+idx))
        
    """This 'segmentValues' contains the segments which is divided randomly in a 12 parts""" 
    segmentValues.append(recordCount-sum(segmentValues))
    
    """randamize the segmentValues"""
    random.shuffle(segmentValues)
    logger.debug("segmentValues - " +format(segmentValues))
    logger.info("segmentation process completed")
    logger.debug("TOtal Time Taken for Segmentation process- " + format(datetime.now() - startTime))
    return segmentValues

def LocalBrowse(result):
    
    resp = make_response(result.to_csv(index=False,))
    resp.headers["Content-Disposition"] = "attachment; filename=OutputData.csv"
    resp.headers["Content-Type"] = "text/csv"
    print("resp-",resp)
    return resp
#     return "done"

def s3Bucket(result):
    
    csv_buffer = StringIO()
    result.to_csv(csv_buffer,index=False)
    s3_resource = boto3.resource('s3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4'))
    bucket=s3_resource.Bucket(BUCKET_NAME)
    
    # It will search for the "unprepared" Folder on s3 if it is not there it will create a newFolder with same name
    bucket.Object('unprepared/OutputData.csv').put(Body=csv_buffer.getvalue())
    return "<h1> File saved to s3 on path-'unprepared/OutputData.csv' <h1>" 
        

@app.route("/compute")
def compute():
    startTime = datetime.now()
    logger.info("Data generation process started")
    """We will get the random number of the  data on specified input"""
    
    dataFrames=[]
    #"f" contains the data absolute files path
    for files in files_list:
        print("files-",files)
        dataFrame=pd.read_csv(files)
#         print("dataFrame-",dataFrame)
        dataFrames.append(dataFrame)
#         print("dataFrames-",dataFrames)
    col_in_files = set([",".join(list(f.columns.values)) for f in dataFrames])
    if len(col_in_files)!=1:
        return render_template("Incomplete.html")
#         return "<h1>Columns are Not Same Please Choose the Correct File and Upload Again</h1>"
    else:
        """Here we are getting YearRange From user"""
        Year_Array=[]
        
        """We are getting the 'fromYear' and 'toYear'range from the user 
        and populate data for the all the years within the range""" 
        for val in range(fromYear, toYear+1):
            Year_Array.append(val)
             
        logger.debug("Year Array - " + format(Year_Array))
         
        Month_Array=['Jan','Feb','Mar','April','May','June','July','Aug','Sep','Oct','Nov','Dec']
        final_Array=[]
        
        global recordCount
        recordCount = recordCount / len(Year_Array)
        
        """ Reading a csv file which is selected by the user for selected Header Columns"""
        df1=dataFrame[targetHeader]
        logger.info("Loaded the file to memory for generating the data for selected Header Columns")
        
        """We are getting the 'Year_Array' and iterating it till specified year"""
        for YrCount in range(0, len(Year_Array), 1):
            MonthCount = 0
            
            """Invoking the segment function """
            seg = segment()
            for i in range(0,len(seg), 1):
                """'SegValue' contains the first number of the segment at the first time of the loop"""
                SegValue=seg[i]
                         
                for j in range(0, int(SegValue) , 1):
                    num=randint(0, len(df1)-1)
                    row=df1.iloc[num]
                    
                    values = [Year_Array[YrCount], Month_Array[MonthCount]]
                    for k in range(0, len(targetHeader)):
                        values.append(row.get(targetHeader[k]))
                        
                    """'final_Array' contains the specified columns and data in a random order"""
                    final_Array.append(values)
#                     final_Array.append(((Year_Array[YrCount], Month_Array[MonthCount],row.get("Asset_Id"),row.get("Asset Family"),row.get("Asset Name"),row.get("Location"),row.get("Asset Component"),row.get("Keywords"),row.get("Conditions"),row.get("Parts"))))
                MonthCount += 1
    
    logger.debug("converting 'final_Array' into a DataFrame")        
    """Here we are converting a 'final_Array' into a DataFrame"""
    data = pd.DataFrame(final_Array)
    
    """Adding column 'SR_ID' to dataframe which acts a sequence number """
    data['SR_ID'] = 'SR' + pd.Series(np.arange(1, len(data.index) + 1)).astype(str).str.zfill(4)
    
    tempColumns = ['Year', 'Month']
    tempColumns.extend(targetHeader)
    tempColumns.append('SrID')
    data.columns = tempColumns
    #Here we are converting the dataframe into list for rearranging the columns
    cols = data.columns.tolist()
    
    #"SrID" is rearranged to the 1st position
    cols.insert(0, cols.pop(cols.index('SrID')))
    result = data.reindex(columns= cols)
#     data.columns = ['Year', 'Month', 'Asset_Id ', 'Asset Family', 'Asset Name', 'Location', 'Asset Component', 'Keywords', 'Conditions', 'Parts','SR_ID']
#     result = data[['SR_ID','Year', 'Month', 'Asset_Id ', 'Asset Family', 'Asset Name', 'Location', 'Asset Component', 'Keywords', 'Conditions', 'Parts']]
    
    if targetLocation == 'BrowserDownload':
        return LocalBrowse(result)
    else:
        return s3Bucket(result)
    
#     csv_buffer = StringIO()
#     result.to_csv(csv_buffer,index=False)
#     s3_resource = boto3.resource('s3',
#     aws_access_key_id=ACCESS_KEY_ID,
#     aws_secret_access_key=ACCESS_SECRET_KEY,
#     config=Config(signature_version='s3v4'))
#     bucket=s3_resource.Bucket(BUCKET_NAME)
#     bucket.Object('NewFolder/GeneratedData.csv').put(Body=csv_buffer.getvalue())
# 
#     logger.info("Data created in memory and started writing it to output file")
# #     resp = make_response(result.to_csv(index=False))
# #     resp.headers["Content-Disposition"] = "attachment; filename=OutputData.csv"
# #     resp.headers["Content-Type"] = "text/csv"
#     logger.info("Data generation process completed")
#     logger.debug("TOtal Time Taken for Data generation process- " + format(datetime.now() - startTime))
#     
#     return render_template("complete.html")
#     return resp

     
if __name__ == '__main__':
    app.run(debug=True)