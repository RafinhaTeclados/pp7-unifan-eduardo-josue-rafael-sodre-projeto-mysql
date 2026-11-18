# lojista_view.py  -  VIEW
# A tela de login do lojista (CustomTkinter). Só desenha e mostra coisas.
# Não valida dados e não acessa o banco: quem decide é o Controller.

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

LARGURA = 380
ALTURA = 340

janela = ctk.CTk()
janela.title("Login do Lojista")
janela.geometry(f"{LARGURA}x{ALTURA}")
janela.resizable(False, False)
janela.grid_columnconfigure(0, weight=1)

# Centraliza a janela na tela
janela.update_idletasks()
_x = (janela.winfo_screenwidth() - LARGURA) // 2
_y = (janela.winfo_screenheight() - ALTURA) // 2
janela.geometry(f"{LARGURA}x{ALTURA}+{_x}+{_y}")

# ---------- Título ----------
ctk.CTkLabel(janela, text="Sistema de Estoque e Atendimento",
             font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=(24, 2))
ctk.CTkLabel(janela, text="Entre com o seu login de lojista",
             text_color="gray70").grid(row=1, column=0, pady=(0, 14))

# ---------- Formulário ----------
quadro_formulario = ctk.CTkFrame(janela)
quadro_formulario.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 12))
quadro_formulario.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(quadro_formulario, text="Login").grid(row=0, column=0, sticky="w", padx=14, pady=(12, 0))
entrada_login = ctk.CTkEntry(quadro_formulario, placeholder_text="Ex.: eduardo")
entrada_login.grid(row=1, column=0, sticky="ew", padx=14, pady=(2, 6))

ctk.CTkLabel(quadro_formulario, text="Senha").grid(row=2, column=0, sticky="w", padx=14)
entrada_senha = ctk.CTkEntry(quadro_formulario, show="*")
entrada_senha.grid(row=3, column=0, sticky="ew", padx=14, pady=(2, 6))

# Caixa "Mostrar senha": troca show="*" por show="" (e vice-versa)
marcador_mostrar_senha = ctk.CTkCheckBox(quadro_formulario, text="Mostrar senha")
marcador_mostrar_senha.grid(row=4, column=0, sticky="w", padx=14, pady=(2, 12))

botao_entrar = ctk.CTkButton(janela, text="Entrar")
botao_entrar.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 20))


# ---------- Funções para o Controller ----------

def _alternar_senha():
    """Mostra ou esconde a senha digitada (só mexe na tela)."""
    if marcador_mostrar_senha.get() == 1:
        entrada_senha.configure(show="")
    else:
        entrada_senha.configure(show="*")


def ligar_botoes(funcao_entrar):
    """Diz qual função do Controller o botão Entrar (e a tecla Enter) devem chamar."""
    botao_entrar.configure(command=funcao_entrar)          # CTk usa configure(), não config()
    # O Tkinter sempre manda o 'evento' no bind, por isso o lambda
    entrada_login.bind("<Return>", lambda evento: funcao_entrar())
    entrada_senha.bind("<Return>", lambda evento: funcao_entrar())
    marcador_mostrar_senha.configure(command=_alternar_senha)


def ler_formulario():
    """Devolve o que foi digitado: login (sem espaços nas pontas) e senha (como digitada)."""
    login = entrada_login.get().strip()
    senha = entrada_senha.get()
    return login, senha


def limpar_senha():
    entrada_senha.delete(0, "end")


def focar_login():
    entrada_login.focus()


def focar_senha():
    entrada_senha.focus()


def fechar():
    """Fecha a tela de login. O mainloop() termina e o main.py segue em frente."""
    janela.destroy()


def mostrar_erro(mensagem):
    messagebox.showerror("Erro", mensagem)