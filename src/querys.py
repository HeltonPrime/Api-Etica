from conexao import obter_conexao  # Obtendo acesso ao banco de dados

def validar_usuario(usuario, senha, filename='config.ini', section='DADOS'):
    conn = obter_conexao(filename, section)
    cursor = conn.cursor()

    permissoes = [        
        'Relatorio de Vendas e Comissões',
        'Relatorios em Geral',
        'Giro de Produtos',
        'Registro de Entrada',
        'Bloqueia Relatorio Caixa Diario'
    ]

    placeholders = ', '.join(['?'] * len(permissoes))

    sql = f'''
        SELECT u.ID, u.USUARIO, u.SENHA, u.ID_PERFIL, p.permite, p.descricao
        FROM USUARIOS u
        LEFT JOIN usuarios_PERMISSOES p ON u.ID_PERFIL = p.ID_PERFIL
        WHERE u.USUARIO = upper(?) AND u.SENHA = ?        
        AND ((p.descricao is null) or (p.descricao IN ({placeholders})))
    '''

    parametros = [usuario, senha] + permissoes
    
    cursor.execute(sql, parametros)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    if resultados:
        # Extrai os dados do primeiro resultado (usuario e id_perfil)
        primeiro_resultado = resultados[0]
        usuario_info = {
            "id": primeiro_resultado[0],
            "usuario": primeiro_resultado[1],
            "id_perfil": primeiro_resultado[3],
            "permissoes": []
        }

        # Adiciona todas as permissões à lista "permissoes"
        for resultado in resultados:
            usuario_info["permissoes"].append({
                "permite": resultado[4],
                "permissao": resultado[5]
            })

        return usuario_info
    else:
        return None

# Teste de query
# print(validar_usuario('ADMIN', 'trigominas'))
