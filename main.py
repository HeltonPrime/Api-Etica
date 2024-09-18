import sys
import os
import jwt

# Obtendo o diretório do script principal (main.py)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho completo para a pasta src
src_path = os.path.join(base_dir, 'src')

# Adiciona o caminho da pasta src ao PYTHONPATH
if src_path not in sys.path:
    sys.path.append(src_path)

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import querys

# Configurações para JWT
SECRET_KEY = "chave_de_segurança"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Criar o Token JWT
def criar_token_jwt(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rota para validar usuário
@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario_validado = querys.validar_usuario(form_data.username, form_data.password, 'src/config.ini', 'DADOS')

    if usuario_validado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Criação do token com o ID_PERFIL e o nome do usuário
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": usuario_validado['nome'],
        "id_perfil": usuario_validado['id_perfil']
    }
    access_token = criar_token_jwt(
        data=token_data, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Rota Dashboard
@app.get("/dashboard/")
async def acessar_dashboard(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        funcionario = payload.get("sub")
        id_perfil = payload.get("id_perfil")
        if funcionario is None or id_perfil is None:
            raise HTTPException(status_code=401, detail="Token Inválido")

        # Obtém as permissões do perfil
        permissoes = querys.obter_permissoes(id_perfil, 'src/config.ini', 'DADOS')
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token Inválido")

    return {"mensagem": f"Bem-vindo ao Dashboard, {funcionario}.", "permissoes": permissoes}
    

# Inicia o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8134)
