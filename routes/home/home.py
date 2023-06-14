from flask import Flask, render_template, url_for, request,redirect,flash, session,Blueprint
from routes.index.index import index_bp
from routes.admin.admin import admin_bp
from routes.user.user import user_bp


home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/home', methods=['GET'])
def home():
    if request.method == "GET":
        if 'user' in session:
            return render_template("home.html")
        
        else:
            return redirect(url_for('user.login'))