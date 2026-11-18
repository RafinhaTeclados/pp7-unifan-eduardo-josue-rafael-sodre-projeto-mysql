# Ponto de partida do programa.
# Execute DE DENTRO da pasta do projeto:  python main.py

from views import lojista_view as login_view
from controllers import lojista_controller as login_controller

if __name__ == "__main__":
    login_controller.iniciar()
    login_view.janela.mainloop()                  # fica aqui até o login fechar

    if login_controller.obter_lojista_logado() is not None:
        from views import mercadoria_view as view
        from controllers import mercadoria_controller as controller

        controller.iniciar()
        view.janela.mainloop()