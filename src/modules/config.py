from dotenv import load_dotenv
import couchdb
import os
from urllib.parse import quote

load_dotenv()
password = os.getenv("SENHA")
encoded_password = quote(password)
couch = couchdb.Server(f'http://admin:{encoded_password}@{os.getenv("IP")}')

db_name = "dados_documentos"
db = couch[db_name]
print(db)


def salvarNoBanco(id, dados_documento):
    if id in db:
        doc = db[id]
        print(f" Documento existente encontrado: {id}")
    else:
        doc = {"_id": id}

    doc["documento"] = dados_documento
    

    db.save(doc)
    print(f"✅ Documento salvo no CouchDB com id {id}")


def listarDocs():
    return db

def retornarConteudoDoc(id):
    return db[id]