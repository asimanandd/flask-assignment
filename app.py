import json
from flask import Flask, request, render_template
from flask import jsonify
from datetime import datetime
from pymongo import MongoClient
import certifi
from werkzeug.security import generate_password_hash

app = Flask(__name__)

MONGO_URI = "mongodb+srv://asimanand501_db_user:NtFvpfTNZxNAyDc2@cluster0.yybqri7.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = client["flask_tutorial"]     # database name
users_collection = db["users"] 


@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')

    return render_template('index.html', day_of_week=day_of_week)

@app.route('/api')
def api():
    with open('data.json') as f:
        data=json.load(f)
    return jsonify(data)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description,
        "createdAt": datetime.utcnow()
    }

    db.todo_items.insert_one(todo_item)

    return "To-Do Item Submitted Successfully"



@app.route('/age')
def name():
    name = request.values.get('name')
    age = request.values.get('age')
    age = int(age)
    if age >18:
        return 'Welcome to the Site, ' + name + "!"
    else:
        return "Sorry, you are too young to use this site!"

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Basic validation
    if not name or not email or not password or not confirm_password:
        return "Please fill all fields!", 400

    if password != confirm_password:
        return "Passwords do not match!", 400

    # Hash the password before saving
    hashed_password = generate_password_hash(password)

    # Insert into MongoDB
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

    return f"Hello {name}, signup successful! Data saved to MongoDB."


if __name__ == '__main__':
    app.run(debug=True)


