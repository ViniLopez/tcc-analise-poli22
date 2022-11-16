import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import datetime
import time

# FrontEnd pelo StreamLit

st.title("TCC - AUTOMATIZAÇÃO DE ANÁLISE DE EMPRESAS PARA AUXÍLIO DE DECISÃO DE INVESTIMENTOS")
st.write("Ferramenta de suporte para decisão de investimento em startups a partir de Machine Learning")

st.subheader("Bem-vindo ao projeto, primeiramente nos diga, quem é você e faça seu cadastro:")
perfil = st.radio('Eu sou:', ['Investidor', 'Empreendedor'])
st.markdown("""---""")

if perfil == 'Investidor':

  st.write("Legal! Agora, faremos seu cadastro. Para isso precisaremos de um registro em planilha de empresas que você já analisou anteriormente e decidiu (investir ou não). Baixe a seguir os nossos templates!\n")
  
  col1, col2 = st.columns(2)
  
  # Modelo para baixar e preencher
  with col1:
    st.write("Baixe o modelo de importação dos dados! Preencha-o com as informações de todas as empresas que você já avaliou, e a decisão final!")
    # Camila: GET de um modelo de tabela
    guia_importacao =  '''teste, oi'''
    baixou_modelo = st.download_button('Download modelo', guia_importacao, 'guia_importacao_tese.csv')
    if (baixou_modelo):
      st.write('Download feito! Não esqueça de respeitar a formatação do arquivo!')
  
  # Testes usados
  with col2:
    st.write("Caso queira entender como funciona primeiro, preparamos este conjunto de dados para você simular!")
    # Camila: GET da tabela que usamos de teste
    exemplo_tese =  '''teste, oi'''
    #st.write(exemplo_tese.head())
    baixou_modelo = st.download_button('Download exemplo', exemplo_tese, 'exemplo_tese.csv')
    if (baixou_modelo):
      st.write('Download feito! Siga adiante!')
  st.markdown("""---""")
  
  # Cadastro inicial com informações pessoais e da tese de investimentos
  with st.form("Nos conte mais sobre você:", clear_on_submit=False):
    nome = st.text_input("Nome:", placeholder="Fulano da Silva")
    email = st.text_input("Email:", placeholder="fulano.silva@gmail.com")
    telefone = st.text_input("Telefone:", placeholder="(__) _____-____")

    st.write("\nAgora, sobre sua tese de investimentos:")

    tese = st.file_uploader('Faça upload das últimas empresas que você analisou aqui: (CSV)', type='csv')

    aceito_lgpd = st.checkbox('Concordo em compartilhar essas informações e sei que o projeto armazenará os dados de minha tese anonimizados, não sendo permitido o compartilhamento dos mesmos.')
    submit = st.form_submit_button("Começar análise")
  if (submit and aceito_lgpd and tese is not None):
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
      switch_page("avaliar empresa")

elif perfil == 'Empreendedor':
  st.header("Nos conte mais de sua empresa")
  # Cadastro inicial com informações pessoais e da tese de investimentos
  with st.form("Nos conte mais sobre você:", clear_on_submit=False):
    nome_founder =  st.text_input("Seu nome:", placeholder="Fulano da Silva")
    email_founder = st.text_input("Email:", placeholder="fulano.silva@gmail.com")
    telefone_founder = st.text_input("Telefone:", placeholder="(__) _____-____")
    nome_founder =  st.text_input("Nome da sua empresa:", placeholder="Nubank")
    data_fundacao = st.date_input("Data da fundação:", max_value=datetime.date.today())
    data_submissao = datetime.date.today()
    qtd_funcionarios = st.number_input("Quantidade de funcionários:", min_value=1, value=1, step=1, format='%d')
    industria = st.text_input("À qual categoria sua indústria pertence?", placeholder="Cleantech")
    prod_proprio = st.radio('Seu produto principal é próprio?', ['Sim', 'Não'])
    submit = st.form_submit_button("Fazer cadastro")                                 
  if submit:
      st.success('Cadastro concluído com sucesso! Redirecionando para a página de escolha de teses...')
      time.sleep(3)
      switch_page("escolher investidor")

# Explicação do projeto
st.markdown("""---""")
st.subheader("Propósito do projeto:")
st.write("Temos a visão de nos tornarmos um canal de conexão entre Investidores e Empreendedores. Através desta plataforma, é possível encontrar potenciais novas parcerias!")
about = st.button("Conhecer saber mais do projeto!")
if(about):
  switch_page("about")
