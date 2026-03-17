import plotly.express as px
import pandas as pd
import funcoes
from dotenv import load_dotenv
import os

ano = 2024
mes = 'jan'

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

res = pd.read_excel(f'{ano}/{mes}/resumo_universidades_jan_2025.xlsx')
res['Custo_Total'] = res['Custo_Total'] / 1_000_000
filtro = res['Custo_Total'] > 11.60
fig = px.pie(
    res[filtro],
    values='Custo_Total',
    names='Nome Órgão',
    title=f'Distribuição de Custos por Universidade (Em Milhões) – jan/{ano}',
    hole=0.35
)

fig.update_traces(
    textinfo='label+percent',
    hovertemplate=(
        '<b>%{label}</b><br>'
        'Custo: R$ %{value:,.2f}<br>'
        'Percentual: %{percent}'
    )
)

fig.update_layout(
    legend_title_text='Universidades com custo superior a 11.60 milhões'
)