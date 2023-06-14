
from flask import Flask, render_template, url_for, request,redirect,flash, session, Blueprint
from dotenv import load_dotenv, dotenv_values

index_bp = Blueprint('index', __name__, template_folder='templates')

@index_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
