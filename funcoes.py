import os

def verifica_pasta(ano, caminho):
    data = ano
    pasta_alvo = rf'{caminho}\{data}'
    if not os.path.exists(pasta_alvo):
        os.mkdir(pasta_alvo)
    return pasta_alvo
