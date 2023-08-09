from flask import Flask, url_for, request, redirect, session
from flask.templating import render_template
from flask_mysqldb import MySQL
import mysql.connector 
from mysql.connector import Error
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapp'

mysqll = MySQL(app)

connection = mysql.connector.connect(host = 'localhost', database = 'crudapp', user = 'root', password= '')
cursor = connection.cursor()
if connection.is_connected():
    print("Connected to MySQL Server version 11")

else:
    print("Error while connecting to MySQL 11")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    user = "check"
    error = None
    connection = mysql.connector.connect(host = 'localhost', database = 'crudapp', user = 'root', password= '')
    cursor = connection.cursor()
    if connection.is_connected():
        print("Connected to MySQL Server version 33")
    else:
        print("Error while connecting to MySQL33")
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor.execute("SELECT * FROM register WHERE Username=%s", (name,))
        user = cursor.fetchone()
        if user:
            if password == user[2]:
                session['user'] = user[1]
                connection.commit()
                cursor.close()
                return redirect(url_for('dashboard'))
            else:
                error = "Password did not match, Try again."
        else:
            error = 'Username or password did not match, Try again.'
            connection.commit()
            cursor.close()
    return render_template('login.html', loginerror = error, user = user)

@app.route('/register', methods=["POST", "GET"])
def register():
    connection = mysql.connector.connect(host = 'localhost', database = 'crudapp', user = 'root', password= '')
    cursor = connection.cursor()
    if connection.is_connected():
        print("Connected to MySQL Server version 22")
    else:
        print("Error while connecting to MySQL22")
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor.execute("SELECT * FROM register WHERE Username=%s", (name,))
        existing_username = cursor.fetchone()
        if existing_username:
            connection.commit()
            cursor.close()
            return render_template('register.html', registererror = 'Username already taken , try different username.')
        else:
            #print("tt")
            cursor.execute("INSERT INTO register ( Username, Password) VALUES (%s, %s)",(name, password))
            connection.commit()
            cursor.close()
        print(existing_username)
        return redirect(url_for('dashboard'))
    return render_template('register.html', user = register)
    
    

@app.route('/dashboard')
def dashboard():
    connection = mysql.connector.connect(host = 'localhost', database = 'crudapp', user = 'root', password= '')
    cursor = connection.cursor()
    if connection.is_connected():
        print("Connected to MySQL Server version 44")
    else:
        print("Error while connecting to MySQL44")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM booking")        
    # connection.commit()
    # cursor.close()
    # con= mysqll.connection.cursor()
    # con.execute()
    data = cursor.fetchall()
    # connection.commit() 
    cursor.close()
    #print(data)
    return render_template('dashboard.html', data = data)




@app.route('/singlecustomer/<string:name>')
def singlecustomer(name):
    user = "check"
    error = None
    connection = mysql.connector.connect(host = 'localhost', database = 'crudapp', user = 'root', password= '')
    cursor = connection.cursor()
    if connection.is_connected():
        print("Connected to MySQL Server version 55")
    else:
        print("Error while connecting to MySQL55")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM booking WHERE Username=%s", (name,))      
    single_emp =  cursor.fetchone()
    print(single_emp)
    print(name)
    return render_template('singlecustomer.html', single_emp = single_emp)



def check_signed_in():
    if 'user' in session:
        return True
    else:
        return False

@app.route('/addnewemployee', methods = ["POST", "GET"])
def addnewemployee():
    # check if the user is signed in
    if not check_signed_in():
        return redirect('/login')

    connection = mysql.connector.connect(host = 'localhost', database = 'crudapp', user = 'root', password= '')
    cursor = connection.cursor()
    if connection.is_connected():
        print("Connected to MySQL Server version ")        
    else:
        print("Error while connecting to MySQL")
     
    if request.method == "POST":
        Name = request.form['name']
        Username = request.form['email']
        Phone = request.form['phone']
        Address = request.form['address']

        journey_prices = {
        "Dundee-Portsmouth": 100,
        "Bristol-Manchester": 60,
        "Bristol-Newcastle": 80,
        "Bristol-Glasgow": 90,
        "Bristol-London": 60,
        "Manchester-Southampton": 70,
        "Cardiff-Edinburgh": 80
        }
        default_price = 75
        business_class_multiplier = 2
        

        route = request.form['flight']
        route_details = route.split('/')
        Journey = route_details[0]
        start_location = route_details[0].split('-')[0]
        start_time = route_details[1].split('-')[0]
        end_location = route_details[0].split('-')[1]
        end_time = route_details[1].split('-')[1]
        seat_type = request.form["seat"]
        print(start_location)
        print(end_location)
        print(start_time)
        print(end_time)

        if Journey in journey_prices:
            fare = journey_prices[Journey]
        else:
            fare = default_price
        
        if seat_type == "bClass":
            fare *= business_class_multiplier
            seat_type = "Business Class"

        else:
            seat_type= "Economy Class"
        print(fare)
        by_who = session['user'] 
        print(by_who)
        #cur = mysqll.connection.cursor()

        #connection.execute("SELECT * FROM booking")
        #query = ()
    
        cursor.execute("INSERT INTO booking (Username, Name, Phone, Address,Departure, Arrival, StartAt, EndAt, Admin,class, price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Username, Name, Phone, Address, start_location, end_location, start_time, end_time, by_who, seat_type, fare))
        
        connection.commit()

        cursor.close()
        return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html')
    

def logout():
    session.pop('user', None)
    render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug = True)
