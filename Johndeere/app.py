from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__, static_folder="static")

modelos_treinados = {}

# Função para gerar dados fictícios
def gerar_dados_ficticios():
    np.random.seed(0)

    data = {
        'Modelo do Veículo': [],
        'Tipo de Peça': [],
        'Quantidade de Manutenções': [],
        'Tempo de Funcionamento': [],
        'Vida Util': []
    }

    modelos_veiculo = ['HPX615E', 'HPX815E', 'TE 4x2 ELECTRIC', 'TH 6x4 DIESEL']
    tipos_pecas = ['Filtros de Ar e Óleo', 'Pastilhas de Freio', 'Bateria', 'Correias de Transmissão']

    for _ in range(10):
        for modelo in modelos_veiculo:
            for tipo_peca in tipos_pecas:
                data['Modelo do Veículo'].append(modelo)
                data['Tipo de Peça'].append(tipo_peca)
                data['Quantidade de Manutenções'].append(np.random.randint(1, 10))
                data['Tempo de Funcionamento'].append(np.random.randint(500, 3000))
                vida_util_media = tipos_pecas_info[tipo_peca]['Vida Util Media']
                data['Vida Util'].append(np.random.randint(vida_util_media - 500, vida_util_media + 500))

    return pd.DataFrame(data)

tipos_pecas_info = {
    'Filtros de Ar e Óleo': {'Vida Util Media': np.random.randint(100, 251)},
    'Pastilhas de Freio': {'Vida Util Media': np.random.randint(1000, 2001)},
    'Bateria': {'Vida Util Media': np.random.randint(2, 6)},
    'Correias de Transmissão': {'Vida Util Media': np.random.randint(500, 1001)},
}

dados_treinamento = gerar_dados_ficticios()

def treinar_e_avaliar_modelo(tipo_peca):
    df = dados_treinamento[dados_treinamento['Tipo de Peça'] == tipo_peca]

    X = df[['Quantidade de Manutenções', 'Tempo de Funcionamento']]
    y = df['Vida Util']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)

    return scaler, rf_model

for tipo_peca in tipos_pecas_info.keys():
    scaler, modelo = treinar_e_avaliar_modelo(tipo_peca)
    modelos_treinados[tipo_peca] = (scaler, modelo)

# Função para fazer previsões
def fazer_previsao(modelo, scaler, quantidade_manutencao, tempo_funcionamento):
    input_data = np.array([[quantidade_manutencao, tempo_funcionamento]])
    input_data_scaled = scaler.transform(input_data)
    vida_util_prevista = modelo.predict(input_data_scaled)
    return vida_util_prevista[0]

# Função para calcular o tempo restante
def calcular_tempo_restante(vida_util_prevista, tempo_funcionamento):
    tempo_restante = vida_util_prevista - tempo_funcionamento
    return max(tempo_restante, 0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fazer_previsao', methods=['POST'])
def fazer_previsao_rota():
    data = request.get_json()
    tipo_peca = data["tipo_peca"]
    quantidade_manutencao = data["quantidade_manutencao"]
    tempo_funcionamento = data["tempo_funcionamento"]

    scaler, modelo = modelos_treinados[tipo_peca]

    # Fazer previsão de vida útil
    vida_util_prevista = fazer_previsao(modelo, scaler, quantidade_manutencao, tempo_funcionamento)

    # Calcular o tempo restante
    tempo_restante = calcular_tempo_restante(vida_util_prevista, tempo_funcionamento)

    return jsonify({
        "vida_util_prevista": vida_util_prevista,
        "tempo_restante": tempo_restante,
    })

if __name__ == '__main__':
    app.run(debug=True)
