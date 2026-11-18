import customtkinter as ctk
from tkinter import ttk, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Estoque - Mercadorias")
janela.geometry("820x600")
janela.minsize(700, 500)
janela.grid_columnconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1)          # a tabela estica com a janela

# Lojistas: o texto que aparece na caixa de escolha <-> o login que vai para o banco
_login_por_texto = {}
_texto_por_login = {}

# ---------- Formulário ----------
quadro_formulario = ctk.CTkFrame(janela)
quadro_formulario.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
quadro_formulario.grid_columnconfigure(1, weight=1)

ctk.CTkLabel(quadro_formulario, text="Referência").grid(row=0, column=0, sticky="w", padx=10, pady=4)
entrada_referencia = ctk.CTkEntry(quadro_formulario, placeholder_text="Ex.: MOU-001")
entrada_referencia.grid(row=0, column=1, sticky="ew", padx=10, pady=4)

ctk.CTkLabel(quadro_formulario, text="Nome").grid(row=1, column=0, sticky="w", padx=10, pady=4)
entrada_nome = ctk.CTkEntry(quadro_formulario)
entrada_nome.grid(row=1, column=1, sticky="ew", padx=10, pady=4)

ctk.CTkLabel(quadro_formulario, text="Quantidade").grid(row=2, column=0, sticky="w", padx=10, pady=4)
entrada_quantidade = ctk.CTkEntry(quadro_formulario)
entrada_quantidade.grid(row=2, column=1, sticky="ew", padx=10, pady=4)

ctk.CTkLabel(quadro_formulario, text="Preço (R$)").grid(row=3, column=0, sticky="w", padx=10, pady=4)
entrada_preco = ctk.CTkEntry(quadro_formulario, placeholder_text="Ex.: 12,50")
entrada_preco.grid(row=3, column=1, sticky="ew", padx=10, pady=4)

ctk.CTkLabel(quadro_formulario, text="Lojista responsável").grid(row=4, column=0, sticky="w", padx=10, pady=4)
caixa_lojista = ctk.CTkComboBox(quadro_formulario, values=[], state="readonly")
caixa_lojista.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
caixa_lojista.set("")

# ---------- Botões ----------
quadro_botoes = ctk.CTkFrame(quadro_formulario, fg_color="transparent")
quadro_botoes.grid(row=5, column=1, sticky="e", padx=10, pady=(6, 10))

botao_novo = ctk.CTkButton(quadro_botoes, text="Novo", width=90)
botao_novo.pack(side="left", padx=4)
botao_salvar = ctk.CTkButton(quadro_botoes, text="Salvar", width=90)
botao_salvar.pack(side="left", padx=4)
botao_excluir = ctk.CTkButton(quadro_botoes, text="Excluir", width=90,
                              fg_color="#B03A2E", hover_color="#8E2E24")
botao_excluir.pack(side="left", padx=4)

# ---------- Tabela ----------
# O CustomTkinter não tem tabela: usamos ttk.Treeview com estilo escuro.
estilo = ttk.Style()
estilo.theme_use("default")                    # aceita as cores personalizadas
estilo.configure("Treeview", background="#2B2B2B", foreground="white",
                 fieldbackground="#2B2B2B", rowheight=28, borderwidth=0)
estilo.map("Treeview", background=[("selected", "#1F6AA5")])
estilo.configure("Treeview.Heading", background="#3A3A3A", foreground="white", relief="flat")

quadro_tabela = ctk.CTkFrame(janela)
quadro_tabela.grid(row=1, column=0, sticky="nsew", padx=12, pady=(6, 12))

tabela = ttk.Treeview(quadro_tabela,
                      columns=("referencia", "nome", "quantidade", "preco", "lojista"),
                      show="headings", height=10)
colunas = [("referencia", "Referência", 110, "w"),
           ("nome", "Nome", 260, "w"),
           ("quantidade", "Qtd", 70, "e"),
           ("preco", "Preço (R$)", 100, "e"),
           ("lojista", "Lojista", 110, "w")]
for coluna, titulo, largura, alinhamento in colunas:
    tabela.heading(coluna, text=titulo)
    tabela.column(coluna, width=largura, anchor=alinhamento)

rolagem = ctk.CTkScrollbar(quadro_tabela, command=tabela.yview)
tabela.configure(yscrollcommand=rolagem.set)
tabela.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=6)
rolagem.pack(side="right", fill="y", pady=6)


# ---------- Funções para o Controller ----------

def ligar_botoes(funcao_novo, funcao_salvar, funcao_excluir, funcao_selecionar):
    """Diz qual função do Controller cada botão deve chamar."""
    botao_novo.configure(command=funcao_novo)          # CTk usa configure(), não config()
    botao_salvar.configure(command=funcao_salvar)
    botao_excluir.configure(command=funcao_excluir)
    tabela.bind("<<TreeviewSelect>>", funcao_selecionar)


def mostrar_lojistas(lojistas):
    """Recebe a lista de tuplas (login, nome_completo) e monta a caixa de escolha."""
    _login_por_texto.clear()
    _texto_por_login.clear()
    for login, nome_completo in lojistas:
        texto = f"{login} - {nome_completo}"
        _login_por_texto[texto] = login
        _texto_por_login[login] = texto
    caixa_lojista.configure(values=list(_login_por_texto.keys()))


def ler_formulario():
    """Devolve o que foi digitado: referencia, nome, quantidade, preco, login do lojista."""
    referencia = entrada_referencia.get().strip()
    nome = entrada_nome.get().strip()
    quantidade = entrada_quantidade.get().strip()
    preco = entrada_preco.get().strip()
    login_lojista = _login_por_texto.get(caixa_lojista.get().strip(), "")
    return referencia, nome, quantidade, preco, login_lojista


def travar_referencia(travar):
    """Ao alterar uma mercadoria, a referência (chave primária) não pode mudar."""
    if travar:
        entrada_referencia.configure(state="disabled")
    else:
        entrada_referencia.configure(state="normal")


def limpar_formulario():
    travar_referencia(False)                   # campo travado não aceita delete()
    entrada_referencia.delete(0, "end")
    entrada_nome.delete(0, "end")
    entrada_quantidade.delete(0, "end")
    entrada_preco.delete(0, "end")
    caixa_lojista.set("")


def preencher_formulario(referencia, nome, quantidade, preco, login_lojista):
    limpar_formulario()
    entrada_referencia.insert(0, referencia)
    entrada_nome.insert(0, nome)
    entrada_quantidade.insert(0, str(quantidade))
    entrada_preco.insert(0, f"{preco:.2f}")
    caixa_lojista.set(_texto_por_login.get(login_lojista, ""))
    travar_referencia(True)


def mostrar_mercadorias(mercadorias):
    """Apaga a tabela e escreve de novo, uma mercadoria por linha."""
    for linha in tabela.get_children():
        tabela.delete(linha)
    for referencia, nome, quantidade, preco, login_lojista in mercadorias:
        # iid=referencia: o identificador da linha é a própria referência
        # (assim "007" não vira o número 7 ao ler a seleção)
        tabela.insert("", "end", iid=referencia,
                      values=(referencia, nome, quantidade, f"{preco:.2f}", login_lojista))


def referencia_selecionada():
    """Devolve a referência da linha clicada na tabela, ou None se nenhuma."""
    selecao = tabela.selection()
    if len(selecao) == 0:
        return None
    return selecao[0]


def desmarcar_tabela():
    tabela.selection_remove(tabela.selection())


def mostrar_erro(mensagem):
    messagebox.showerror("Erro", mensagem)


def mostrar_aviso(mensagem):
    messagebox.showinfo("Pronto", mensagem)


def confirmar(mensagem):
    """Pergunta Sim/Não. Devolve True se o usuário confirmou."""
    return messagebox.askyesno("Confirmar", mensagem)
