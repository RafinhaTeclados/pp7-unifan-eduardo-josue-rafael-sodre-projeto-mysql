# Decide o que acontece quando o usuário clica em algo.
# Conversa com a View (tela), o Model (regras) e o Repository (banco).

from views import mercadoria_view as view
from models import mercadoria_model as model
from repositories import mercadoria_repository as repositorio
from repositories import lojista_repository as lojista_repositorio


def iniciar():
    # Liga os botões, carrega os lojistas e preenche a tabela.
    view.ligar_botoes(novo, salvar, excluir, selecionar)
    try:
        view.mostrar_lojistas(lojista_repositorio.listar())
    except Exception as erro:
        view.mostrar_erro(f"Não foi possível carregar os lojistas.\n\n{erro}")
    atualizar_tabela()


def atualizar_tabela():
    try:
        mercadorias = repositorio.listar()
    except Exception as erro:
        view.mostrar_erro(f"Não foi possível carregar as mercadorias.\n\n{erro}")
        return
    view.mostrar_mercadorias(mercadorias)


def novo():
    # Botão Novo: limpa a tela para cadastrar outra mercadoria.
    view.limpar_formulario()
    view.desmarcar_tabela()


def selecionar(evento):
    """Clique numa linha da tabela: mostra a mercadoria no formulário.
    (o Tkinter sempre manda o 'evento', mesmo que a gente não use)"""
    referencia = view.referencia_selecionada()
    if referencia is None:
        return
    try:
        mercadoria = repositorio.buscar_por_referencia(referencia)
    except Exception as erro:
        view.mostrar_erro(f"Não foi possível buscar a mercadoria.\n\n{erro}")
        return
    if mercadoria is not None:
        view.preencher_formulario(*mercadoria)


def salvar():
    # Botão Salvar: cadastra uma mercadoria nova ou altera a selecionada.
    referencia, nome, quantidade, preco, login_lojista = view.ler_formulario()

    # 1) Pergunta ao Model se os dados estão certos
    erro = model.validar_mercadoria(referencia, nome, quantidade, preco, login_lojista)
    if erro is not None:
        view.mostrar_erro(erro)
        return

    # 2) Converte os textos em números (o Model já garantiu que são válidos)
    quantidade = model.texto_para_quantidade(quantidade)
    preco = model.texto_para_preco(preco)

    # 3) Pede ao Repository para gravar no banco
    try:
        if view.referencia_selecionada() is None:
            deu_certo = repositorio.adicionar(referencia, nome, quantidade, preco, login_lojista)
            mensagem_falha = "Já existe uma mercadoria com essa referência."
        else:
            deu_certo = repositorio.atualizar(referencia, nome, quantidade, preco, login_lojista)
            mensagem_falha = "O banco recusou a alteração. Confira os dados e o lojista escolhido."
    except Exception as erro_banco:
        view.mostrar_erro(f"Erro ao acessar o banco de dados.\n\n{erro_banco}")
        return

    if not deu_certo:
        view.mostrar_erro(mensagem_falha)
        return

    # 4) Atualiza a tela
    view.mostrar_aviso("Mercadoria salva com sucesso!")
    novo()
    atualizar_tabela()


def excluir():
    #Botão Excluir: apaga a mercadoria selecionada (depois de confirmar).
    referencia = view.referencia_selecionada()
    if referencia is None:
        view.mostrar_erro("Clique em uma mercadoria da tabela para excluir.")
        return
    if not view.confirmar(f"Excluir a mercadoria {referencia}?"):
        return

    try:
        deu_certo = repositorio.remover(referencia)
    except Exception as erro:
        view.mostrar_erro(f"Erro ao acessar o banco de dados.\n\n{erro}")
        return

    if not deu_certo:
        view.mostrar_erro("Essa mercadoria já foi usada em um atendimento e não pode ser excluída.")
        return

    view.mostrar_aviso("Mercadoria excluída com sucesso!")
    novo()
    atualizar_tabela()
