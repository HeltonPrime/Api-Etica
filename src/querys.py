from conexao import obter_conexao

# Validação de Usuário e Senha
def validar_usuario(usuario, senha, filename='config.ini', section='DADOS'):
    try:
        
        conn = obter_conexao(filename, section)
        cursor = conn.cursor()    

        sql = f'''
            SELECT u.ID_PERFIL, f.NOME
            FROM USUARIOS u
            JOIN FUNCIONARIO f            
            ON f.id = u.VENDEDOR
            WHERE u.USUARIO = upper(?) AND u.SENHA = ?                
        '''

        parametros = [usuario, senha]
    
        cursor.execute(sql, parametros)
        resultado = cursor.fetchone()        

        print ({'id_perfil': resultado[0], 'nome': resultado[1]})
        return {'id_perfil': resultado[0], 'nome': resultado[1]} if resultado else None

    except Exception as e:
        print(f"Erro ao validar usuário: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtendo as permissões que o usuário tem
def obter_permissoes(id_perfil, filename='config.ini', section='DADOS'):
    conn = None
    cursor = None
    try:
        conn = obter_conexao(filename, section)
        cursor = conn.cursor()

        permissoes_necessarias = [        
            'Relatorio de Vendas e Comissões',
            'Relatorios em Geral',
            'Giro de Produtos',
            'Registro de Entrada',
            'Bloqueia Relatorio Caixa Diario'
        ]

        placeholders = ', '.join(['?'] * len(permissoes_necessarias))

        sql = f'''
            SELECT PERMITE, DESCRICAO
            FROM USUARIOS_PERMISSOES
            WHERE ID_PERFIL = ?
            AND DESCRICAO IN ({placeholders})
        '''

        parametros = [id_perfil] + permissoes_necessarias
        
        cursor.execute(sql, parametros)
        permissoes = cursor.fetchall()

        # Retorna uma lista com as descricoes
        print([{'permite': p[0], 'descricao': p[1]} for p in permissoes])
        return [{'permite': p[0], 'descricao': p[1]} for p in permissoes]

    except Exception as e:
        print(f"Erro ao obter permissões: {e}")
        return []

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()
                     
    
# Teste validar_usuario
# print(validar_usuario('teste', '123'))

# Teste validar_usuario
#print(obter_permissoes(2, 'config.ini', 'DADOS'))
