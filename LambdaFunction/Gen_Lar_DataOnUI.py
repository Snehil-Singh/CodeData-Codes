import random
import string
import sys
import argparse
import os
import csv
from pandas import DataFrame
from flask import Flask, render_template, request,Response, redirect, make_response

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

tempFile =""

#defined the flask route
@app.route("/")
def index():
    print("Loading the root file")
    return render_template("uploadFIle.html")

@app.route("/uploadFile", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'metadata/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
        
    global recordCount
    recordCount = request.values.get("records")
   
    for file in request.files.getlist("source_fileName"):
        print(file)
        filename = file.filename
        
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        global tempFile
        tempFile = destination
        print("tempFile - " + tempFile)
        
    #define global scope and reference it
    global destination_fileName
    destination_fileName = request.form.get('target_fileName')
    return redirect("/compute", )

@app.route("/compute")
def compute():
    print("Start")
    num_rec=[]
    num_recuser=[]
    
    #The argparse module makes it easy to write user-friendly command-line interfaces
    parser = argparse.ArgumentParser()
    
    #Filling an ArgumentParser with information about program arguments is done by making calls to the add_argument() method. 
    parser.add_argument("-i", dest = "metadata_file",default=tempFile, help="full path to metadata file")
    parser.add_argument("-f", dest = "file_name", default='data_feed2.csv', help="output feed file name")
    parser.add_argument("-nrec", dest = "num_rec",default=num_rec, help="number of records")
    parser.add_argument("-nreca", dest = "num_recuser",default=num_recuser, help="number of records")
    parser.add_argument("-d", dest = "delimiter", default=',', help="field delimiter")
    parser.add_argument("-hdr", dest = "header_req", default='Y', help="Y if header is required otherwise N")
    
    #ArgumentParser parses arguments through the parse_args() method.
    args = parser.parse_args()    
    metadata_file = args.metadata_file
    file_name = args.file_name
    delimiter = args.delimiter
    header_req = args.header_req.upper()
    num_rec=int(recordCount)
    num_recuser = 3
    
    #Raise error if metadata is not passed in Parameter
    if not (metadata_file):
        parser.print_help()
        sys.exit()
    
    record = ''
    record_type=[]
    field_type=[]
        
    with open(metadata_file) as metadata:
        reader = csv.reader(metadata)
        j=0
        for row in reader:
            field_type=[]
            if j>0:
                field_type.append(row[0])
                field_type.append(row[1])
                field_type.append(row[2])
                field_type.append(row[3])
                field_type.append(row[4])
                field_type.append(row[5])
                
                record_type.append(field_type)
            j+=1
            
    print("Generating the Feed File Named "+file_name+" With "+str(len(record_type))+" Columns and Delimiter = "+delimiter)    
    
    records=[]
    header=''
    if header_req == 'Y':
        for rec in record_type:
            header=header+rec[0]+delimiter
        header=header[:len(header)-1]+"\n"
        records.append(header)
    
    for i in range(num_rec):
        record=''
        for rec in record_type:
            record= record+getData(rec[1],rec[2],rec[num_recuser])+delimiter
        record=record[:len(record)-1]+"\n"
        records.append(record)
        print("record-",record )
    print("File "+file_name+" Generated Successfully")
    return Response(records, content_type="text/csv", headers={ "Content-Disposition": "attachment;filename=data.csv"}) 

def getData(p_dataType, p_length, p_type):
    value =''
    dataType = p_dataType.upper()
    length=int(p_length)
    type=p_type.upper()
    if 'INT' in dataType or 'NUM' in dataType:
        if type == 'FIXED':
            return ''.join(random.choice(string.digits) for _ in range(length))
        else:
            length=random.randint(1,length)
            return ''.join(random.choice(string.digits) for _ in range(length))
        
    elif 'CHAR' in dataType or 'STR' in dataType:
        if type == 'FIXED':
            return ''.join(random.choice(string.ascii_uppercase))+''.join(random.choice(string.ascii_lowercase) for _ in range(length-1))
        elif type != 'FIXED' and len(type)>0:
            return ''.join(random.choice(type.split(",")))
        else:
            length=random.randint(0,length)
            return ''.join(random.choice(string.ascii_uppercase))+''.join(random.choice(string.ascii_lowercase) for _ in range(length-1))
    
if __name__ == '__main__':
    app.run(debug=True)


