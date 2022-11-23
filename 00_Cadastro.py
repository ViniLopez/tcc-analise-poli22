import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import datetime
import time

import requests

import teste_vini

global_url = 'http://127.0.0.1:5000/'
isApiRunning = True
#isApiRunning = False

###########################
# FrontEnd pelo StreamLit #
###########################

st.title("TCC - AUTOMATIZAÇÃO DE ANÁLISE DE EMPRESAS PARA AUXÍLIO DE DECISÃO DE INVESTIMENTOS")
st.write("Ferramenta de suporte para decisão de investimento em startups a partir de Machine Learning")

# Teste de integração entre outros arquivos
#st.write(teste_vini.main(2))

st.subheader("Bem-vindo ao projeto, primeiramente nos diga, quem é você e faça seu cadastro:")
perfil = st.radio('Eu sou:', ['Investidor', 'Empreendedor'])
st.markdown("""---""")
isInvestor = False

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index = False).encode('utf-8')

if perfil == 'Investidor':
  isInvestor = True

  st.write("Legal! Agora, faremos seu cadastro. Para isso precisaremos de um registro em planilha de empresas que você já analisou anteriormente e decidiu (investir ou não). Baixe a seguir os nossos templates!\n")
  
  col1, col2 = st.columns(2)
  
  # Modelo para baixar e preencher
  with col1:
    st.write("Baixe o modelo de importação dos dados! Preencha-o com as informações de todas as empresas que você já avaliou, e a decisão final!")
    # Camila Done: GET de um modelo de tabela vazia

    if isApiRunning:
      pandas_load = pd.read_json(r"investor_json_examples\\investor_empty.json")
      guia_importacao = convert_df(pandas_load)

      baixou_modelo = st.download_button('Download modelo',
                                        data=guia_importacao,
                                        file_name='guia_importacao_tese.csv',
                                        mime='text/csv')
    else: 
      guia_importacao =  '''teste, oi'''
      baixou_modelo = st.download_button('Download modelo', guia_importacao, 'guia_importacao_tese.csv')    

    if (baixou_modelo):
      st.write('Download feito! Não esqueça de respeitar a formatação do arquivo!')
  
  # Testes usados
  with col2:
    st.write("Caso queira entender como funciona primeiro, preparamos este conjunto de dados para você simular!")
    # Camila Done: GET da tabela que usamos de teste
    if isApiRunning:
      pandas_load = pd.read_json(r"investor_json_examples\\investor_filled.json")
      exemplo_tese = convert_df(pandas_load)

      baixou_modelo = st.download_button('Download modelo',
        data=exemplo_tese,
        file_name='exemplo_tese.csv',
        mime='text/csv')
    else: 
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
    senha = st.text_input("Senha:", placeholder="****")
    
    st.write("\nAgora, sobre sua tese de investimentos:")

    tese = st.file_uploader('Faça upload das últimas empresas que você analisou aqui: (CSV)', type='csv')

    aceito_lgpd = st.checkbox('Concordo em compartilhar essas informações e sei que o projeto armazenará os dados de minha tese anonimizados, não sendo permitido o compartilhamento dos mesmos.')
    submit = st.form_submit_button("Começar análise")

  if (submit and aceito_lgpd and tese is not None):

    # Camila Done: POST informações de cadastro acima

    if isApiRunning:
      add_profile = {
        "_user_name": email,
        "name" : nome,
        "email" : email,
        "phone" : telefone,
        "investor": isInvestor,
        "password": senha
      } 

      inserted = requests.post(global_url + 'profile', json = add_profile)

      st.success(f"{inserted.json()['name']}, cadastro concluído com sucesso!")
    else:
      st.success(f"{nome}, cadastro concluído com sucesso!")
    tese = pd.read_csv(tese)

    # Iniciar EDA e descrição da tese
    st.markdown("""---""")
    st.write("Tese do " + nome + ":")
    with st.spinner('Analisando sua tese...'):
      st.write(tese.head())
      # Modulo 1 Colab - Data Augmentation
      # Modulo 2 Colab - Treinar o modelo
      # Modulo 3 Colab - Limpeza dos dados
      # Modulo 4 Colab - EDA
      # Modulo 5 Colab - Engenharia de variáveis
      
      # Camila: POST conjuntos X e Y da tese
      
      # Principais variáveis do modelo Random Forest

      # Modulo 6 Colab - Treino dos modelos
      # Modulo 7 Colab - Aplicação dos dois
        # comparar .score e ver quem é maior
        # Camila: POST modelo escolhido

      # Modelo escolhido
      # Acurácia do modelo
  # avaliar_empresa = st.button("Finalizar cadastro e avaliar uma empresa!")
  # if(avaliar_empresa):
  #   switch_page("01_avaliar_empresa")

elif perfil == 'Empreendedor':
  st.header("Nos conte mais de sua empresa")
  # Cadastro inicial com informações pessoais e da tese de investimentos
  with st.form("Nos conte mais sobre você:", clear_on_submit=False):
    nome_founder =  st.text_input("Seu nome:", placeholder="Fulano da Silva")
    email_founder = st.text_input("Email:", placeholder="fulano.silva@gmail.com")
    telefone_founder = st.text_input("Telefone:", placeholder="(__) _____-____")
    senha_founder = st.text_input("Senha:", placeholder="*****")

    nome_empresa =  st.text_input("Nome da sua empresa:", placeholder="Nubank")
    cnpj_empresa =  st.text_input("CNPJ da sua empresa:", placeholder="xx.xxx.xxx/0001-xx")
    data_fundacao = st.date_input("Data da fundação:", max_value=datetime.date.today())
    data_submissao = datetime.date.today()
    qtd_funcionarios = st.number_input("Quantidade de funcionários:", min_value=1, value=1, step=1, format='%d')
    industria = st.text_input("À qual categoria sua indústria pertence?", placeholder="Cleantech")
    prod_proprio = st.radio('Seu produto principal é próprio?', ['Sim', 'Não'])
    submit = st.form_submit_button("Fazer cadastro")                                 
  if submit:
      # Camila done: POST informações de cadastro acima
      if isApiRunning:
        add_profile = {
          "_user_name": email_founder,
          "name" : nome_founder,
          "email" : email_founder,
          "phone" : telefone_founder,
          "investor": isInvestor,
          "password": senha_founder
        } 

        profile_inserted = requests.post(global_url + 'profile', json = add_profile)
        
        if profile_inserted:
          add_company = {
            "_company_cnpj": cnpj_empresa,
            "_company_id" : nome_empresa,
            "_user_name" : email_founder,
            "oficial_name" : nome_empresa,
            "data_fundacao" : data_fundacao,
            "data_submissao" : data_submissao,
            "qtd_funcionarios" : qtd_funcionarios,
            "industria" : industria,
            "prod_proprio" : prod_proprio,
            # "prod_proprio" : True if prod_proprio == 'Sim' else False,
          } 

          company_inserted = requests.post(global_url + 'company', json = add_company)

        st.success(f'''{profile_inserted.json()["name"]}, seu cadastro e da empresa {company_inserted.json()["oficial_name"]}
          foram concluídos com sucesso! Redirecionando para a página de escolha de teses em instantes...''')
      else:
        st.success(f'''{nome_founder}, seu cadastro e da empresa {nome_empresa} foram concluídos com sucesso!
          Redirecionando para a página de escolha de teses em instantes...''')

      time.sleep(3)
      switch_page("02_Sou_Founder")

# Explicação do projeto
st.markdown("""---""")
st.subheader("Propósito do projeto:")
st.write("Temos a visão de nos tornarmos um canal de conexão entre Investidores e Empreendedores. Através desta plataforma, é possível encontrar potenciais novas parcerias!")
about = st.button("Conhecer saber mais do projeto!")
if(about):
    switch_page("99_About")
