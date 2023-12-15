# app.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, current_app, session, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import joblib
import pandas as pd

#importação de modelo
from exemplo20_10_2023 import train_model

# importação de rota
from routes.login import login_blueprint
from routes.create_user import create_user_blueprint
from routes.show_prediction import show_prediction_blueprint
from routes.train import train_blueprint
from routes.dashboard import dashboard

from routes.predict import predict_blueprint

# ... importe os outros blueprints ...

DB_URL = 'postgresql://postgres:postgres@localhost:5432/abex'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = 'umachaveultrasecreta'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(512))

app.register_blueprint(login_blueprint)
app.register_blueprint(create_user_blueprint)
app.register_blueprint(show_prediction_blueprint)
app.register_blueprint(predict_blueprint)
app.register_blueprint(train_blueprint)
# app.register_blueprint(dashboard_blueprint)  # dashboard_blueprint não foi definido

# ... registre os outros blueprints ...

# ---------------Chektoken-----------------------
def check_token(f):
    @wraps(f)

    def decorated(*args, **kwargs):
        # print(datetime.datetime.now())

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token não encontrado.'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            
            if not current_user:
                return({'message': 'Usuário inválido'}), 401
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token não é válido.'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated
# -------------------------------------------------

if __name__ == '__main__':

    train_model()

    print("Carregando o modelo.....")
    model = joblib.load('rf_opt.joblib')
    print("Modelo carregado!")
    app.run()