import datetime
import os
import csv
import pandas as pd
from flask import Flask, render_template, request,Response, redirect, make_response
from _cffi_backend import string

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

tempFile = "nyc-jobs.csv";
fields = [] 
rows = [] 

#defined the flask route
@app.route("/")
def index():
    print("Loading the root file")
    return render_template("uploadFIle.html")

@app.route("/uploadFile", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'csvfile/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
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

    with open(tempFile, 'r',encoding="utf8") as csvfile:
        # creating a csv reader object 
        reader = csv.DictReader(csvfile, delimiter=',')
    # next(reader, None)
    
        '''We then restructure the data to be a set of keys with list of values {key_1: [], key_2: []}:'''        
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
                    
        '''Next we want to give each value in each list a unique identifier.'''            
        # Loop through all keys
        for key in data.keys():
            values = data[key]
                 
            things = list(sorted(set(values), key=values.index))
                 
            for i, x in enumerate(data[key]):
                if key==("Title Code No") or key==("Salary Range From") or key==("Salary Range To") or key==("Job ID"):
                    continue
                if data[key][i] == "":
                    data[key][i] = datetime.datetime.now().isoformat()
                if key==("Posting Date") or key==("Posting Updated") or key==("Process Date") or key == ("Post Until"):
                    data[key][i] = data[key][i][0:10]
                else:
                    data[key][i] = things.index(x) + 1
    
    """Since csv.writerows() takes a list but treats it as a row, we need to restructure our 
        data so that each row is one value from each list. This can be accomplished using zip():"""
                
    with open('data_cleansing.csv', "w") as outfile:
        writer = csv.writer(outfile)
        # Write headers
        writer.writerow(data.keys())
        # Make one row equal to one value from each list
        rows = zip(*data.values())
        # Write rows
        writer.writerows(rows)
    
    return render_template("complete.html")

if __name__ == "__main__":
    app.run(debug=True)