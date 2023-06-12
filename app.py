import os
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect, flash
from dotenv import load_dotenv, dotenv_values
from flask import render_template
from bson import ObjectId

load_dotenv()

db = os.getenv('DB')
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# conectando ao banco MongoDB Atlas
mongo_uri = 'mongodb+srv://<user>:<password>@cluster0.m0ltzpg.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(mongo_uri)
db = client['db_site']
collection = db['usuarios']


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/admin', methods=['GET'])
def admin():
    # return render_template('home.html')
    users = list(collection.find()) # Obtenha a lista de usuários do MongoDB
    return render_template('admin.html', users=users)

@app.route('/edit_user/<user_id>', methods=['GET'])
def show_edit_user(user_id):
    user = collection.find_one({'_id': ObjectId(user_id)})  # Converta user_id para ObjectId
    if user:
        return render_template('edit_user.html', user=user)
    else:
        flash('Usuário não encontrado')
        return redirect(url_for('admin'))

@app.route('/edit_user/<user_id>', methods=['POST'])
def edit_user(user_id):
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Atualize as informações do usuário no MongoDB
    collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'name': name, 'email': email, 'password': password}})

    flash('Usuário atualizado com sucesso')
    return redirect(url_for('admin'))

@app.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    # Converta o ID para ObjectId
    user_id = ObjectId(user_id)

    # Exclua o usuário do MongoDB
    collection.delete_one({'_id': user_id})

    flash('Usuário excluído com sucesso')
    return redirect(url_for('admin'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        user = request.form['usuario']
        password = request.form['senha']

        usuarios = {
            'name': user,
        }

        usuario = collection.find_one(usuarios)
        print(usuario)
        if usuario:
            if usuario['password'] == password:
                return redirect(url_for('home'))
            else:
                flash('Senha inválida')
                return render_template("login.html")
        else:
            flash('Login ou senha inválidos')
            return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def add_cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        usuarios = {
            'name': name,
            'email': email,
            'password': password
        }

        collection.insert_one(usuarios)

        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
