import streamlit as st

st.title("Sobre o projeto")
st.subheader("Trabalho de conclusão de curso da Aline Tsuruda, Camila Miwa e Vinícius Lopez na Escola Politécnica da USP - 2022")

st.markdown("""---""")
st.write("Este projeto tem o intuito de aplicar os conceitos estudados ao longo do curso de Engenharia Elétrica, ênfase em Computação para a criação de uma ferramenta de suporte à decisão de investimentos.")

st.write("A ferramenta, recebe dos investidores uma tese de investimentos implícita através de um histórico de empresas que já foram previamente analisadas. A partir desses exemplos, faz um tratamento de dados prévio (incluindo rotinas de Data Augmentation e Engenharia de Variáveis) e treina dois algoritmos de Machine Learning Supervisionados para classificação - K-Nearest Neighbours e Random Forest.")
st.write("Em seguida, recebe a descrição de uma empresa candidata para avaliar se a mesma está aderente às teses cadastradas na plataforma.")

st.markdown("""---""")
st.write("Para conhecer mais do projeto, acesse o relatório completo do trabalho disponível em [Relatório TCC](https://docs.google.com/document/d/1jcARZxQTIwcTSX0b9vaBgocrXZKcrAfRFKzAaypXa74/edit?usp=sharing) ou o repositório do projeto final [Github - TCC](https://github.com/ViniLopez/tcc-analise-poli22).")
