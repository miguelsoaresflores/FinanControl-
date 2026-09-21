import os
import sqlite3


def conectar():
    caminho_banco = os.path.join(
        os.path.dirname(__file__),
        "financontrol.db"
    )

    return sqlite3.connect(caminho_banco)


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor_objetivo REAL NOT NULL,
            valor_atual REAL NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# =========================
# RECEITAS
# =========================

def salvar_receita(descricao, valor, data, categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO receitas
        (descricao, valor, data, categoria)
        VALUES (?, ?, ?, ?)
    """, (descricao, valor, data, categoria))

    conexao.commit()
    conexao.close()


def buscar_receitas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT descricao, valor, data, categoria
        FROM receitas
    """)

    dados = cursor.fetchall()
    conexao.close()

    return dados


def buscar_receitas_com_id():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, descricao, valor, data, categoria
        FROM receitas
        ORDER BY id
    """)

    dados = cursor.fetchall()
    conexao.close()

    return dados


def excluir_receita(id_receita):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM receitas WHERE id = ?",
        (id_receita,)
    )

    conexao.commit()
    conexao.close()


def editar_receita(id_receita, descricao, valor, data, categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE receitas
        SET descricao = ?,
            valor = ?,
            data = ?,
            categoria = ?
        WHERE id = ?
    """, (
        descricao,
        valor,
        data,
        categoria,
        id_receita
    ))

    conexao.commit()
    conexao.close()


# =========================
# DESPESAS
# =========================

def salvar_despesa(descricao, valor, data, categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO despesas
        (descricao, valor, data, categoria)
        VALUES (?, ?, ?, ?)
    """, (descricao, valor, data, categoria))

    conexao.commit()
    conexao.close()


def buscar_despesas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT descricao, valor, data, categoria
        FROM despesas
    """)

    dados = cursor.fetchall()
    conexao.close()

    return dados


def buscar_despesas_com_id():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, descricao, valor, data, categoria
        FROM despesas
        ORDER BY id
    """)

    dados = cursor.fetchall()
    conexao.close()

    return dados


def buscar_despesas_por_categoria(categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT descricao, valor, data, categoria
        FROM despesas
        WHERE LOWER(categoria) = LOWER(?)
    """, (categoria,))

    dados = cursor.fetchall()
    conexao.close()

    return dados


def excluir_despesa(id_despesa):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM despesas WHERE id = ?",
        (id_despesa,)
    )

    conexao.commit()
    conexao.close()


def editar_despesa(id_despesa, descricao, valor, data, categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE despesas
        SET descricao = ?,
            valor = ?,
            data = ?,
            categoria = ?
        WHERE id = ?
    """, (
        descricao,
        valor,
        data,
        categoria,
        id_despesa
    ))

    conexao.commit()
    conexao.close()


# =========================
# METAS
# =========================

def salvar_meta(nome, valor_objetivo, valor_atual):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO metas
        (nome, valor_objetivo, valor_atual)
        VALUES (?, ?, ?)
    """, (
        nome,
        valor_objetivo,
        valor_atual
    ))

    conexao.commit()
    conexao.close()


def buscar_metas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, valor_objetivo, valor_atual
        FROM metas
    """)

    dados = cursor.fetchall()
    conexao.close()

    return dados


def buscar_metas_com_id():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, valor_objetivo, valor_atual
        FROM metas
        ORDER BY id
    """)

    dados = cursor.fetchall()
    conexao.close()

    return dados


def excluir_meta(id_meta):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM metas WHERE id = ?",
        (id_meta,)
    )

    conexao.commit()
    conexao.close()


def editar_meta(id_meta, nome, valor_objetivo, valor_atual):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE metas
        SET nome = ?,
            valor_objetivo = ?,
            valor_atual = ?
        WHERE id = ?
    """, (
        nome,
        valor_objetivo,
        valor_atual,
        id_meta
    ))

    conexao.commit()
    conexao.close()