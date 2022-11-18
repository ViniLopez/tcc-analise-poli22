import streamlit as st
import pandas as pd
import datetime
import time

st.title("Olá empreendedor, vamos simular sua empresa em uma das nossas teses")

# Camila - GET parâmetros de análise deste empreendedor
# criar dataset X_empreendedor a partir disso

# Camila - GET nomes dos investidores cadastrados

investidores_cadastrados = ["Anima", "Sequoia Capital", "Warren Buffet"]

investidor = st.selectbox('Escolha os investidores que deseja consultar:', investidores_cadastrados)

melhor_match = []

for potencial_investidor in investidores_cadastrados:
  # Camila - GET variáveis X e Y da tese de cada investidor cadastrado, pré-processadas na home
  # Camila - GET modelo indicado para análise
  variaveis_disponiveis = X_empreendedor.columns.tolist()
  variaveis_analisar = X_investidor.columns.tolist()
  
  for coluna in variaveis_disponiveis:
    if coluna not in variaveis_analisar:
      X_empreendedor.drop(coluna, axis=1, inplace=True)
    
  # Modulos 6 Colab - Treinar o modelo
  # Modulos 7 Colab - Aplicar o modelo
    # avaliacao_investidor = predict
  if (avaliacao_investidor):
    melhor_match.append(potencial_investidor)
  # else:
    # Melhoria: print da árvore de classificação das teses que não passou