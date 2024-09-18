from conexao import obter_conexao

# Validação de Usuário e Senha
def validar_usuario(usuario, senha, filename='config.ini', section='DADOS'):
    try:
        
        conn = obter_conexao(filename, section)
        cursor = conn.cursor()    

        sql = f'''
            SELECT u.ID_PERFIL, u.USUARIO
            FROM USUARIOS u        
            WHERE u.USUARIO = upper(?) AND u.SENHA = ?                
        '''

        parametros = [usuario, senha]
    
        cursor.execute(sql, parametros)
        resultado = cursor.fetchone()
        

        return {'id_perfil': resultado[0], 'usuario': resultado[1]} if resultado else None # {'Resposta': 'Usuário ou Senha Inválido'}

    except Exception as e:
        print(f"Erro ao validar usuário: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
# Teste de query
#print(validar_usuario('teste', '12s3'))
