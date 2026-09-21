import sqlite3
import os
import matplotlib.pyplot as plt


def conectar():
    caminho_banco = os.path.join(
        os.path.dirname(__file__),
        "..",
        "database",
        "financontrol.db"
    )

    return sqlite3.connect(caminho_banco)


def grafico_gastos_categoria():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT categoria, SUM(valor)
        FROM despesas
        GROUP BY categoria
    """)

    dados = cursor.fetchall()
    conexao.close()

    if len(dados) == 0:
        print("Não existem despesas cadastradas.")
        return

    categorias = [item[0] for item in dados]
    valores = [item[1] for item in dados]

    plt.figure(figsize=(8, 6))

    plt.pie(
        valores,
        labels=categorias,
        autopct="%1.1f%%"
    )

    plt.title("Gastos por Categoria")

    plt.show()


def grafico_receitas_despesas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT SUM(valor)
        FROM receitas
    """)

    resultado_receitas = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(valor)
        FROM despesas
    """)

    resultado_despesas = cursor.fetchone()[0] or 0

    conexao.close()

    nomes = ["Receitas", "Despesas"]
    valores = [resultado_receitas, resultado_despesas]

    plt.figure(figsize=(8, 6))

    plt.bar(
        nomes,
        valores
    )

    plt.title("Receitas x Despesas")
    plt.ylabel("Valor (R$)")

    plt.show()


def grafico_evolucao_saldo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT data, valor
        FROM receitas
        ORDER BY data
    """)

    receitas = cursor.fetchall()

    cursor.execute("""
        SELECT data, valor
        FROM despesas
        ORDER BY data
    """)

    despesas = cursor.fetchall()

    conexao.close()

    movimentacoes = []

    for data, valor in receitas:
        movimentacoes.append(
            (data, valor)
        )

    for data, valor in despesas:
        movimentacoes.append(
            (data, -valor)
        )

    movimentacoes.sort()

    if len(movimentacoes) == 0:
        print("Não existem movimentações cadastradas.")
        return

    datas = []
    saldos = []

    saldo = 0

    for data, valor in movimentacoes:
        saldo += valor

        datas.append(data)
        saldos.append(saldo)

    plt.figure(figsize=(10, 6))

    plt.plot(
        datas,
        saldos,
        marker="o"
    )

    plt.title("Evolução do Saldo")
    plt.xlabel("Data")
    plt.ylabel("Saldo (R$)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    grafico_evolucao_saldo()