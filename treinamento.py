# exemplo20_10_2023.py

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from joblib import dump
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def train_model():
    # Carregar os dados do arquivo CSV
    dados = pd.read_csv('dataset_evasao.csv')

    dados.dropna(subset=['evadido'], inplace=True)

    # Codificar variáveis categóricas
    for column in dados.columns:
        if dados[column].dtype == type(object):
            le = LabelEncoder()
            dados[column] = le.fit_transform(dados[column])

    x = dados.drop(['evadido'], axis=1)
    y = dados['evadido']

    evadido = LabelEncoder()
    y = evadido.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    modelo = KNeighborsClassifier(n_neighbors=4)
    modelo.fit(x_train, y_train)

    # Salvar o modelo treinado
    dump(modelo, 'rf_opt.joblib')

    y_pred = modelo.predict(x_test)

    print("Acurácia:", metrics.accuracy_score(y_test, y_pred))
    print("F1-score:", metrics.f1_score(y_test, y_pred))
    print("Precisao:", metrics.precision_score(y_test, y_pred))
    print("Sensibilidade:", metrics.recall_score(y_test, y_pred))

