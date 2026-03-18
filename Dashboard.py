import streamlit as st
import pandas as pd
import os
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


    st.title(':blue[Dashboard Universidades]', text_alignment='center')
    container = st.container(horizontal=True, horizontal_alignment='center', vertical_alignment='bottom', height=100, border=False, gap='large')
    option_ano = container.selectbox('Anos Disponíveis:', anos, width=250)
    option_mes = container.selectbox('Meses Disponíveis:', meses.keys(), width=250)
    mes_codigo = meses[option_mes]
    df_uni = pd.read_excel(f'{option_ano}/{mes_codigo}/universidades_{mes_codigo}_{option_ano}.xlsx', dtype=str)
    st.subheader(f'Custos de {option_mes} de {option_ano}')
    df_uni

    st.subheader(f'Custo anual de {option_ano}')
    dados = []

    for mes_nome, mes_abrev in meses.items():
        caminho = f'{option_ano}/{mes_abrev}/universidades_{mes_abrev}_{option_ano}.xlsx'
        if os.path.exists(caminho):
            df_mes = pd.read_excel(caminho)
            custo_total = df_mes['Custo Total'].sum()

            dados.append({
                'Mês': mes_nome,
                'Custo (R$)': custo_total / 1_000_000_000  # bilhões
            })

    df_anual = pd.DataFrame(dados)

    fig = px.bar(
        df_anual,
        x='Mês',
        y='Custo (R$)',
        text='Custo (R$)',
    )

    fig.update_traces(
        texttemplate='R$ %{text:.2f} bi',
        textposition='outside'
    )

    fig.update_layout(
        yaxis_title='Custo (em bilhões de R$)',
        yaxis_tickformat='.2f',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig, use_container_width=True)



except FileNotFoundError:
    st.subheader(':red[Tabela não encontrada!]', text_alignment='center')

