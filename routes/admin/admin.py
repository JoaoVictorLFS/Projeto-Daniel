from flask import Flask, render_template, url_for, request,redirect,flash, session,Blueprint
from dotenv import load_dotenv, dotenv_values
import os 
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import check_password_hash

load_dotenv()

db = os.getenv('DB')

client = MongoClient(db)
db = client['usuarios']

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/admin/login', methods=['GET','POST'])
def loginAdmin():
    if request.method == "GET":
         return render_template('login_adm.html')
    else:
        colection = db['admin']
        user1 = request.form['usuario']
        password = request.form['senha']

        users = {
            'user': user1,
        }

        usuario = colection.find_one(users)
       
        if usuario:
            userlogin = usuario['user']
            userpassword = usuario['password']

            if check_password_hash(userpassword, password) == True:
                session['adm'] = userlogin
                return redirect(url_for('admin.admin'))
            
            else:
                flash('Senha invalida')
                return render_template('login_adm.html')
        else:
            flash('Usuário invalido')
            return redirect(url_for('admin.loginAdmin'))

@admin_bp.route('/admin/logout', methods=['GET'])
def logout():
    session.pop('adm', None)
    return redirect(url_for('index.index'))


@admin_bp.route('/admin', methods=['GET'])
def admin():
    if request.method == "GET":
        if 'adm' in session:
            colection = db['users']
            users = list(colection.find()) # Obtenha a lista de usuários do MongoDB
            return render_template('admin.html', users=users)
        
        else:
            return redirect(url_for('admin.loginAdmin'))

@admin_bp.route('/edit_user/<user_id>', methods=['GET'])
def show_edit_user(user_id):
    if request.method == "GET":
        if 'adm' in session:
            colection = db['users']
            
            user = colection.find_one({'_id': ObjectId(user_id)})  # Converta user_id para ObjectId
            if user:
                return render_template('edit_user.html', user=user)
            else:
                flash('Usuário não encontrado')
                return redirect(url_for('admin.admin'))
    else:
        return redirect(url_for('admin.loginAdmin'))

@admin_bp.route('/edit_user/<user_id>', methods=['POST'])
def edit_user(user_id):

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    colection = db['users']
    colection.update_one({'_id': ObjectId(user_id)}, {'$set': {'name': name, 'email': email, 'password': password}})

    #flash('Usuário atualizado com sucesso')
    return redirect(url_for('admin.admin'))


@admin_bp.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    # Converta o ID para ObjectId
    user_id = ObjectId(user_id)
    colection = db['users']
    colection.delete_one({'_id': user_id})

    return redirect(url_for('admin.admin'))


