# -*- coding: utf-8 -*-

# %%writefile app.py
import streamlit as st

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
			st.header("Nos conte mais de sua tese de investimentos")
			with st.form("cadastro", clear_on_submit=True):
				nome = st.text_input("Nome:")
				email = st.text_input("Email:")
				telefone = st.text_input("Telefone:")

				st.checkbox('Concordo em compartilhar essas informações e sei que o projeto armazenará os dados de minha tese anonimizados, não sendo permitido o compartilhamento dos mesmos.')
				submit = st.form_submit_button("Fazer cadastro")

		elif perfil == 'Empreendedor':
			st.header("Nos conte mais de sua empresa")
		else:
			st.write("Basta escolher na lista acima, o perfil que melhor se encaixa e iniciaremos a configuração de sua conta.")

	if choice == 'About':
		st.subheader("O projeto é da Aline, Camila e Vinicius para o TCC da Escola Politécnica 2022, departamento PCS.")

if __name__ == '__main__':
	main()
