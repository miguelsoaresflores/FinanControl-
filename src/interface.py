import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from tkcalendar import DateEntry

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database.database import (
    criar_tabelas,
    salvar_receita,
    salvar_despesa,
    salvar_meta,
    buscar_receitas_com_id,
    buscar_despesas_com_id,
    buscar_metas_com_id,
    excluir_receita,
    excluir_despesa,
    excluir_meta,
    editar_receita,
    editar_despesa,
    editar_meta
)


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

CATEGORIAS_PADRAO = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Lazer",
    "Saúde",
    "Educação",
    "Salário",
    "Investimentos",
    "Outros"
]

COR_FUNDO = "#f5f6f8"
COR_CARD = "#ffffff"
COR_TEXTO = "#202124"
COR_SECUNDARIA = "#73777d"
COR_BORDA = "#e8e9ec"
COR_BOTAO = "#202124"
COR_BOTAO_HOVER = "#36383c"
COR_INPUT = "#f8f8f9"

criar_tabelas()


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def obter_categorias():
    categorias = set(CATEGORIAS_PADRAO)

    for receita in buscar_receitas_com_id():
        categorias.add(receita[4])

    for despesa in buscar_despesas_com_id():
        categorias.add(despesa[4])

    return sorted(categorias)


def converter_valor(valor):
    valor = (
        valor
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

    return float(valor)


def formatar_moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

root = tk.Tk()

root.title("FinanControl")
root.geometry("1400x850")
root.minsize(1100, 700)
root.configure(bg=COR_FUNDO)


# ==========================================================
# ESTILO
# ==========================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=COR_CARD,
    fieldbackground=COR_CARD,
    foreground=COR_TEXTO,
    rowheight=34,
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#f0f1f3",
    foreground=COR_TEXTO,
    font=("Segoe UI", 10, "bold"),
    borderwidth=0
)

style.map(
    "Treeview",
    background=[
        ("selected", "#e8eaed")
    ],
    foreground=[
        ("selected", COR_TEXTO)
    ]
)

style.configure(
    "TCombobox",
    padding=8,
    font=("Segoe UI", 10)
)


# ==========================================================
# FUNÇÕES VISUAIS
# ==========================================================

def criar_botao(parent, texto, comando, destaque=False):

    fundo = COR_BOTAO if destaque else COR_CARD
    texto_cor = "#ffffff" if destaque else COR_TEXTO

    frame = tk.Frame(
        parent,
        bg=fundo,
        highlightbackground=COR_BORDA,
        highlightthickness=1
    )

    label = tk.Label(
        frame,
        text=texto,
        bg=fundo,
        fg=texto_cor,
        font=("Segoe UI", 10, "bold"),
        padx=16,
        pady=9,
        cursor="hand2"
    )

    label.pack()

    def entrar(event):
        cor = COR_BOTAO_HOVER if destaque else "#f1f2f4"

        frame.configure(bg=cor)
        label.configure(bg=cor)

    def sair(event):
        frame.configure(bg=fundo)
        label.configure(bg=fundo)

    def clicar(event):
        comando()

    frame.bind("<Enter>", entrar)
    frame.bind("<Leave>", sair)
    frame.bind("<Button-1>", clicar)

    label.bind("<Enter>", entrar)
    label.bind("<Leave>", sair)
    label.bind("<Button-1>", clicar)

    return frame


def criar_card(parent):

    return tk.Frame(
        parent,
        bg=COR_CARD,
        highlightbackground=COR_BORDA,
        highlightthickness=1
    )


def criar_label_input(parent, texto):

    tk.Label(
        parent,
        text=texto,
        bg=COR_CARD,
        fg=COR_TEXTO,
        font=("Segoe UI", 10, "bold")
    ).pack(
        anchor="w",
        pady=(0, 6)
    )


def criar_entry(parent):

    return tk.Entry(
        parent,
        bg=COR_INPUT,
        fg=COR_TEXTO,
        insertbackground=COR_TEXTO,
        relief="flat",
        highlightbackground=COR_BORDA,
        highlightthickness=1,
        font=("Segoe UI", 11)
    )


def criar_titulo_janela(janela, titulo, subtitulo=None):

    tk.Label(
        janela,
        text=titulo,
        bg=COR_FUNDO,
        fg=COR_TEXTO,
        font=("Segoe UI", 21, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 3)
    )

    if subtitulo:

        tk.Label(
            janela,
            text=subtitulo,
            bg=COR_FUNDO,
            fg=COR_SECUNDARIA,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )


# ==========================================================
# CABEÇALHO
# ==========================================================

header = tk.Frame(
    root,
    bg=COR_CARD,
    height=78,
    highlightbackground=COR_BORDA,
    highlightthickness=1
)

header.pack(fill="x")
header.pack_propagate(False)

logo_frame = tk.Frame(
    header,
    bg=COR_CARD
)

logo_frame.pack(
    side="left",
    padx=30
)

tk.Label(
    logo_frame,
    text="FinanControl",
    bg=COR_CARD,
    fg=COR_TEXTO,
    font=("Segoe UI", 21, "bold")
).pack(side="left")

tk.Label(
    logo_frame,
    text="  •  Controle financeiro pessoal",
    bg=COR_CARD,
    fg=COR_SECUNDARIA,
    font=("Segoe UI", 10)
).pack(
    side="left",
    pady=7
)


# ==========================================================
# ÁREA PRINCIPAL
# ==========================================================

container = tk.Frame(
    root,
    bg=COR_FUNDO
)

container.pack(
    fill="both",
    expand=True
)

canvas = tk.Canvas(
    container,
    bg=COR_FUNDO,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

conteudo = tk.Frame(
    canvas,
    bg=COR_FUNDO
)

conteudo.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas_window = canvas.create_window(
    (0, 0),
    window=conteudo,
    anchor="nw"
)


def ajustar_largura(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    ajustar_largura
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ==========================================================
# TÍTULO
# ==========================================================

tk.Label(
    conteudo,
    text="Visão geral",
    bg=COR_FUNDO,
    fg=COR_TEXTO,
    font=("Segoe UI", 24, "bold")
).pack(
    anchor="w",
    padx=35,
    pady=(30, 4)
)

tk.Label(
    conteudo,
    text="Acompanhe suas finanças e registre novas movimentações.",
    bg=COR_FUNDO,
    fg=COR_SECUNDARIA,
    font=("Segoe UI", 10)
).pack(
    anchor="w",
    padx=35,
    pady=(0, 20)
)


# ==========================================================
# AÇÕES
# ==========================================================

acoes = tk.Frame(
    conteudo,
    bg=COR_FUNDO
)

acoes.pack(
    fill="x",
    padx=35,
    pady=(0, 25)
)


# ==========================================================
# CARDS FINANCEIROS
# ==========================================================

cards = tk.Frame(
    conteudo,
    bg=COR_FUNDO
)

cards.pack(
    fill="x",
    padx=35
)


def criar_card_financeiro(parent, titulo, valor):

    frame = criar_card(parent)

    tk.Label(
        frame,
        text=titulo,
        bg=COR_CARD,
        fg=COR_SECUNDARIA,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        padx=20,
        pady=(18, 5)
    )

    label = tk.Label(
        frame,
        text=valor,
        bg=COR_CARD,
        fg=COR_TEXTO,
        font=("Segoe UI", 19, "bold")
    )

    label.pack(
        anchor="w",
        padx=20,
        pady=(0, 18)
    )

    return frame, label


card_saldo, label_saldo = criar_card_financeiro(
    cards,
    "Saldo atual",
    "R$ 0,00"
)

card_receitas, label_receitas = criar_card_financeiro(
    cards,
    "Receitas",
    "R$ 0,00"
)

card_despesas, label_despesas = criar_card_financeiro(
    cards,
    "Despesas",
    "R$ 0,00"
)

card_metas, label_metas = criar_card_financeiro(
    cards,
    "Metas",
    "0"
)

card_saldo.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)

card_receitas.pack(
    side="left",
    fill="both",
    expand=True,
    padx=8
)

card_despesas.pack(
    side="left",
    fill="both",
    expand=True,
    padx=8
)

card_metas.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(8, 0)
)


# ==========================================================
# GRÁFICO
# ==========================================================

graficos = tk.Frame(
    conteudo,
    bg=COR_FUNDO
)

graficos.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=25
)


def criar_card_grafico(parent, titulo):

    frame = criar_card(parent)

    tk.Label(
        frame,
        text=titulo,
        bg=COR_CARD,
        fg=COR_TEXTO,
        font=("Segoe UI", 12, "bold")
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    return frame


grafico_categoria_card = criar_card_grafico(
    graficos,
    "Gastos por categoria"
)

grafico_categoria_card.pack(
    fill="both",
    expand=True,
    pady=6
)


# ==========================================================
# ATUALIZAR GRÁFICO
# ==========================================================

def remover_graficos(frame):

    for widget in frame.winfo_children():

        if isinstance(widget, tk.Canvas):
            widget.destroy()


def atualizar_graficos():

    despesas = buscar_despesas_com_id()

    remover_graficos(
        grafico_categoria_card
    )

    dados_categoria = {}

    for despesa in despesas:

        categoria = despesa[4]
        valor = float(despesa[2])

        dados_categoria[categoria] = (
            dados_categoria.get(categoria, 0)
            + valor
        )

    fig = Figure(
        figsize=(10, 4.5),
        dpi=90
    )

    ax = fig.add_subplot(111)

    if dados_categoria:

        ax.pie(
            dados_categoria.values(),
            labels=dados_categoria.keys(),
            autopct="%1.1f%%"
        )

        ax.set_title(
            "Distribuição das despesas",
            fontsize=10
        )

    else:

        ax.text(
            0.5,
            0.5,
            "Nenhuma despesa cadastrada",
            ha="center",
            va="center"
        )

        ax.set_title(
            "Distribuição das despesas",
            fontsize=10
        )

    fig.tight_layout()

    canvas_grafico = FigureCanvasTkAgg(
        fig,
        master=grafico_categoria_card
    )

    canvas_grafico.draw()

    canvas_grafico.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=12,
        pady=(5, 12)
    )


# ==========================================================
# DASHBOARD
# ==========================================================

def atualizar_dashboard():

    receitas = buscar_receitas_com_id()
    despesas = buscar_despesas_com_id()
    metas = buscar_metas_com_id()

    total_receitas = sum(
        float(r[2])
        for r in receitas
    )

    total_despesas = sum(
        float(d[2])
        for d in despesas
    )

    saldo = (
        total_receitas
        - total_despesas
    )

    label_saldo.config(
        text=formatar_moeda(saldo)
    )

    label_receitas.config(
        text=formatar_moeda(total_receitas)
    )

    label_despesas.config(
        text=formatar_moeda(total_despesas)
    )

    label_metas.config(
        text=str(len(metas))
    )

    atualizar_graficos()


# ==========================================================
# FORMULÁRIO DE RECEITA
# ==========================================================

def abrir_formulario_receita(receita_id=None):

    janela = tk.Toplevel(root)

    janela.title(
        "Editar receita"
        if receita_id
        else "Nova receita"
    )

    janela.geometry("520x570")
    janela.configure(bg=COR_FUNDO)
    janela.resizable(False, False)

    criar_titulo_janela(
        janela,
        "Editar receita"
        if receita_id
        else "Nova receita",
        "Preencha os dados da movimentação."
    )

    card = criar_card(janela)

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    formulario = tk.Frame(
        card,
        bg=COR_CARD
    )

    formulario.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=25
    )

    criar_label_input(
        formulario,
        "Descrição"
    )

    entrada_descricao = criar_entry(
        formulario
    )

    entrada_descricao.pack(
        fill="x",
        ipady=7,
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Valor"
    )

    entrada_valor = criar_entry(
        formulario
    )

    entrada_valor.pack(
        fill="x",
        ipady=7,
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Data"
    )

    entrada_data = DateEntry(
        formulario,
        date_pattern="dd/mm/yyyy",
        font=("Segoe UI", 10)
    )

    entrada_data.pack(
        fill="x",
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Categoria"
    )

    entrada_categoria = ttk.Combobox(
        formulario,
        values=obter_categorias(),
        state="readonly"
    )

    entrada_categoria.pack(
        fill="x",
        ipady=6,
        pady=(0, 25)
    )

    if receita_id:

        receita = next(
            (
                r
                for r in buscar_receitas_com_id()
                if r[0] == receita_id
            ),
            None
        )

        if receita:

            entrada_descricao.insert(
                0,
                receita[1]
            )

            entrada_valor.insert(
                0,
                str(receita[2])
            )

            try:

                entrada_data.set_date(
                    datetime.strptime(
                        receita[3],
                        "%d/%m/%Y"
                    ).date()
                )

            except ValueError:
                pass

            entrada_categoria.set(
                receita[4]
            )

    def salvar():

        descricao = (
            entrada_descricao
            .get()
            .strip()
        )

        valor_texto = (
            entrada_valor
            .get()
            .strip()
        )

        data = entrada_data.get()
        categoria = entrada_categoria.get()

        if (
            not descricao
            or not valor_texto
            or not categoria
        ):

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )

            return

        try:

            valor = converter_valor(
                valor_texto
            )

            if valor <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite um valor válido."
            )

            return

        if receita_id:

            editar_receita(
                receita_id,
                descricao,
                valor,
                data,
                categoria
            )

        else:

            salvar_receita(
                descricao,
                valor,
                data,
                categoria
            )

        janela.destroy()

        atualizar_dashboard()

    criar_botao(
        formulario,
        "Salvar receita",
        salvar,
        destaque=True
    ).pack(
        anchor="e"
    )


# ==========================================================
# FORMULÁRIO DE DESPESA
# ==========================================================

def abrir_formulario_despesa(despesa_id=None):

    janela = tk.Toplevel(root)

    janela.title(
        "Editar despesa"
        if despesa_id
        else "Nova despesa"
    )

    janela.geometry("520x570")
    janela.configure(bg=COR_FUNDO)
    janela.resizable(False, False)

    criar_titulo_janela(
        janela,
        "Editar despesa"
        if despesa_id
        else "Nova despesa",
        "Registre uma nova saída financeira."
    )

    card = criar_card(janela)

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    formulario = tk.Frame(
        card,
        bg=COR_CARD
    )

    formulario.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=25
    )

    criar_label_input(
        formulario,
        "Descrição"
    )

    entrada_descricao = criar_entry(
        formulario
    )

    entrada_descricao.pack(
        fill="x",
        ipady=7,
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Valor"
    )

    entrada_valor = criar_entry(
        formulario
    )

    entrada_valor.pack(
        fill="x",
        ipady=7,
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Data"
    )

    entrada_data = DateEntry(
        formulario,
        date_pattern="dd/mm/yyyy",
        font=("Segoe UI", 10)
    )

    entrada_data.pack(
        fill="x",
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Categoria"
    )

    entrada_categoria = ttk.Combobox(
        formulario,
        values=obter_categorias(),
        state="readonly"
    )

    entrada_categoria.pack(
        fill="x",
        ipady=6,
        pady=(0, 25)
    )

    if despesa_id:

        despesa = next(
            (
                d
                for d in buscar_despesas_com_id()
                if d[0] == despesa_id
            ),
            None
        )

        if despesa:

            entrada_descricao.insert(
                0,
                despesa[1]
            )

            entrada_valor.insert(
                0,
                str(despesa[2])
            )

            try:

                entrada_data.set_date(
                    datetime.strptime(
                        despesa[3],
                        "%d/%m/%Y"
                    ).date()
                )

            except ValueError:
                pass

            entrada_categoria.set(
                despesa[4]
            )

    def salvar():

        descricao = (
            entrada_descricao
            .get()
            .strip()
        )

        valor_texto = (
            entrada_valor
            .get()
            .strip()
        )

        data = entrada_data.get()
        categoria = entrada_categoria.get()

        if (
            not descricao
            or not valor_texto
            or not categoria
        ):

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )

            return

        try:

            valor = converter_valor(
                valor_texto
            )

            if valor <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite um valor válido."
            )

            return

        if despesa_id:

            editar_despesa(
                despesa_id,
                descricao,
                valor,
                data,
                categoria
            )

        else:

            salvar_despesa(
                descricao,
                valor,
                data,
                categoria
            )

        janela.destroy()

        atualizar_dashboard()

    criar_botao(
        formulario,
        "Salvar despesa",
        salvar,
        destaque=True
    ).pack(
        anchor="e"
    )


# ==========================================================
# FORMULÁRIO DE META
# ==========================================================

def abrir_formulario_meta(meta_id=None):

    janela = tk.Toplevel(root)

    janela.title(
        "Editar meta"
        if meta_id
        else "Nova meta"
    )

    janela.geometry("520x500")
    janela.configure(bg=COR_FUNDO)
    janela.resizable(False, False)

    criar_titulo_janela(
        janela,
        "Editar meta"
        if meta_id
        else "Nova meta",
        "Defina um objetivo financeiro."
    )

    card = criar_card(janela)

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    formulario = tk.Frame(
        card,
        bg=COR_CARD
    )

    formulario.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=25
    )

    criar_label_input(
        formulario,
        "Nome da meta"
    )

    entrada_nome = criar_entry(
        formulario
    )

    entrada_nome.pack(
        fill="x",
        ipady=7,
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Valor objetivo"
    )

    entrada_objetivo = criar_entry(
        formulario
    )

    entrada_objetivo.pack(
        fill="x",
        ipady=7,
        pady=(0, 18)
    )

    criar_label_input(
        formulario,
        "Valor já guardado"
    )

    entrada_atual = criar_entry(
        formulario
    )

    entrada_atual.pack(
        fill="x",
        ipady=7,
        pady=(0, 25)
    )

    if meta_id:

        meta = next(
            (
                m
                for m in buscar_metas_com_id()
                if m[0] == meta_id
            ),
            None
        )

        if meta:

            entrada_nome.insert(
                0,
                meta[1]
            )

            entrada_objetivo.insert(
                0,
                str(meta[2])
            )

            entrada_atual.insert(
                0,
                str(meta[3])
            )

    def salvar():

        nome = (
            entrada_nome
            .get()
            .strip()
        )

        objetivo_texto = (
            entrada_objetivo
            .get()
            .strip()
        )

        atual_texto = (
            entrada_atual
            .get()
            .strip()
        )

        if (
            not nome
            or not objetivo_texto
            or not atual_texto
        ):

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )

            return

        try:

            objetivo = converter_valor(
                objetivo_texto
            )

            atual = converter_valor(
                atual_texto
            )

            if objetivo <= 0 or atual < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite valores válidos."
            )

            return

        if meta_id:

            editar_meta(
                meta_id,
                nome,
                objetivo,
                atual
            )

        else:

            salvar_meta(
                nome,
                objetivo,
                atual
            )

        janela.destroy()

        atualizar_dashboard()

    criar_botao(
        formulario,
        "Salvar meta",
        salvar,
        destaque=True
    ).pack(
        anchor="e"
    )


# ==========================================================
# MOVIMENTAÇÕES
# ==========================================================

def abrir_movimentacoes():

    janela = tk.Toplevel(root)

    janela.title("Movimentações")
    janela.geometry("1000x650")
    janela.configure(bg=COR_FUNDO)

    criar_titulo_janela(
        janela,
        "Movimentações",
        "Consulte, edite ou exclua seus lançamentos."
    )

    card = criar_card(janela)

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    tabela = ttk.Treeview(
        card,
        columns=(
            "id",
            "tipo",
            "descricao",
            "valor",
            "data",
            "categoria"
        ),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("descricao", text="Descrição")
    tabela.heading("valor", text="Valor")
    tabela.heading("data", text="Data")
    tabela.heading("categoria", text="Categoria")

    tabela.column("id", width=50)
    tabela.column("tipo", width=100)
    tabela.column("descricao", width=230)
    tabela.column("valor", width=120)
    tabela.column("data", width=120)
    tabela.column("categoria", width=160)

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    botoes = tk.Frame(
        janela,
        bg=COR_FUNDO
    )

    botoes.pack(
        pady=(0, 20)
    )

    def carregar():

        for item in tabela.get_children():
            tabela.delete(item)

        for receita in buscar_receitas_com_id():

            tabela.insert(
                "",
                "end",
                values=(
                    receita[0],
                    "Receita",
                    receita[1],
                    formatar_moeda(float(receita[2])),
                    receita[3],
                    receita[4]
                )
            )

        for despesa in buscar_despesas_com_id():

            tabela.insert(
                "",
                "end",
                values=(
                    despesa[0],
                    "Despesa",
                    despesa[1],
                    formatar_moeda(float(despesa[2])),
                    despesa[3],
                    despesa[4]
                )
            )

    def editar_selecionado():

        selecionado = tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma movimentação."
            )

            return

        dados = tabela.item(
            selecionado[0]
        )["values"]

        id_movimentacao = int(dados[0])
        tipo = dados[1]

        janela.destroy()

        if tipo == "Receita":

            abrir_formulario_receita(
                id_movimentacao
            )

        else:

            abrir_formulario_despesa(
                id_movimentacao
            )

    def excluir_selecionado():

        selecionado = tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma movimentação."
            )

            return

        dados = tabela.item(
            selecionado[0]
        )["values"]

        id_movimentacao = int(dados[0])
        tipo = dados[1]

        confirmar = messagebox.askyesno(
            "Excluir movimentação",
            "Deseja realmente excluir esta movimentação?"
        )

        if not confirmar:
            return

        if tipo == "Receita":

            excluir_receita(
                id_movimentacao
            )

        else:

            excluir_despesa(
                id_movimentacao
            )

        carregar()
        atualizar_dashboard()

    criar_botao(
        botoes,
        "Editar",
        editar_selecionado
    ).pack(
        side="left",
        padx=5
    )

    criar_botao(
        botoes,
        "Excluir",
        excluir_selecionado
    ).pack(
        side="left",
        padx=5
    )

    carregar()


# ==========================================================
# FILTRO DE DESPESAS
# ==========================================================

def abrir_filtro():

    janela = tk.Toplevel(root)

    janela.title("Filtrar despesas")
    janela.geometry("900x600")
    janela.configure(bg=COR_FUNDO)

    criar_titulo_janela(
        janela,
        "Filtrar despesas",
        "Consulte seus gastos por categoria."
    )

    filtro_card = criar_card(janela)

    filtro_card.pack(
        fill="x",
        padx=30,
        pady=(0, 10)
    )

    filtro_frame = tk.Frame(
        filtro_card,
        bg=COR_CARD
    )

    filtro_frame.pack(
        fill="x",
        padx=20,
        pady=18
    )

    tk.Label(
        filtro_frame,
        text="Categoria",
        bg=COR_CARD,
        fg=COR_TEXTO,
        font=("Segoe UI", 10, "bold")
    ).pack(
        side="left",
        padx=(0, 10)
    )

    categoria = ttk.Combobox(
        filtro_frame,
        values=obter_categorias(),
        state="readonly",
        width=30
    )

    categoria.pack(
        side="left"
    )

    tabela_card = criar_card(janela)

    tabela_card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    tabela = ttk.Treeview(
        tabela_card,
        columns=(
            "descricao",
            "valor",
            "data",
            "categoria"
        ),
        show="headings"
    )

    tabela.heading("descricao", text="Descrição")
    tabela.heading("valor", text="Valor")
    tabela.heading("data", text="Data")
    tabela.heading("categoria", text="Categoria")

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    label_total = tk.Label(
        janela,
        text="Total: R$ 0,00",
        bg=COR_FUNDO,
        fg=COR_TEXTO,
        font=("Segoe UI", 13, "bold")
    )

    label_total.pack(
        pady=10
    )

    def filtrar():

        for item in tabela.get_children():
            tabela.delete(item)

        categoria_selecionada = categoria.get()

        if not categoria_selecionada:
            return

        total = 0

        for despesa in buscar_despesas_com_id():

            if (
                despesa[4].lower()
                ==
                categoria_selecionada.lower()
            ):

                tabela.insert(
                    "",
                    "end",
                    values=(
                        despesa[1],
                        formatar_moeda(
                            float(despesa[2])
                        ),
                        despesa[3],
                        despesa[4]
                    )
                )

                total += float(
                    despesa[2]
                )

        label_total.config(
            text=f"Total: {formatar_moeda(total)}"
        )

    criar_botao(
        filtro_frame,
        "Filtrar",
        filtrar,
        destaque=True
    ).pack(
        side="left",
        padx=10
    )


# ==========================================================
# METAS
# ==========================================================

def abrir_metas():

    janela = tk.Toplevel(root)

    janela.title("Metas financeiras")
    janela.geometry("950x620")
    janela.configure(bg=COR_FUNDO)

    criar_titulo_janela(
        janela,
        "Metas financeiras",
        "Acompanhe o progresso dos seus objetivos."
    )

    card = criar_card(janela)

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 15)
    )

    tabela = ttk.Treeview(
        card,
        columns=(
            "id",
            "nome",
            "objetivo",
            "atual",
            "falta",
            "progresso"
        ),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Meta")
    tabela.heading("objetivo", text="Objetivo")
    tabela.heading("atual", text="Guardado")
    tabela.heading("falta", text="Falta")
    tabela.heading("progresso", text="Progresso")

    tabela.column("id", width=50)
    tabela.column("nome", width=250)

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    botoes = tk.Frame(
        janela,
        bg=COR_FUNDO
    )

    botoes.pack(
        pady=(0, 20)
    )

    def carregar():

        for item in tabela.get_children():
            tabela.delete(item)

        for meta in buscar_metas_com_id():

            objetivo = float(meta[2])
            atual = float(meta[3])

            falta = max(
                objetivo - atual,
                0
            )

            progresso = (
                atual / objetivo * 100
                if objetivo > 0
                else 0
            )

            tabela.insert(
                "",
                "end",
                values=(
                    meta[0],
                    meta[1],
                    formatar_moeda(objetivo),
                    formatar_moeda(atual),
                    formatar_moeda(falta),
                    f"{progresso:.1f}%"
                )
            )

    def nova_meta():

        janela.destroy()
        abrir_formulario_meta()

    def editar():

        selecionado = tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma meta."
            )

            return

        dados = tabela.item(
            selecionado[0]
        )["values"]

        meta_id = int(dados[0])

        janela.destroy()

        abrir_formulario_meta(
            meta_id
        )

    def excluir():

        selecionado = tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma meta."
            )

            return

        dados = tabela.item(
            selecionado[0]
        )["values"]

        meta_id = int(dados[0])

        confirmar = messagebox.askyesno(
            "Excluir meta",
            "Deseja realmente excluir esta meta?"
        )

        if not confirmar:
            return

        excluir_meta(meta_id)

        carregar()
        atualizar_dashboard()

    criar_botao(
        botoes,
        "+ Nova meta",
        nova_meta,
        destaque=True
    ).pack(
        side="left",
        padx=5
    )

    criar_botao(
        botoes,
        "Editar",
        editar
    ).pack(
        side="left",
        padx=5
    )

    criar_botao(
        botoes,
        "Excluir",
        excluir
    ).pack(
        side="left",
        padx=5
    )

    carregar()


# ==========================================================
# BOTÕES DO DASHBOARD
# ==========================================================

criar_botao(
    acoes,
    "+ Receita",
    abrir_formulario_receita,
    destaque=True
).pack(
    side="left",
    padx=(0, 8)
)

criar_botao(
    acoes,
    "+ Despesa",
    abrir_formulario_despesa
).pack(
    side="left",
    padx=8
)

criar_botao(
    acoes,
    "+ Meta",
    abrir_formulario_meta
).pack(
    side="left",
    padx=8
)

criar_botao(
    acoes,
    "Movimentações",
    abrir_movimentacoes
).pack(
    side="left",
    padx=8
)

criar_botao(
    acoes,
    "Filtrar",
    abrir_filtro
).pack(
    side="left",
    padx=8
)

criar_botao(
    acoes,
    "Metas",
    abrir_metas
).pack(
    side="left",
    padx=8
)

criar_botao(
    acoes,
    "Atualizar",
    atualizar_dashboard
).pack(
    side="left",
    padx=8
)


# ==========================================================
# INICIALIZAÇÃO
# ==========================================================

atualizar_dashboard()

root.mainloop()