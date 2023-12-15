import uuid
import joblib
import pandas as pd
from flask import Flask, jsonify, request, current_app, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from treinamento import train_model
from flask import Flask, render_template, request, redirect, url_for, flash


DB_URL = 'postgresql://postgres:postgres@localhost:5432/abex'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = 'umachaveultrasecreta'

db = SQLAlchemy(app)

model = None

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(512))

# -------------------CreateUser------------------------
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data['password'] or not data['user']:
        return jsonify({'message':'Usuário ou senha não informados'}) 

    hashed_password = generate_password_hash(data['password'], method='pbkdf2')
    public_id = str(uuid.uuid4())

    new_user = User(public_id=public_id,
                    username=data['user'],
                    password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso.'})
# -------------------------------------------------

# -------------------login----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Usuário ou senha não informados')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Usuário inválido')
            return redirect(url_for('login'))

        if check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('dashboard'))  # redireciona para o dashboard
        
        flash('Erro ao fazer login. Verifique as suas credenciais.')
        return redirect(url_for('login'))

    return render_template('login.html')
# -------------------------------------------------

# ----------------show_prediction----------------------
from flask import request, jsonify

@app.route('/show_prediction', methods=['POST', 'GET'])
def show_prediction():
    if request.method == 'POST':
        # Aqui você pode obter a previsão
        prediction = get_prediction()  # substitua por sua função de previsão

        return jsonify({'prediction': prediction})
    else:
        # Aqui você pode lidar com solicitações GET, se necessário
        pass

def get_prediction():
    # Implement your logic to obtain the prediction here
    pass
# -------------------------------------------------


# -----------------predict-----------------------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json(force=True)

        if not data:
            return jsonify({'message': 'Envie os dados para fazer a predicão'}), 500

        try:
            X_test = {key: float(value) for key, value in data.items()}
            X_test = pd.DataFrame(data, index=[0])
            X_test.insert(0, 'Unnamed: 0', 0)
            prediction = model.predict(X_test)
            print(prediction)

            return jsonify({'prediction': prediction.tolist()})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Erro durante a predição. \
                            Consulte a documentação para verificar \
                             as chaves dos dados.'}), 500
    else:  # Se a solicitação for GET
        # Aqui você pode retornar uma previsão padrão ou fazer outra coisa
        return jsonify({'prediction': get_prediction()})
# -------------------------------------------------

# ---------------TRAIN------------------------
@app.route('/train', methods=['GET'])
def train():
    # Treinar um novo modelo
    train_model()

    # Retornar uma mensagem de sucesso
    return jsonify({'message': 'Novo modelo treinado com sucesso'}), 200
# -------------------------------------------------

# --------------DASHBOARD------------------------
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))
# -------------------------------------------------

# --------------LOGOUT------------------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# -------------------------------------------------

if __name__ == '__main__':

    train_model()

    print("Carregando o modelo.....")
    model = joblib.load('rf_opt.joblib')
    print("Modelo carregado!")
    app.run()