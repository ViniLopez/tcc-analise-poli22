import streamlit as st
import pandas as pd

st.title("TCC - AUTOMATIZAÇÃO DE ANÁLISE DE EMPRESAS PARA AUXÍLIO DE DECISÃO DE INVESTIMENTOS")
st.write("Ferramenta de suporte para decisão de investimento em startups a partir de Machine Learning")

st.markdown('<a href="/pages/99_about.py" target="_self">Conheça mais do projeto</a>', unsafe_allow_html=True)

st.subheader("Bem-vindo ao projeto, primeiramente nos diga, quem é você:")
perfil = st.selectbox('Eu sou:', ['Investidor', 'Empreendedor'])

if perfil == 'Investidor':
  with st.form("Nos conte mais sobre você:", clear_on_submit=True):
    nome = st.text_input("Nome:")
    email = st.text_input("Email:")
    telefone = st.text_input("Telefone:")

    st.write("\nAgora, sobre sua tese de investimentos:")

    tese = st.file_uploader('Faça upload das últimas empresas que você analisou aqui: (CSV)', type='csv')
    aceito_lgpd = st.checkbox('Concordo em compartilhar essas informações e sei que o projeto armazenará os dados de minha tese anonimizados, não sendo permitido o compartilhamento dos mesmos.')
    submit = st.form_submit_button("Começar análise")
    if (submit and aceito_lgpd):
      st.success('Cadastro concluído com sucesso!')
      tese = pd.read_csv(tese)
      st.write(tese.head())

elif perfil == 'Empreendedor':
  st.header("Nos conte mais de sua empresa")

# Explicação do projeto
st.markdown("""---""")
st.subheader("Propósito do projeto:")
st.write("Temos a visão de nos tornarmos um canal de conexão entre Investidores e Empreendedores. Através desta plataforma, é possível encontrar potenciais novas parcerias! Conheça mais na página a seguir:")
#  if(st.button("Conhecer saber mais do projeto!")):
#    choice = 'About'
