"""Abre a conexão com o MySQL.

Os dados de acesso (usuário, senha...) ficam no arquivo .env, que NÃO vai
para o GitHub (está no .gitignore). Use o .env.example como modelo.
"""
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env, se existir


def conectar():
    """Devolve uma conexão nova com o banco.

    Se o MySQL estiver desligado ou a senha estiver errada, o
    mysql.connector lança um erro. Quem chama (a View) captura esse erro
    e mostra a mensagem na tela.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "estoque_atendimento"),
    )
