import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

# Funções do algoritmo


# FrontEnd pelo StreamLit

st.title("TCC - AUTOMATIZAÇÃO DE ANÁLISE DE EMPRESAS PARA AUXÍLIO DE DECISÃO DE INVESTIMENTOS")
st.write("Ferramenta de suporte para decisão de investimento em startups a partir de Machine Learning")

st.subheader("Bem-vindo ao projeto, primeiramente nos diga, quem é você e faça seu cadastro:")
perfil = st.radio('Eu sou:', ['Investidor', 'Empreendedor'])

if perfil == 'Investidor':
  
  st.write("Baixe o modelo de importação dos dados! Preencha-o com as informações de todas as empresas que você já avaliou, e a decisão final!")
  guia_importacao =  '''teste, oi'''
  st.download_button('Download CSV', guia_importacao, 'guia_importacao_tese/csv')

  if (st.download_button):
    st.write('Download feito! Não esqueça de respeitar a formatação do arquivo!')
  
  # Cadastro inicial com informações pessoais e da tese de investimentos
  with st.form("Nos conte mais sobre você:"):
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
    with st.spinner('Analisando sua tese...'):
      st.write(tese.head())
      # EDA
      # Principais variáveis do modelo Random Forest
      # Modelo escolhido
      # Acurácia do modelo

    pag_avaliar_empresa = st.button("Finalizar cadastro e avaliar uma empresa:")
    if pag_avaliar_empresa:
      switch_page("01_avaliar_empresa")

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
