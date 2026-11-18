"""Teste manual do Repository, ainda sem tela.

Antes de rodar: execute database/banco.sql e database/seed.sql no MySQL e
configure o arquivo .env. Depois, de dentro da pasta do projeto:
    python teste_repository.py
"""
from repositories import lojista_repository, mercadoria_repository as repositorio


def main():
    try:
        lojistas = lojista_repository.listar()
        if len(lojistas) == 0:
            print("Nenhum lojista no banco. Rode database/seed.sql primeiro.")
            return
        login = lojistas[0][0]

        print("1) Adicionar:      ", repositorio.adicionar("TESTE-001", "Item de teste", 5, 9.90, login))
        print("   Repetida:       ", repositorio.adicionar("TESTE-001", "Item de teste", 5, 9.90, login), "(False = já existe)")
        print("2) Buscar:         ", repositorio.buscar_por_referencia("TESTE-001"))
        print("3) Atualizar:      ", repositorio.atualizar("TESTE-001", "Item alterado", 7, 12.50, login))
        print("   Depois:         ", repositorio.buscar_por_referencia("TESTE-001"))
        print("4) Total na lista: ", len(repositorio.listar()), "mercadorias")
        print("5) Remover:        ", repositorio.remover("TESTE-001"))
        print("   Depois:         ", repositorio.buscar_por_referencia("TESTE-001"))
    except Exception as erro:
        print("Deu erro:", erro)


if __name__ == "__main__":
    main()
