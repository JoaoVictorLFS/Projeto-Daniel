from flask import Flask, render_template, url_for, request,redirect,flash, session,Blueprint
from dotenv import load_dotenv, dotenv_values
import os 
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

db = os.getenv('DB')

client = MongoClient(db)
db = client['usuarios']

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        if 'user' in session:
            return redirect(url_for('home.home'))
        else:
            return render_template("login.html")
        
    else:
        colection = db['users']
        user = request.form['usuario']
        password = request.form['senha']

        users = {
            'name': user,
        }

        usuario = colection.find_one(users)
       
        if usuario:
            userlogin = usuario['name']
            userpassword = usuario['password']
            if check_password_hash(userpassword, password) == True:
                session['user'] = userlogin
                return redirect(url_for('home.home'))
            
            else:
                flash('Senha invalida')
                return render_template("login.html")
        else:
            flash('Usuário invalido')
            return redirect(url_for('user.login'))

@user_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index.index'))

@user_bp.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == "GET":
        if 'user' in session:
            return redirect(url_for('home.home'))
        else:
            return render_template("cadastro.html")

    else:
        colection = db['users']

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        usercadastro = {
            'name': name,
            'email': email,
            'password': generate_password_hash(password)
        }
        
        usuario = colection.find()

        if usuario:
            for user in usuario:
                if user['name'] == name:
                    flash('Nome já cadastrado')
                    return redirect(url_for('user.cadastro'))
                
                elif user['email'] == email:
                    flash('E-mail já cadastrado')
                    return redirect(url_for('user.cadastro'))
                
            else:
                colection.insert_one(usercadastro)
                return redirect(url_for('user.login'))
        else:
            colection.insert_one(usercadastro)
            return redirect(url_for('user.login'))
        

