# mercadoria_model.py  -  MODEL
# As REGRAS da mercadoria (validação dos dados digitados).
# Este arquivo não sabe nada de tela nem de banco de dados: é Python puro.

from decimal import Decimal, InvalidOperation

QUANTIDADE_MAXIMA = 2147483647           # limite do INT do MySQL
PRECO_MAXIMO = Decimal("99999999.99")    # limite do DECIMAL(10,2)


def texto_para_quantidade(texto):
    """Converte o texto digitado em número inteiro (0 ou mais).
    Devolve None se o texto não for um número inteiro válido."""
    texto = texto.strip()
    if not texto.isdecimal():            # só dígitos: recusa vazio, "-3", "2,5", "abc"
        return None
    quantidade = int(texto)
    if quantidade > QUANTIDADE_MAXIMA:
        return None
    return quantidade


def texto_para_preco(texto):
    """Converte o texto digitado em Decimal (0 ou mais, até 2 casas).
    Aceita vírgula ou ponto ("12,50" ou "12.50").
    Devolve None se o texto não for um preço válido."""
    texto = texto.strip().replace(",", ".")
    try:
        preco = Decimal(texto)
    except InvalidOperation:
        return None
    if not preco.is_finite() or preco < 0 or preco > PRECO_MAXIMO:
        return None
    if preco != preco.quantize(Decimal("0.01")):   # mais de 2 casas decimais
        return None
    return preco


def validar_mercadoria(referencia, nome, quantidade, preco, login_lojista):
    """Confere os dados da mercadoria (todos chegam como texto da tela).
    Devolve uma mensagem de erro, ou None se estiver tudo certo."""
    if referencia == "":
        return "Informe a referência."
    if len(referencia) > 20:
        return "A referência pode ter no máximo 20 caracteres."
    if len(nome) < 3:
        return "O nome precisa ter pelo menos 3 letras."
    if len(nome) > 100:
        return "O nome pode ter no máximo 100 caracteres."
    if texto_para_quantidade(quantidade) is None:
        return "A quantidade precisa ser um número inteiro (0 ou mais)."
    if texto_para_preco(preco) is None:
        return "O preço precisa ser um número de 0 em diante, com até 2 casas decimais (ex.: 12,50)."
    if login_lojista == "":
        return "Escolha o lojista responsável."
    return None
