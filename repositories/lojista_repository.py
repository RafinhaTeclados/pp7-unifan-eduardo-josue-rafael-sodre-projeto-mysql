# lojista_repository.py  -  REPOSITORY (só leitura, por enquanto)
# Serve para preencher a caixa de escolha "Lojista responsável" no formulário
# de Mercadoria, já que mercadoria.login_lojista é uma chave estrangeira.

from database.conexao import conectar


def listar():
    """Devolve os lojistas: uma lista de tuplas (login, nome_completo)."""
    sql = "SELECT login, CONCAT_WS(' ', prenome, sobrenome) FROM lojista ORDER BY prenome"
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()
