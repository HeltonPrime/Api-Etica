import sys
import os

# Obtendo o diretório do script principal (main.py)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho completo para a pasta src
src_path = os.path.join(base_dir, 'src')

# Adiciona o caminho da pasta src ao PYTHONPATH
if src_path not in sys.path:
    sys.path.append(src_path)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.querys import validar_usuario

app = FastAPI()

# Modelo de requisição para login
class LoginRequest(BaseModel):
    usuario: str
    senha: str

# Rota para validar usuário
@app.post("/login/")
async def login(login: LoginRequest):
    resultado = validar_usuario(login.usuario, login.senha, 'src/config.ini', 'DADOS')

    if resultado:
        return resultado
    else:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

# Inicia o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8134)
