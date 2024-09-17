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
    resultado = validar_usuario(login.usuario, login.senha)

    if resultado:
        return resultado
    else:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

# Inicia o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8134)
