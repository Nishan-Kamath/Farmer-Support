import os
import sqlite3
import pandas as pd
import requests
from flask import Flask, jsonify, redirect, render_template, request, session
from joblib import load
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load models once at startup
rf_model = load('rf_model.joblib')
lr_model = load('lr_model.joblib')
dt_model = load('dt_model.joblib')

# Global variable to store prediction data
data = None

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password))
    users = cursor.fetchall()
    connection.close()

    if len(users) > 0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return render_template('login.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    uname = request.form.get('uname')
    uemail = request.form.get('uemail')
    upassword = request.form.get('upassword')

    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user WHERE email=?", (uemail,))
    check_user = cursor.fetchall()
    if len(check_user) == 0:
        cursor.execute("INSERT INTO user(email, name, password) VALUES (?, ?, ?)", (uemail, uname, upassword))
        connection.commit()
        connection.close()
        return render_template('login.html')
    else:
        connection.close()
        return "Email Already Exists!"

@app.route('/set_crop')
def set_crop():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    global data,rainfall,temperature,humidity,ph
    rainfall = request.form.get("rainfall")
    temperature = request.form.get("temperature")
    ph = request.form.get("ph")
    humidity = request.form.get("humidity")

    try:
        # Convert inputs to floats
        prediction_data = [float(temperature), float(humidity), float(ph), float(rainfall)]

        # Load data for prediction
        df = pd.read_csv("cropdata.csv")
        new_df = df.copy()
        new_df.drop(columns=['N', 'P', 'K'], axis=1, inplace=True)
        x = new_df.drop(['label'], axis=1)
        y = new_df['label']

        # Predictions
        rf_pred = rf_model.predict([prediction_data])[0]
        lr_pred = lr_model.predict([prediction_data])[0]
        dt_pred = dt_model.predict([prediction_data])[0]

        # Determine final prediction
        if rf_pred == lr_pred or rf_pred == dt_pred:
            final_pred = rf_pred
        else:
            final_pred = lr_pred

        data = final_pred
        return render_template('prediction.html', temperature=temperature, humidity=humidity, ph=ph, rainfall=rainfall, data=final_pred)

    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('error.html', error_message=str(e))

@app.route('/get_crop', methods=['GET'])
def get_crop():
    global data
    if data is not None:
        return jsonify({'message': data})
    else:
        return jsonify({'message': 'No prediction available'})

@app.route('/show_crop')
def show_crop():
    global data
    return render_template('prediction.html', temperature=temperature, humidity=humidity, ph=ph, rainfall=rainfall, data=data)

@app.route('/set_whether')
def set_whether():
    return render_template('get_whether.html')

@app.route('/get_whether', methods=['POST'])
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

    return render_template('show_whether.html', desc=desc, temp=temp, name=name, humidity=humidity, sea_level=sea_level)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
