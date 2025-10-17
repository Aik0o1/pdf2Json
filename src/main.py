import ollama
import json
import fitz  
import os
from modules.config import salvarNoBanco
import uuid 

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um arquivo PDF."""
    if not os.path.exists(caminho_pdf):
        print(f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.")
        return None
    
    texto_completo = ""
    try:
        with fitz.open(caminho_pdf) as doc:
            for pagina in doc:
                texto_completo += pagina.get_text("text")
        return texto_completo
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return None

nome_arquivo_pdf = "./documentos/0197359.pdf" 
nome_arquivo_saida = "./jsons/resultado_ia.json"

texto_documento = extrair_texto_pdf(nome_arquivo_pdf)

if texto_documento:
    print("--- Texto extraído do PDF ---")
    # print(texto_documento[:500] + "...") 
    print("\n--- Enviando para a IA para estruturação ---")

    prompt_template = f"""
    Você é um assistente de IA especialista em análise e digitalização de documentos. Sua principal tarefa é ler o texto do documento fornecido e extrair **ABSOLUTAMENTE TODAS as informações**, convertendo-as em um formato JSON detalhado, completo e hierárquico.

    **Não resuma ou omita nenhuma informação.** Seu objetivo é criar uma representação digital exata do documento.

    **Instrução de Prioridade:** A primeira e mais importante informação a ser extraída é o número de **protocolo** do documento, se existir. Este valor deve ser colocado em uma chave de nível superior chamada "protocolo". Este campo é crucial, pois será usado para identificar o documento em um banco de dados CouchDB. Se o documento não tiver um número de protocolo explícito, essa chave deve ser omitida do JSON.

    Depois de tratar do protocolo, analise o restante do conteúdo para capturar cada detalhe, desde o cabeçalho até o rodapé, incluindo todos os parágrafos, listas, tabelas e metadados visíveis. Crie um esquema JSON que espelhe a estrutura do documento original, usando chaves (keys) claras e descritivas e aninhando os dados de forma lógica.

    A sua resposta deve ser **APENAS o código JSON VÁLIDO**. Não inclua nenhuma explicação, comentário, introdução ou a formatação ```json` antes ou depois do código. Não esqueça, estruture todas as informações do documento, sem exceção.

    Aqui está o texto do documento para análise:
    ---
    {texto_documento}
    ---
"""
    try:
        response = ollama.chat(
            model='llama3', 
            messages=[{'role': 'user', 'content': prompt_template}],
            format='json',
            options={'temperature': 0.0} 
        )

        # Extrair e processar o JSON
        json_output = response['message']['content']
        json_output = json_output.strip().replace("```json", "").replace("```", "")
        
        dados_estruturados_ia = json.loads(json_output)
        
        # with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
        #     json.dump(dados_estruturados_ia, f, ensure_ascii=False, indent=4) 
        # print(f"Arquivo '{nome_arquivo_saida}' salvo com sucesso!")

 
        doc_id = dados_estruturados_ia.get('protocolo', str(uuid.uuid4()))
        
        salvarNoBanco(doc_id, dados_estruturados_ia)

    except json.JSONDecodeError as e:
        print(f"\n--- ERRO ---")
        print(f"A IA retornou um JSON inválido. Erro: {e}")
        print("Resposta recebida da IA:")
        print(response['message']['content'])
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

