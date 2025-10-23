import streamlit as st
from modules.estruturacao import extrair_dados_estruturados
from modules.config import listarDocs, retornarConteudoDoc

st.set_page_config(page_title="Pdf2Json", layout="wide")
st.title("Pdf2Json")

abas = st.tabs(["Upload de PDFs", "Documentos Salvos"])

# Aba 1
with abas[0]:
    st.subheader("Envie seus documentos PDF")

    arquivos = st.file_uploader(
        "Selecione um ou mais PDFs",
        accept_multiple_files=True,
        type="pdf"
    )

    if arquivos:
        progresso = st.progress(0)
        total = len(arquivos)
        for i, arquivo in enumerate(arquivos, start=1):
            with st.expander(f"{arquivo.name}"):
                st.info("Processando documento...")
                extrair_dados_estruturados(arquivo)
                st.success(f"✅ {arquivo.name} processado com sucesso!")

            arquivo.close()
            del arquivo
            progresso.progress(i / total)

        st.success("Todos os documentos foram processados!")

# Aba 2
with abas[1]:
    st.subheader("Documentos armazenados no banco de dados")

    documentosNoBanco = listarDocs()

    if not documentosNoBanco:
        st.info("Nenhum documento encontrado.")
    else:
        doc_id = st.selectbox(
            "Selecione um documento para visualizar:",
            documentosNoBanco,
            index=None,
            placeholder="Escolha um documento..."
        )

        if doc_id:
            conteudo = retornarConteudoDoc(doc_id)
            st.json(conteudo)
