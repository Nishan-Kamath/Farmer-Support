import os
import sqlite3
from flask import Flask, jsonify, redirect, render_template ,request, session
import pandas as pd
import numpy as np
import requests
import openai 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)
app.secret_key=os.urandom(24)


rainfall = ''
temperature = ''
ph = ''
humidity = ''
ques= ''
command = ''

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    connection = sqlite3.connect(database='user.db')
    cursor = connection.cursor()
    cursor.execute("select * from user where email=? and password=?",(email,password,))
    users = cursor.fetchall()
    global name ,mailId

    connection.close()


    if len(users)>0:
        name = users[0][1]
        mailId = users[0][0]

        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return render_template('login.html')
    

    
@app.route('/add_user',methods=['POST'])
def add_user():
    uname = request.form.get('uname')
    uemail = request.form.get('uemail')
    upassword = request.form.get('upassword')

    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()

    cursor.execute("select * from user where email=?",(uemail,))
    check_user = cursor.fetchall()
    print(check_user)
    #connection.close()
    if(len(check_user) == 0):
        cursor.execute("insert into user(email,name,password)values(?,?,?)",(uemail,uname,upassword,))
        connection.commit()
        connection.close()
        return render_template('login.html')
    else:
         connection.close()
         return "Email Already Exists!"
    
@app.route('/set_crop')
def set_crop():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    global rainfall ,temperature ,ph ,humidity
    rainfall = request.form.get("rainfall")
    temperature = request.form.get("temperature")
    ph = request.form.get("ph")
    humidity = request.form.get("humidity")

    prediction_data = [float(temperature),float(humidity),float(ph),float(rainfall)]

    df = pd.read_csv("C:\\Users\\Nishan Kamath\\Desktop\\2nd Year\\internship_project\\crop_yield_recommendation\\cropdata.csv")

    new_df = df.copy()
    new_df.drop(columns=['N','P','K'],axis=1,inplace=True)
    x = new_df.drop(['label'], axis=1)
    y = new_df['label']

    x_train,x_test,y_train,y_test = train_test_split(x, y, test_size=0.3)

    rf_model = RandomForestClassifier()
    rf_model.fit(x_train,y_train)

    lr_model = LogisticRegression(solver='liblinear')
    lr_model.fit(x_train,y_train)

    dt_model = DecisionTreeClassifier()
    dt_model.fit(x_train,y_train)

    prediction_data = [temperature,humidity,ph,rainfall]
    for i in range(len(prediction_data)):
        prediction_data[i] = float(prediction_data[i])

    rf_pred = rf_model.predict([prediction_data])
    lr_pred = lr_model.predict([prediction_data])
    dt_pred = dt_model.predict([prediction_data])

    for i in rf_pred:
        rf_pred = str(i)

    for i in lr_pred:
        lr_pred = str(i)

    for i in dt_pred:
        dt_pred = str(i)

    final_pred = 0

    if(rf_pred == lr_pred or rf_pred == dt_pred):
        final_pred = rf_pred
    else:
        final_pred = lr_pred

    global data
    data = final_pred
    return render_template('prediction.html',temperature=temperature,humidity=humidity,ph=ph,rainfall=rainfall,data=data)

@app.route('/get_crop', methods=['GET'])
def get_crop():
    data = {'message': data}
    return jsonify(data)

@app.route('/show_crop')
def show_crop():
    return render_template('prediction.html',temperature=temperature,humidity=humidity,ph=ph,rainfall=rainfall)

@app.route('/set_whether')
def set_whether():
    return render_template('get_whether.html')

@app.route('/get_whether',methods=['POST'])
def get_whether():
    city = request.form.get('city')
    api_key = 'b1693ed7ad181ad79817cc99d0523aa3'  # Replace with your actual API key
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    desc = data['weather'][0]['description']
    temp = data['main']['temp']
    name = data['name']
    humidity = data['main']['humidity']
    sea_level = data['main']['sea_level']

    return render_template('show_whether.html',desc=desc,temp=temp,name=name,humidity=humidity,sea_level=sea_level)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
