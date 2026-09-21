from models.receita import Receita
from models.despesa import Despesa
from models.meta import MetaFinanceira

from database.database import (
    criar_tabelas,
    salvar_receita,
    salvar_despesa,
    buscar_receitas,
    buscar_despesas,
    buscar_despesas_por_categoria,
    salvar_meta,
    buscar_metas
)

from relatorios.graficos import (
    grafico_gastos_categoria,
    grafico_receitas_despesas,
    grafico_evolucao_saldo
)


criar_tabelas()


receitas = []
despesas = []
metas = []


def carregar_dados():
    receitas_banco = buscar_receitas()
    despesas_banco = buscar_despesas()
    metas_banco = buscar_metas()

    for receita in receitas_banco:
        nova_receita = Receita(
            receita[0],
            receita[1],
            receita[2],
            receita[3]
        )

        receitas.append(nova_receita)

    for despesa in despesas_banco:
        nova_despesa = Despesa(
            despesa[0],
            despesa[1],
            despesa[2],
            despesa[3]
        )

        despesas.append(nova_despesa)

    for meta in metas_banco:
        nova_meta = MetaFinanceira(
            meta[0],
            meta[1],
            meta[2]
        )

        metas.append(nova_meta)


def cadastrar_receita():
    print("\n=== NOVA RECEITA ===")

    descricao = input("Descrição: ")
    valor = float(input("Valor: R$ "))
    data = input("Data: ")
    categoria = input("Categoria: ")

    nova_receita = Receita(
        descricao,
        valor,
        data,
        categoria
    )

    receitas.append(nova_receita)

    salvar_receita(
        descricao,
        valor,
        data,
        categoria
    )

    print("\nReceita cadastrada com sucesso!")


def cadastrar_despesa():
    print("\n=== NOVA DESPESA ===")

    descricao = input("Descrição: ")
    valor = float(input("Valor: R$ "))
    data = input("Data: ")
    categoria = input("Categoria: ")

    nova_despesa = Despesa(
        descricao,
        valor,
        data,
        categoria
    )

    despesas.append(nova_despesa)

    salvar_despesa(
        descricao,
        valor,
        data,
        categoria
    )

    print("\nDespesa cadastrada com sucesso!")


def mostrar_resumo():
    total_receitas = sum(receita.valor for receita in receitas)
    total_despesas = sum(despesa.valor for despesa in despesas)

    saldo = total_receitas - total_despesas

    print("\n=== RESUMO FINANCEIRO ===")
    print(f"Total de receitas: R$ {total_receitas:.2f}")
    print(f"Total de despesas: R$ {total_despesas:.2f}")
    print(f"Saldo atual: R$ {saldo:.2f}")


def mostrar_movimentacoes():
    print("\n=== MOVIMENTAÇÕES ===")

    if len(receitas) == 0:
        print("\nNenhuma receita cadastrada.")
    else:
        print("\nRECEITAS:")

        for receita in receitas:
            print(
                f"{receita.descricao} | "
                f"R$ {receita.valor:.2f} | "
                f"{receita.data} | "
                f"{receita.categoria}"
            )

    if len(despesas) == 0:
        print("\nNenhuma despesa cadastrada.")
    else:
        print("\nDESPESAS:")

        for despesa in despesas:
            print(
                f"{despesa.descricao} | "
                f"R$ {despesa.valor:.2f} | "
                f"{despesa.data} | "
                f"{despesa.categoria}"
            )


def filtrar_despesas():
    print("\n=== FILTRAR DESPESAS ===")

    categoria = input("Digite a categoria: ")

    resultados = buscar_despesas_por_categoria(categoria)

    if len(resultados) == 0:
        print("\nNenhuma despesa encontrada nessa categoria.")
        return

    print(f"\nDESPESAS - {categoria.upper()}")

    total = 0

    for despesa in resultados:
        print(
            f"{despesa[0]} | "
            f"R$ {despesa[1]:.2f} | "
            f"{despesa[2]}"
        )

        total += despesa[1]

    print(f"\nTotal da categoria: R$ {total:.2f}")


def cadastrar_meta():
    print("\n=== NOVA META FINANCEIRA ===")

    nome = input("Nome da meta: ")
    valor_objetivo = float(input("Valor objetivo: R$ "))
    valor_atual = float(input("Valor já guardado: R$ "))

    nova_meta = MetaFinanceira(
        nome,
        valor_objetivo,
        valor_atual
    )

    metas.append(nova_meta)

    salvar_meta(
        nome,
        valor_objetivo,
        valor_atual
    )

    print("\nMeta cadastrada com sucesso!")


def mostrar_metas():
    print("\n=== METAS FINANCEIRAS ===")

    if len(metas) == 0:
        print("\nNenhuma meta cadastrada.")
        return

    for meta in metas:
        falta = meta.valor_objetivo - meta.valor_atual

        if meta.valor_objetivo > 0:
            percentual = (
                meta.valor_atual / meta.valor_objetivo
            ) * 100
        else:
            percentual = 0

        if falta < 0:
            falta = 0

        print("\n------------------------------")
        print(f"Meta: {meta.nome}")
        print(f"Objetivo: R$ {meta.valor_objetivo:.2f}")
        print(f"Guardado: R$ {meta.valor_atual:.2f}")
        print(f"Falta: R$ {falta:.2f}")
        print(f"Progresso: {percentual:.1f}%")


def mostrar_graficos():
    while True:
        print("\n=== RELATÓRIOS E GRÁFICOS ===")
        print("1 - Gastos por categoria")
        print("2 - Receitas x Despesas")
        print("3 - Evolução do saldo")
        print("4 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            grafico_gastos_categoria()

        elif opcao == "2":
            grafico_receitas_despesas()

        elif opcao == "3":
            grafico_evolucao_saldo()

        elif opcao == "4":
            break

        else:
            print("\nOpção inválida. Tente novamente.")


carregar_dados()


while True:
    print("\n=== FINANCONTROL ===")
    print("1 - Cadastrar receita")
    print("2 - Cadastrar despesa")
    print("3 - Ver resumo financeiro")
    print("4 - Ver movimentações")
    print("5 - Filtrar despesas por categoria")
    print("6 - Cadastrar meta financeira")
    print("7 - Ver metas financeiras")
    print("8 - Ver relatórios e gráficos")
    print("9 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        cadastrar_receita()

    elif opcao == "2":
        cadastrar_despesa()

    elif opcao == "3":
        mostrar_resumo()

    elif opcao == "4":
        mostrar_movimentacoes()

    elif opcao == "5":
        filtrar_despesas()

    elif opcao == "6":
        cadastrar_meta()

    elif opcao == "7":
        mostrar_metas()

    elif opcao == "8":
        mostrar_graficos()

    elif opcao == "9":
        print("\nPrograma encerrado.")
        break

    else:
        print("\nOpção inválida. Tente novamente.")