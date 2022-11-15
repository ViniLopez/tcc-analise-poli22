# -*- coding: utf-8 -*-

# %%writefile app.py
import streamlit as st
import pandas as pd

def main():
	st.title("TCC - AUTOMATIZAÇÃO DE ANÁLISE DE EMPRESAS PARA AUXÍLIO DE DECISÃO DE INVESTIMENTOS")
	st.subheader("Ferramenta de suporte para decisão de investimento em startups a partir de Machine Learning")
	pages = ["Home", "About"]
	choice = st.sidebar.selectbox('Menu', pages)

	if choice == 'Home':
		st.subheader("Página inicial do projeto")
		st.write("Bem-vindo ao projeto, primeiramente nos diga, quem é você:")
		perfil = st.selectbox('Eu sou:', ['Investidor', 'Empreendedor'])

		if perfil == 'Investidor':
			with st.form("Nos conte mais sobre você:", clear_on_submit=True):
				nome = st.text_input("Nome:")
				email = st.text_input("Email:")
				telefone = st.text_input("Telefone:")

				submit = st.form_submit_button("Fazer cadastro")

				if submit:
					st.success('Cadastro concluído com sucesso!')
					
			with st.form("Agora, sobre sua tese de investimentos", clear_on_submit=True):
				tese = st.file_uploader('Faça upload das últimas empresas que você analisou aqui: (CSV)', type='csv')
				submit = st.form_submit_button("Começar análise")
				aceito_lgpd = st.checkbox('Concordo em compartilhar essas informações e sei que o projeto armazenará os dados de minha tese anonimizados, não sendo permitido o compartilhamento dos mesmos.')
				if (submit and aceito_lgpd):
					st.success('Cadastro concluído com sucesso!')
					
			tese = pd.DataFrame(tese)
			st.write(tese.head)

		elif perfil == 'Empreendedor':
			st.header("Nos conte mais de sua empresa")
		else:
			st.write("Basta escolher na lista acima, o perfil que melhor se encaixa e iniciaremos a configuração de sua conta.")

	if choice == 'About':
		st.subheader("O projeto é da Aline, Camila e Vinicius para o TCC da Escola Politécnica 2022, departamento PCS.")

if __name__ == '__main__':
	main()
