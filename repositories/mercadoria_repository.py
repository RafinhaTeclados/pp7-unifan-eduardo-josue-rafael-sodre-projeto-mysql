# O ÚNICO arquivo que conversa com o banco de dados sobre mercadorias.
# O resto do sistema só chama estas funções e nunca escreve SQL.
# Cada mercadoria é uma tupla: (referencia, nome, quantidade, preco, login_lojista)

import mysql.connector
from database.conexao import conectar


def listar():
    """Devolve todas as mercadorias: uma lista de tuplas, em ordem de nome."""
    sql = ("SELECT referencia, nome, quantidade, preco, login_lojista "
           "FROM mercadoria ORDER BY nome")
    return _consultar(sql, ())


def buscar_por_referencia(referencia):
    """Devolve uma mercadoria (tupla) ou None se não encontrar."""
    sql = ("SELECT referencia, nome, quantidade, preco, login_lojista "
           "FROM mercadoria WHERE referencia = %s")
    linhas = _consultar(sql, (referencia,))
    if len(linhas) == 0:
        return None
    return linhas[0]


def adicionar(referencia, nome, quantidade, preco, login_lojista):
    """Cadastra uma mercadoria. Devolve True se deu certo,
    ou False se a referência já existe (ou o lojista não existe)."""
    sql = ("INSERT INTO mercadoria (referencia, nome, quantidade, preco, login_lojista) "
           "VALUES (%s, %s, %s, %s, %s)")
    return _executar(sql, (referencia, nome, quantidade, preco, login_lojista))


def atualizar(referencia, nome, quantidade, preco, login_lojista):
    """Altera uma mercadoria pela referência (a referência em si não muda).
    Devolve True se deu certo, ou False se o banco recusou os dados."""
    sql = ("UPDATE mercadoria SET nome = %s, quantidade = %s, preco = %s, login_lojista = %s "
           "WHERE referencia = %s")
    return _executar(sql, (nome, quantidade, preco, login_lojista, referencia))


def remover(referencia):
    """Apaga uma mercadoria. Devolve True se deu certo, ou False se ela já
    foi usada em algum atendimento (o MySQL recusa: ON DELETE RESTRICT)."""
    return _executar("DELETE FROM mercadoria WHERE referencia = %s", (referencia,))


# ---------- funções de apoio (uso só neste arquivo) ----------

def _consultar(sql, valores):
    """SELECT: conectar -> cursor -> execute -> ler -> fechar."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, valores)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()


def _executar(sql, valores):
    """INSERT / UPDATE / DELETE: executa e confirma (commit).
    Devolve True se deu certo e False se o banco recusou (IntegrityError)."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        deu_certo = True
    except mysql.connector.IntegrityError:
        conexao.rollback()
        deu_certo = False
    finally:
        cursor.close()
        conexao.close()
    return deu_certo
