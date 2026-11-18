# lojista_controller.py  -  CONTROLLER
# Decide o que acontece quando o lojista clica em "Entrar".
# Conversa com a View (tela), o Model (regras) e o Repository (banco).
# Aqui NÃO tem widgets (tela) e NÃO tem SQL.
#
# Erros do banco (MySQL desligado, senha errada no .env...) são capturados
# com try/except e mostrados na tela com view.mostrar_erro().

from views import lojista_view as view
from models import lojista_model as model
from repositories import lojista_repository as repositorio

# Lojista que fez login: tupla (login, nome_completo, funcao), ou None se ninguém entrou.
_lojista_logado = None


def iniciar():
    """Liga o botão Entrar e põe o cursor no campo de login."""
    view.ligar_botoes(entrar)
    view.focar_login()


def obter_lojista_logado():
    """Devolve (login, nome_completo, funcao) de quem entrou, ou None."""
    return _lojista_logado


def entrar():
    """Botão Entrar: confere os dados, consulta o banco e abre o sistema."""
    global _lojista_logado
    login, senha = view.ler_formulario()

    # 1) Pergunta ao Model se os dados estão certos
    erro = model.validar_login(login, senha)
    if erro is not None:
        view.mostrar_erro(erro)
        return

    # 2) A senha nunca vai pura para o banco: o Model gera o hash
    senha_hash = model.gerar_hash_senha(senha)

    # 3) Pede ao Repository para procurar o lojista
    try:
        lojista = repositorio.autenticar(login, senha_hash)
    except Exception as erro_banco:
        view.mostrar_erro(f"Erro ao acessar o banco de dados.\n\n{erro_banco}")
        return

    # 4) Mensagem única: não revela se foi o login ou a senha que errou
    if lojista is None:
        view.mostrar_erro("Login ou senha incorretos.")
        view.limpar_senha()
        view.focar_senha()
        return

    # 5) Deu certo: guarda quem entrou e fecha a tela de login
    _lojista_logado = lojista
    view.fechar()