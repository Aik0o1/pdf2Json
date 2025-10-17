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

for doc_id in db:
    doc = db[doc_id]
    print(doc)

def salvarNoBanco(id, doc):
    db[id] = doc
    print(f"✅ Documento salvo no CouchDB com id '{id}'")