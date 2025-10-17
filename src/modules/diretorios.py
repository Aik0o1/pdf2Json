import os
import shutil

def criarPasta(path):
    os.mkdir(path)

def verificarDiretorios(path):
    paths = os.listdir()
    print(paths)

    if path not in paths:
        print(f"Diretorio {path} inexistente")

verificarDiretorios("rr")

