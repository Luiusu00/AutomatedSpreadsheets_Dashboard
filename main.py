import pandas as pd
import funcoes
import plotly.express as px
from dotenv import load_dotenv
import os

#Configurações para exportar
ano = 2024
mes = 'mar'

#Verificando caminhos e configurando
caminho_arq = os.getenv(f"PLANILHA_BASE{ano}_{mes}_ItemCompra.csv")
planilha = pd.read_csv(caminho_arq, encoding='Windows-1252', sep=';', decimal=',')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

#Filtrando apenas universidades e criando coluna nova
filtro_uni = planilha['Nome Órgão'].str.contains('universidade', case=False, na=False)
planilha_universidades = planilha[filtro_uni]
planilha_universidades = planilha_universidades.drop(columns=['Código UG', 'Nome UG', 'Descrição Complementar Item Compra'])
qtd = planilha_universidades['Quantidade Item']
valor = planilha_universidades['Valor Item']
planilha_universidades['Custo Total'] = qtd * valor

#Filtrando custos acima de 0 reais e organizando do maior custo para o menor
filtro_custo = planilha_universidades['Custo Total'] > 0
planilha_universidades = planilha_universidades[filtro_custo]
planilha_universidades = planilha_universidades.sort_values(by='Custo Total', ascending=False).reset_index(drop=True)

#Exportando arquivo universidades
caminho_pasta = funcoes.verifica_pasta(ano, os.getenv("CAMINHO"))
caminho_pasta2 = funcoes.verifica_pasta(mes, f'{caminho_pasta}')
planilha_universidades.to_excel(rf'{caminho_pasta2}\universidades_{mes}_{ano}.xlsx', index=False)

#Resumo
planilha_resumo = planilha_universidades.copy()
planilha_resumo['Quantidade total'] = planilha_universidades['Quantidade Item'].sum()
planilha_resumo = planilha_universidades.groupby('Nome Órgão', as_index=False).agg(Quantidade_Total=('Quantidade Item', 'sum'), Valor_Total=('Valor Item', 'sum'), Custo_Total=('Custo Total', 'sum'))

#Exportando planilha Resumos
caminho_pasta = funcoes.verifica_pasta(ano, os.getenv("CAMINHO"))
caminho_pasta2 = funcoes.verifica_pasta(mes, f'{caminho_pasta}')
planilha_resumo.to_excel(rf'{caminho_pasta2}\resumo_universidades_{mes}_{ano}.xlsx', index=False)

#Gráfico Custo Anual
meses = {
    'jan': 'Janeiro',
    'fev': 'Fevereiro',
    'mar': 'Março',
    'abr': 'Abril',
    'mai': 'Maio',
    'jun': 'Junho',
    'jul': 'Julho',
    'ago': 'Agosto',
    'set': 'Setembro',
    'out': 'Outubro',
    'nov': 'Novembro',
    'dez': 'Dezembro'
}

dfs = {
    'Janeiro': [],
    'Fevereiro': [],
    'Março': [],
    'Abril': [],
    'Maio': [],
    'Junho': [],
    'Julho': [],
    'Agosto': [],
    'Setembro': [],
    'Outubro': [],
    'Novembro': [],
    'Dezembro': []
}

for cod, nome in meses.items():
    caminho = f'{ano}/{cod}/universidades_{cod}_{ano}.xlsx'
    try:
        df = pd.read_excel(caminho)
        dfs[nome].append(df)
    except FileNotFoundError:
        pass

resumo_anual = []

ordem_meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

for mes in ordem_meses:
    lista_dfs = dfs.get(mes, [])

    if lista_dfs:
        df_mes = pd.concat(lista_dfs, ignore_index=True)

        # garante que é número
        custo = df_mes['Custo Total'].sum()

    else:
        custo = 0

    resumo_anual.append({
        'Mês': mes,
        'Custo Total': custo
    })

df_anual = pd.DataFrame(resumo_anual)
caminho_pasta = funcoes.verifica_pasta(ano, os.getenv("CAMINHO"))
df_anual.to_excel(rf'{caminho_pasta}\custos_anual_{ano}.xlsx', index=False)

df_anual['Custo (Bilhões)'] = df_anual['Custo Total'] / 1_000_000_000

fig = px.bar(
    df_anual,
    x='Mês',
    y='Custo (Bilhões)',
    title='Custo Anual por Mês (em bilhões)',
    text_auto='.2f'
)

fig.update_layout(
    yaxis_title='Custo Total (R$ bilhões)',
    yaxis_tickformat='.2f'
)
caminho_pasta = funcoes.verifica_pasta(ano, os.getenv("CAMINHO"))
fig.write_image(f'{caminho_pasta}\grafico_custo_{ano}.png')