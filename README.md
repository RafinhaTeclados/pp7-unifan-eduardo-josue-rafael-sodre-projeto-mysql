# Sistema de Estoque e Atendimento (PP7)

Projeto da turma **pp7** — refatoração do sistema de estoque e atendimento do semestre passado,
agora com dados guardados em **MySQL**, organizado em **MVC + Repository** (só com funções,
como no exemplo da aula) e com interface em **CustomTkinter**.

## Integrantes

- Eduardo Araújo de Lima — @earauj4152lima-ux
- Josué Calebe Alves Santos — @Calebebatera
- Rafael Sodré Nunes Marques Dourado — @RafinhaTeclados

## O que o sistema faz

Controla o estoque de uma loja e o atendimento aos clientes.
O banco segue o DER do grupo: **Lojista**, **Mercadoria**, **Cliente** (com telefones),
**Atendimento** (fila) e **Item de atendimento** (relação N:N entre atendimento e mercadoria).

Nesta versão, o **CRUD completo** (cadastrar, listar, alterar e excluir) é da entidade **Mercadoria**:

- **Novo**: limpa o formulário para cadastrar outra mercadoria.
- **Salvar**: cadastra (se nenhuma linha estiver selecionada) ou altera (se houver).
- **Clique numa linha da tabela**: mostra a mercadoria no formulário (a referência fica travada).
- **Excluir**: apaga a mercadoria selecionada, depois de pedir confirmação.
- Erros (dado inválido, referência repetida, mercadoria já usada em atendimento, MySQL fora do ar)
  aparecem em caixas de mensagem (`messagebox`).

## Como executar

1. Tenha instalados o **Python 3.10+** e o **MySQL 8.0.16+** (com o MySQL Workbench).
2. Instale as bibliotecas:
   ```
   pip install -r requirements.txt
   ```
3. Crie o banco e as tabelas. No MySQL Workbench, abra e execute (raio) **nesta ordem**:
   1. `database/banco.sql` — cria o banco `estoque_atendimento` e as tabelas
   2. `database/seed.sql` — insere os dados de exemplo (inclui os lojistas, necessários para cadastrar mercadorias)
4. Configure o acesso ao MySQL: copie `.env.example` para `.env` e troque `sua_senha_aqui` pela senha do **seu** MySQL.
5. Rode o sistema **de dentro da pasta do projeto**:
   ```
   python main.py
   ```

Para testar só a camada do banco, sem tela: `python teste_repository.py`.

## Estrutura do projeto

```
main.py                                # dá a partida: controller.iniciar() e abre a janela
database/
  banco.sql                            # cria o banco e as tabelas do DER
  seed.sql                             # dados de exemplo
  conexao.py                           # conexão com o MySQL (dados vêm do .env)
models/mercadoria_model.py             # REGRAS: validar_mercadoria() (sem tela, sem banco)
views/mercadoria_view.py               # TELA em CustomTkinter (sem SQL, sem validação)
controllers/mercadoria_controller.py   # o que fazer em cada clique
repositories/mercadoria_repository.py  # ÚNICO lugar com SQL (mercadoria)
repositories/lojista_repository.py     # lista os lojistas para a caixa de escolha
pp1_legado/                            # código original do PP1 (dados só em memória)
```

A tela nunca acessa o banco: **View → Controller → Repository → MySQL**.
O Controller usa o **Model** para conferir os dados antes de gravar.

## Uso de IA

O esqueleto inicial do projeto (estrutura de pastas, `banco.sql`, `seed.sql`, `conexao.py`, Model, Repository, Controller e View na parte de mercadorias) foi gerado com apoio do **Claude (Anthropic)**, seguindo o exemplo de MVC + Repository do professor, e revisado pelo grupo.

## Status

- [x] Script do banco (`banco.sql`) e dados de exemplo (`seed.sql`)
- [x] Conexão com o MySQL
- [x] Model, Repository e Controller da Mercadoria
- [x] Tela em CustomTkinter (formulário, tabela, botões)
- [x] Tratamento de exceções com `messagebox`
- [x] Testar tudo no MySQL real (grupo)
- [x] Preencher integrantes e conferir a seção "Uso de IA"
