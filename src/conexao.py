import fdb
import configparser

# Função para ler o arquivo config.ini
def ler_ini(filename='config.ini', section='DADOS'):
    parser = configparser.ConfigParser()
    parser.read(filename)  # O correto é parser.read()

    # Cria um dicionário com as informações de configuração
    dados = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            dados[param[0].lower()] = param[1]  # Converte chaves para minúsculas para facilitar o uso
    else:
        raise Exception(f'A seção {section} não foi encontrada no arquivo {filename}')
    
    return dados

# Função para obter a conexão com o banco
def obter_conexao(filename='config.ini', section='DADOS'):
    config = ler_ini(filename, section)
    return fdb.connect(
        dsn=config['path'],
        user=config['usuario'],
        password=config['senha'],
        charset='UTF8'
    )

# Teste para ler o arquivo ini
# print(ler_ini(filename='config.ini', section='DADOS'))
