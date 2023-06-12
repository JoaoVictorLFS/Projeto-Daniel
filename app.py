import os
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request,redirect,flash, session
from dotenv import load_dotenv, dotenv_values
from werkzeug.security import check_password_hash, generate_password_hash
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import nltk
from bson import ObjectId

nltk.download('punkt')

load_dotenv()

db = os.getenv('DB')
secret_key = os.getenv('SECRET_KEY')

client = MongoClient(db)
db = client['usuarios']

app = Flask(__name__)
app.secret_key = secret_key

def resumo_texto(resumo):
  string = ""
  for sentenca in resumo:
    string = string+str(sentenca)+''
  return string

@app.route('/admin', methods=['GET'])
def admin():
    colection = db['users']
    users = list(colection.find()) # Obtenha a lista de usuários do MongoDB
    return render_template('admin.html', users=users)

@app.route('/edit_user/<user_id>', methods=['GET'])
def show_edit_user(user_id):
    colection = db['users']
    
    user = colection.find_one({'_id': ObjectId(user_id)})  # Converta user_id para ObjectId
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
    colection = db['users']
    colection.update_one({'_id': ObjectId(user_id)}, {'$set': {'name': name, 'email': email, 'password': password}})

    #flash('Usuário atualizado com sucesso')
    return redirect(url_for('admin'))


@app.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    # Converta o ID para ObjectId
    user_id = ObjectId(user_id)
    colection = db['users']
    colection.delete_one({'_id': user_id})

    return redirect(url_for('admin'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    if request.method == "GET":
        if 'user' in session:
            return render_template("home.html")
        
        else:
            return redirect(url_for('login'))
        
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        if 'user' in session:
            return redirect(url_for('home'))
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
                return redirect(url_for('home'))
            
            else:
                flash('Senha invalida')
                return render_template("login.html")
        else:
            flash('Usuário invalido')
            return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == "GET":
        if 'user' in session:
            return redirect(url_for('home'))
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
                    return redirect(url_for('cadastro'))
                
                elif user['email'] == email:
                    flash('E-mail já cadastrado')
                    return redirect(url_for('cadastro'))
                
            else:
                colection.insert_one(usercadastro)
                return redirect(url_for('login'))
        else:
            colection.insert_one(usercadastro)
            return redirect(url_for('login'))

@app.route('/resumo', methods=['GET', 'POST'])
def resumo():
    if request.method == "GET":
        if 'user' in session:
            return render_template("resumo.html")
        
        else:
            return redirect(url_for('login'))
    
    else:
        colection = db['summary']

        texto = request.form['texto']
        texto.center
        parser = PlaintextParser.from_string(texto, Tokenizer('portuguese'))
        sumarizador =  LuhnSummarizer()
        resumo = sumarizador(parser.document, 7)
        resumo = resumo_texto(resumo)

        resultado = {
            'user': session['user'],
            'summary': resumo

        }
        
        colection.insert_one(resultado)
        return redirect(url_for('resultadoResumo'))

@app.route('/resumo/resultado', methods=['GET','POST'])
def resultadoResumo():    
    if request.method == "GET":
        if 'user' in session:
            colection = db['summary']
            validuser = session['user']
            for u in colection.find({'user':validuser}).limit(1).sort([( '$natural', -1 )] ):
                texto = u['summary']
                return render_template("resultado_resumo.html",text=texto)
        
        else:
            return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
