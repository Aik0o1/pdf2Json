import streamlit as st
from modules.estruturacao import extrair_dados_estruturados

st.title("Pdf2Json")


abas = st.tabs(["aba1", "aba2"])
with abas[0]:

    arquivos = st.file_uploader("Escolha os documentos", 
                            accept_multiple_files=True, 
                            type="pdf")


    if arquivos:
        for arquivo in arquivos:

            extrair_dados_estruturados(arquivos[0])

