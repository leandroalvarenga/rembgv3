from fastapi import FastAPI, UploadFile, File, Form
from rembg import remove
from PIL import Image
import io
import modelos

app = FastAPI()

@app.post("/remover_fundo/")
async def remover_fundo(file: UploadFile = File(...), modelo: str = Form("Padrão")):
    modelo_escolhido = modelos.get_modelo(modelo)
    if not modelo_escolhido:
        return {"erro": "Modelo inválido"}
    
    image = Image.open(io.BytesIO(await file.read()))
    output = remove(image, session=modelo_escolhido)
    
    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return {"imagem": img_byte_arr.hex()}