from collections import deque
#Estrutura de dados completa adicionada
estoque_lista = []      
estoque_dict = {}
fila_atendimento = deque()

def cadastra_mercadoria():     #Estrutura atualizada: verificar se item já existe e adicionar em lista e 
    print("\n--- CADASTRAR MERCADORIA ---")
    referencia = input("Digite a referência/código único da mercadoria: ").strip()       
                        #.strip é pra remover espaços extras depois ou antes do dado   
    
    if referencia in estoque_dict:
        print("Erro: Já existe uma mercadoria com essa referência!")
        return

    nome = input("Digite o nome da mercadoria: ").strip()
    quantidade = int(input("Digite a quantidade da mercadoria: "))
    preco = float(input("Preço: R$ "))

    mercadoria = {
        "Referência": referencia,
        "Nome": nome,
        "Quantidade": quantidade,
        "Preço": preco
    }

    estoque_lista.append(mercadoria)
    estoque_dict[referencia] = mercadoria
    print("Mercadoria cadastrada com sucesso!")

def listar_mercadoria():
    print("\n--- ESTOQUE COMPLETO ---")
    if len(estoque_lista) == 0:
        print("Estoque vazio.")
    else:
        for produto in estoque_lista:
            print(f"Referência: {produto['Referência']}")
            print(f"Produto: {produto['Nome']}")
            print(f"Quantidade: {produto['Quantidade']}")
            print(f"Preço: R$ {produto['Preço']:.2f}")
            print("-----------------------")


def consultar_produto():
    print("\n--- CONSULTAR PRODUTO POR CÓDIGO/REF ---")
    ref = input("Digite a referência da mercadoria: ").strip()

    #Busca direta via dicionário
    if ref in estoque_dict:
        produto = estoque_dict[ref]
        print("\nProduto encontrado:")
        print(f"Referência: {produto['Referência']}")
        print(f"Nome: {produto['Nome']}")
        print(f"Quantidade: {produto['Quantidade']}")
        print(f"Preço: R$ {produto['Preço']:.2f}")
    else:
        print("Produto não encontrado.")

def atualizar_produto():
    listar_mercadoria()           #Mostrar o que tem pra facilitar a mudança
    print("\n--- ATUALIZAR PRODUTO ---")
    ref = input("Digite a referência/código do produto que deseja alterar: ").strip()

    #Busca direta via dicionário tempo constante O(1)
    if ref in estoque_dict:
        produto = estoque_dict[ref]
        print(f"\nProduto selecionado: {produto['Nome']}")
        print(f"- Quantidade atual: {produto['Quantidade']}")
        print(f"- Preço atual: R$ {produto['Preço']:.2f}")

        print("\nO que você deseja alterar?")
        print("1 - Apenas a Quantidade")
        print("2 - Apenas o Preço")
        print("3 - Quantidade e preço (ambos)")
        
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                nova_qtd = int(input("Digite a nova quantidade: "))
                produto["Quantidade"] = nova_qtd
                print("Quantidade atualizada com sucesso!")

            case "2":
                novo_preco = float(input("Digite o novo preço: R$ "))
                produto["Preço"] = novo_preco
                print("Preço atualizado com sucesso!")

            case "3":
                nova_qtd = int(input("Digite a nova quantidade: "))
                novo_preco = float(input("Digite o novo preço: R$ "))
                produto["Quantidade"] = nova_qtd
                produto["Preço"] = novo_preco
                print("Quantidade e Preço atualizados com sucesso!")

            case _:
                print("Opção inválida! Nenhuma alteração foi feita.")

    else:
        print("Produto não encontrado com essa referência.")

def remover_produto():
    listar_mercadoria()            #Mostrar o que tem pra facilitar a exclusão
    print("\n--- REMOVER PRODUTO ---")
    ref = input("Informe a referência do produto que deseja remover: ").strip()

    if ref in estoque_dict:
        produto = estoque_dict.pop(ref)
        estoque_lista.remove(produto)
        print(f"Produto '{produto['Nome']}' removido com sucesso!")
    else:
        print("Produto não encontrado.")

def inserir_na_fila():
    print("\n--- INSERIR CLIENTE NA FILA DE ATENDIMENTO ---")
    cliente = input("Nome do cliente: ").strip()
    servico = input("Serviço solicitado: ").strip()
    
    fila_atendimento.append({"cliente": cliente, "servico": servico})
    print(f"Cliente '{cliente}' adicionado à fila!")

def processar_fila():
    print("\n--- PROCESSAR ATENDIMENTO ---")
    if fila_atendimento:
        atendimento = fila_atendimento.popleft()
        print(f"Atendendo cliente: {atendimento['cliente']}")
        print(f"Serviço: {atendimento['servico']}")
        print("Atendimento concluído!")
    else:
        print("Fila de atendimento vazia.")

def listar_fila():
    print("\n--- FILA DE ATENDIMENTO ---")
    if not fila_atendimento:
        print("A fila de atendimento está vazia.")
        return

    print("Clientes aguardando atendimento (em ordem de chegada):")
    for posicao, atendimento in enumerate(fila_atendimento, start=1):
        #Destaca o primeiro da fila
        if posicao == 1:
            status = " (PRÓXIMO A SER ATENDIDO)"
        else:
            status = print("") #Se for o próximo, exibe a mensagem, se não, exibe nada
        print(f"{posicao}º - Cliente: {atendimento['cliente']} | Serviço: {atendimento['servico']}{status}")

while True:
    print("\n==== SISTEMA DE ESTOQUE E ATENDIMENTO ====") 
    print("1 - Cadastrar mercadoria")
    print("2 - Listar todas as mercadorias (Lista)")
    print("3 - Consultar por Referência (Dicionário)")
    print("4 - Atualizar produto (Preço/Quantidade)") 
    print("5 - Remover produto")
    print("6 - Inserir cliente na Fila") #Deque
    print("7 - Atender próximo da Fila") #Deque fifo
    print("8 - Listar fila")             #Últimas opções adicionadas
    print("0 - Sair do sistema")

    opcao = input("Escolha sua opção: ").strip()

    match(opcao):           #If else substituido por match case
        case '1':
            cadastra_mercadoria()
        case '2':
            listar_mercadoria()
        case '3':
            consultar_produto()
        case '4':
            atualizar_produto()
        case '5':
            remover_produto()
        case '6':
            inserir_na_fila()
        case '7':
            processar_fila()
        case '8':
            listar_fila()
        case '0':
            print("Saindo do sistema...") #mensagem atualizada
            break
        case _:
            print("Opcão inválida.")




