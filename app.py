import os
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request,redirect,flash
from dotenv import load_dotenv, dotenv_values


load_dotenv()

db = os.getenv('DB')
secret_key = os.getenv('SECRET_KEY')

client = MongoClient(db)
db = client['usuarios']
colection = db['users']

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        user = request.form['usuario']
        password = request.form['senha']

        users = {
            'name': user,
        }

        usuario = colection.find_one(users)
        print(usuario)
        if usuario:
            if usuario['password'] == password:
                return redirect(url_for('home'))
            
            else:
                flash('Senha invalida')
                return render_template("login.html")
        else:
            flash('Login ou senha invalido')
            return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET','POST'])
def add_cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        users = {
            'name': name,
            'email': email,
            'password': password
        }
        
        colection.insert_one(users)
        
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
