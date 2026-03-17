import streamlit as st
import pandas as pd
import plotly.express as px

try:
    st.set_page_config(page_title='Dashboard Universidades', layout='wide')

    anos = ['2025', '2024']
    meses = {
        'Janeiro': 'jan',
        'Fevereiro': 'fev',
        'Março': 'mar',
        'Abril': 'abr',
        'Maio': 'mai',
        'Junho': 'jun',
        'Julho': 'jul',
        'Agosto': 'ago',
        'Setembro': 'set',
        'Outubro': 'out',
        'Novembro': 'nov',
        'Dezembro': 'dez'
    }

    st.title(':blue[Resumo Universidades]', text_alignment='center')
    container = st.container(horizontal=True, horizontal_alignment='center', vertical_alignment='bottom', height=100, border=False, gap='large')
    option_ano = container.selectbox('Anos Disponíveis', anos, width=250)
    option_mes = container.selectbox('Meses Disponíveis', meses.keys(), width=250)
    mes_codigo = meses[option_mes]
    df_res = pd.read_excel(f'{option_ano}/{mes_codigo}/resumo_universidades_{mes_codigo}_{option_ano}.xlsx')
    st.subheader(f'Resumo dos Custos de {option_mes} de {option_ano}')
    df_res

    st.subheader(f'Distribuição de Custos por Universidade (Em Milhões) – {option_mes}/{option_ano}')
    res = pd.read_excel(f'{option_ano}/{mes_codigo}/resumo_universidades_{mes_codigo}_{option_ano}.xlsx')
    res['Custo_Total'] = res['Custo_Total'] / 1_000_000
    filtro = res['Custo_Total'] > 11.60
    fig = px.pie(
        res[filtro],
        values='Custo_Total',
        names='Nome Órgão',
        title='Universidades com custo superior a 11.60 milhões',
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
        legend_title_text='Universidades'
    )

    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.subheader(':red[Tabela não encontrada!]', text_alignment='center')