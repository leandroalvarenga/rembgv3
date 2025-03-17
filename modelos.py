import os
import requests
import mysql.connector
from rembg.session_factory import new_session

MODEL_DIR = "modelos"

# Criar diretório se não existir
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

MODELOS = {
    "Padrão": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
    "Plus": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx",
    "Retrato": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-portrait-epoch_150.onnx",
    "Ilustração": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-anime.onnx"
}

# Configuração do MySQL via variáveis de ambiente
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def conectar_db():
    return mysql.connector.connect(**DB_CONFIG)

def baixar_modelo(nome, url):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verifica se já existe no banco
    cursor.execute("SELECT modelo FROM modelos WHERE nome = %s", (nome,))
    row = cursor.fetchone()
    if row:
        caminho = os.path.join(MODEL_DIR, f"{nome}.onnx")
        with open(caminho, "wb") as f:
            f.write(row[0])
        conn.close()
        return caminho
    
    # Baixa e salva no banco
    print(f"Baixando modelo {nome}...")
    resposta = requests.get(url)
    caminho = os.path.join(MODEL_DIR, f"{nome}.onnx")
    with open(caminho, "wb") as f:
        f.write(resposta.content)
    
    cursor.execute("INSERT INTO modelos (nome, modelo) VALUES (%s, %s)", (nome, resposta.content))
    conn.commit()
    conn.close()
    
    return caminho

def get_modelo(apelido):
    if apelido in MODELOS:
        caminho = baixar_modelo(apelido, MODELOS[apelido])
        return new_session(caminho)
    return None

# Criar tabela no MySQL (rode isso uma vez manualmente no banco)
# CREATE TABLE modelos (
#    id INT AUTO_INCREMENT PRIMARY KEY,
#    nome VARCHAR(50) UNIQUE,
#    modelo LONGBLOB
# );
