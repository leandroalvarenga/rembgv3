import os
import requests
import mysql.connector
from rembg.session_factory import new_session

MODEL_DIR = "modelos"

MODELOS = {
    "Padrão": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
    "Plus": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx",
    "Retrato": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-portrait-epoch_150.onnx",
    "Ilustração": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-anime.onnx"
}