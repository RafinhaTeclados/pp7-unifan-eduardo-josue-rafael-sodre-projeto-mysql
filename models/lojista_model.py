# Valida os dados do login e transforma a senha em hash
import hashlib

def validar_login(login, senha):
    if login == "":
        return("Informe o login.")
    elif len(login) > 30:
        return("O login pode ter no máximo 30 caracteres.")
    elif senha == "":
        return("Informe a senha.")
    else:
        return None

def gerar_hash_senha(senha):
    senha_hash = hashlib.sha256(senha.encode("utf-8")).hexdigest()
    return senha_hash