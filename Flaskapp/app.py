from flask import Flask,render_template, request, redirect
from wtforms import Form, StringField, PasswordField, validators
import mysql.connector
import yaml
from wtforms.validators import email
from django.conf.global_settings import SECRET_KEY

#Instantiate an object for Flask class
app = Flask(__name__)
db =yaml.load(open('db.yaml')) #loads all the config. file required to connect DB
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
app.config['MYSQL_CURSORCLASS']= "DictCursor"
 
mydb=mysql.connector.connect(
    host=db['mysql_host'],
    user=db['mysql_user'],
    passwd=db['mysql_password'],
    database=db['mysql_db'])
 
#create route to handle request on the server       
@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
      
        userDetails = request.form  #fetching the form details
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']
        cur = mydb.cursor() #making connection with MySQL db using cursor.
        cur.execute("insert into Employees_Detail(username, email, password)values(%s, %s, %s)",(username, email, password))
        mydb.commit() #commit on the database
        cur.close()
        return redirect('/users') 
    return render_template('index.html')
 
@app.route('/users') #fetching all the details from the db and display on web browser
def users():
    cur = mydb.cursor()
    userDetails = cur.execute("select * from Employees_Detail")# executing a query to fetch all the rows
    userDetails = cur.fetchall()
     
    if len(userDetails) > 0: # if return rows are greater. then store the details in userDetail        
        return render_template('users.html',userDetails=userDetails)
    return render_template('register.html')

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']
        
        # Create cursor
        cur = mydb.cursor()

#      Execute query
        cur.execute("INSERT INTO Employees_Detail(username, email, password) VALUES(%s, %s, %s)", ( username, email, password))

        # Commit to DB
        mydb.commit()
        cur.close()
        return redirect('/users')
    return render_template('register.html', form=form)
    
     
# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password = request.form['password']
        
        cur = mydb.cursor()
        cur.execute("SELECT * FROM Employees_Detail WHERE username = %s and password = %s", [username, password])
        userDetails = cur.fetchone()
        if userDetails is not None and len(userDetails) > 0:
            return redirect('/users')
    return render_template('login.html')

if __name__ == '__main__':
    secret_key = "123345353543"

    app.run(debug=True,port=8081)
