import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

import pymongo

st.title("TCC - AUTOMATIZAÇÃO DE ANÁLISE DE EMPRESAS PARA AUXÍLIO DE DECISÃO DE INVESTIMENTOS")
st.write("Ferramenta de suporte para decisão de investimento em startups a partir de Machine Learning")

###################################################################################
# Initialize connection.
# Uses st.experimental_singleton to only run once.

@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

import pdb
pdb.set_trace()

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_data():
    db = client.users
    items = db.profile.find()
    items = list(items)  # make hashable for st.experimental_memo
    return items

items = get_data()
pdb.set_trace()

# Print results.
for item in items:
    st.write(f"{item['name']} has a {item['email']}")
    
###################################################################################

st.subheader("Bem-vindo ao projeto, primeiramente nos diga, quem é você:")
perfil = st.selectbox('Eu sou:', ['Investidor', 'Empreendedor'])

if perfil == 'Investidor':
  # Cadastro inicial com informações pessoais e da tese de investimentos
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
      # Iniciar EDA e descrição da tese
      st.markdown("""---""")
      st.write("Tese do " + nome + ":")
      with st.spinner('Wait for it...'):
        st.write(tese.head())
        # EDA
        # Principais variáveis do modelo Random Forest
        # Modelo escolhido
        # Acurácia do modelo

      botao = st.button("Cadastrar e avaliar uma empresa:")
      #if botao:
        # Salvar as variáveis do modelo para rodar
        #switch_page("01_avaliar_empresa")

elif perfil == 'Empreendedor':
  st.header("Nos conte mais de sua empresa")

# Explicação do projeto
st.markdown("""---""")
st.subheader("Propósito do projeto:")
st.write("Temos a visão de nos tornarmos um canal de conexão entre Investidores e Empreendedores. Através desta plataforma, é possível encontrar potenciais novas parcerias! Conheça mais na página a seguir:")
#  if(st.button("Conhecer saber mais do projeto!")):
#    choice = 'About'

"""
Snippet para mudar de pagina com o metodo switch_page:
  botao = st.button("Cadastrar e avaliar uma empresa:")
  if botao:
    switch_page("01_avaliar_empresa")
"""
