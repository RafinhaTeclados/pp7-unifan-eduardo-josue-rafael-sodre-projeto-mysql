# main.py
# Ponto de partida do programa.
# Execute DE DENTRO da pasta do projeto:  python main.py

from views import mercadoria_view as view
from controllers import mercadoria_controller as controller

if __name__ == "__main__":
    controller.iniciar()
    view.janela.mainloop()
