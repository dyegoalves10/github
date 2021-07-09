import requests
import json
import os

def arquivo_json_existe(file_name):
    return os.path.exists(file_name)

def requisicao_api(url,headers):
    resposta = requests.get(url,headers=headers)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        return resposta.status_code

# Leitura de arquivo json comum 
def ler_arquivo_json_tipo_1(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf8') as f:
        return json.load(f)

# Leitura de arquivo json linha a linha
def ler_arquivo_json_tipo_2(nome_arquivo):
    lista_json = []
    for line in open(nome_arquivo, 'r', encoding='utf8'):
        lista_json.append(json.loads(line))

    return lista_json

def gravar_arquivo_json(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, sort_keys=False, separators=(',' , ':'))

# Verifica se o repositorio está na base de dados json. Em caso positivo, atribui a lista de topicos.
def consulta_topicos_base_de_dados_json(base_dados_json, arquivo_json):
    arquivo_json_topicos = []
    arquivo_json_nao_encontrado = []

    # Pesquisa por URL
    for i in range(len(arquivo_json)):
        achou = False
        for x in range(len(base_dados_json)):
            if arquivo_json[i]['url'] == base_dados_json[x]['url']:
                arquivo_json[i]['list_topics'] = base_dados_json[x]['topics']
                arquivo_json_topicos.append(arquivo_json[i])
                achou = True
                break

        if not achou: 
            #print(arquivo_json[i]['url'])
            arquivo_json_nao_encontrado.append(arquivo_json[i])

    # Pesquisa por Nome e Timestamp de criação
    for i in range(len(arquivo_json_nao_encontrado)):
        achou = False
        # Formata data de UTC para T Z
        data_hora = arquivo_json_nao_encontrado[i]['created_at'].replace(" UTC","Z")
        data_hora_formatada = data_hora.replace(" ","T")
        for x in range(len(base_dados_json)):
            if (arquivo_json_nao_encontrado[i]['name']       == base_dados_json[x]['name'] and
                data_hora_formatada                          == base_dados_json[x]['created_at']):
                arquivo_json_nao_encontrado[i]['list_topics'] = base_dados_json[x]['topics']
                arquivo_json_topicos.append(arquivo_json_nao_encontrado[i])
                achou = True
                break

        if not achou: 
            print(arquivo_json_nao_encontrado[i]['name'])
            print(arquivo_json_nao_encontrado[i]['created_at'])
    
    return arquivo_json_topicos

        
#================================================================================#
# MAIN                                                                           #
#================================================================================#

nome_base_dados = "base_dados_repositorios.json"

print("Informe o nome do arquivo.json que deseja consultar os topicos na base de dados: ")
nome_arquivo = input()

if arquivo_json_existe(nome_arquivo):
    
    print("Deseja pesquisar quantos registros do arquivo informado: ")
    quantidade_registros_pesquisa = input()

    arquivo_json = ler_arquivo_json_tipo_2(nome_arquivo)
    base_dados = ler_arquivo_json_tipo_1(nome_base_dados)
    base_dados_json = base_dados['items']

    # Seleciona os x registros 
    arquivo_json_reg_selecao = []

    for i in range(int(quantidade_registros_pesquisa)):
        arquivo_json_reg_selecao.append(arquivo_json[i])

    arquivo_json_topicos = consulta_topicos_base_de_dados_json(base_dados_json, arquivo_json_reg_selecao)

    print(f'Quantidade de registros encontrados: {str(len(arquivo_json_topicos))}')

    nome_arquivo_saida = f'resultado-{str(nome_arquivo)}'

    gravar_arquivo_json(nome_arquivo_saida, arquivo_json_topicos)

else:
    print(f'Erro - Arquivo {str(nome_arquivo)} não foi localizados!')