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
    caminho = os.path.join(MODEL_DIR, f"{nome}.onnx")
    
    # Se o modelo já existe localmente, usa ele
    if os.path.exists(caminho):
        return caminho
    
    print(f"Baixando modelo {nome}...")
    resposta = requests.get(url)
    with open(caminho, "wb") as f:
        f.write(resposta.content)
    
    # Tenta salvar no banco (se falhar, o modelo ainda estará salvo localmente)
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO modelos (nome, modelo) VALUES (%s, %s)", (nome, resposta.content))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
    
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
