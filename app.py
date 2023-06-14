import os
from flask import Flask
from dotenv import load_dotenv
from routes.index.index import index_bp
from routes.admin.admin import admin_bp
from routes.user.user import user_bp
from routes.home.home import home_bp
from routes.resumo.resumo import resumo_bp

load_dotenv()

secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = secret_key
app.register_blueprint(index_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)
app.register_blueprint(resumo_bp)
  
if __name__ == '__main__':
    app.run()
