# Agora temos leitura e login :D
from database.conexao import conectar


def listar():
    # Devolve os lojistas: uma lista de tuplas (login, nome_completo).
    sql = "SELECT login, CONCAT_WS(' ', prenome, sobrenome) FROM lojista ORDER BY prenome"
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

def autenticar(login, senha_hash):
    sql = ("""SELECT login, CONCAT_WS(' ', prenome, sobrenome), funcao
    FROM lojista WHERE login = %s AND senha = %s""")

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, (login, senha_hash))
        return cursor.fetchone()
    finally:
        cursor.close()
        conexao.close()
