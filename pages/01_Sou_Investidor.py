import streamlit as st
import pandas as pd
import datetime
import time

st.title("Tese carregada com sucesso")
st.write("Preencha os dados a seguir para avaliar a aderência da empresaà tese:")

# Camila - GET nome do investidor 
# Camila - GET variáveis X e Y da tese, pré-processada na home

with st.form("Preencha os dados a seguir para avaliar a aderência da empresa à tese:", clear_on_submit=False):
    nome_founder =  st.text_input("Nome founder:", placeholder="Fulano da Silva")
    email_founder = st.text_input("Email:", placeholder="fulano.silva@gmail.com")
    telefone_founder = st.text_input("Telefone:", placeholder="(__) _____-____")
    nome_empresa =  st.text_input("Nome da empresa candidata:", placeholder="Nubank")
    data_fundacao = st.date_input("Data da fundação:", max_value=datetime.date.today())
    data_submissao = datetime.date.today()
    qtd_funcionarios = st.number_input("Quantidade de funcionários:", min_value=1, value=1, step=1, format='%d')
    industria = st.text_input("À qual categoria sua indústria pertence?", placeholder="Fintech")
    prod_proprio = st.radio('Seu produto principal é próprio?', ['Sim', 'Não'])
    
    # Camila - POST das infos da empresa acima
    
    submit = st.form_submit_button("Fazer cadastro")                                 
    if submit:
        st.success('')
        with st.spinner('Analisando sua tese...'):
            # Modulos: 6 e 7 do colab
            st.write(tese.head())
            time.sleep(2)
