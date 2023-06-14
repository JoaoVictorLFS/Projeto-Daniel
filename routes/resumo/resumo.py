import os
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request,redirect,flash, session,Blueprint
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import nltk

nltk.download('punkt')

def resumo_texto(resumo):
  string = ""
  for sentenca in resumo:
    string = string+str(sentenca)+''
  return string

load_dotenv()

db = os.getenv('DB')
client = MongoClient(db)
db = client['usuarios']

resumo_bp = Blueprint('resumo', __name__, template_folder='templates')

@resumo_bp.route('/resumo', methods=['GET', 'POST'])
def resumo():
    if request.method == "GET":
        if 'user' in session:
            return render_template("resumo.html")
        
        else:
            return redirect(url_for('user.login'))
    
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
        if texto == '':
            return redirect(url_for('resumo.resultadoResumo'))
        
        else:
            colection.insert_one(resultado)
            return redirect(url_for('resumo.resultadoResumo'))

@resumo_bp.route('/resumo/resultado', methods=['GET','POST'])
def resultadoResumo():    
    if request.method == "GET":
        if 'user' in session:
            colection = db['summary']
            validuser = session['user']
            for u in colection.find({'user':validuser}).limit(1).sort([( '$natural', -1 )] ):
                texto = u['summary']
            
                if texto:
                    return render_template("resultado_resumo.html",text=texto)
                    
            else:
                return redirect(url_for('resumo.resumo'))
        
        else:
            return redirect(url_for('user.login'))