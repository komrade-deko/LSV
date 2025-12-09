import flet as ft
import sqlite3

salvar_style = ft.ButtonStyle(padding=20, alignment=ft.alignment.center_left, color="#EEEEEE", bgcolor="#273273",
                              shape=ft.RoundedRectangleBorder(radius=7),
                              text_style=ft.TextStyle(size=14, font_family="inter"))
cancelar_style = ft.ButtonStyle(padding=20, alignment=ft.alignment.center, color="#212121", bgcolor="#BDBDBD",
                                shape=ft.RoundedRectangleBorder(radius=7),
                                text_style=ft.TextStyle(size=14, font_family="inter"))

def apenas_numeros(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])
    e.control.value = v
    e.control.update()

def limpar_erro(e):
    c = e.control
    if c.value and c.value.strip():
        c.error_text = None
        c.border_color = None
        c.update()

def formatar_data(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])[:8]
    e.control.value = (v[:2] + ("/" + v[2:4] if len(v) >= 3 else "") +
                       ("/" + v[4:8] if len(v) >= 5 else ""))
    e.control.update()

def fechar_modal(modal, page):
    modal.open = False
    page.update()


def formatar_telefone(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])[:11]

    if len(v) >= 1:
        v = "(" + v
    if len(v) >= 3:
        v = v[:3] + ") " + v[3:]
    if len(v) >= 6:
        v = v[:6] + v[6:]

    e.control.value = v
    e.control.update()
    limpar_erro(e)


def validar_campos_obrigatorios(*campos):
    valido = True
    for campo in campos:
        if not campo.value or not campo.value.strip():
            campo.error_text = "⚠️ Campo Obrigatório"
            campo.border_color = "#E53935"
            campo.update()
            valido = False
    return valido

def set_fab(page, color, callback):
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=color,
        on_click=lambda e: callback(page)
    )
    page.update()

def buscar_generico(conectar_fn, tabela, colunas, coluna_pesquisa, texto):
    conn, cursor = conectar_fn()

    if texto:
        busca = f"%{texto}%"
        condicoes = " OR ".join([f"{col} LIKE ?" for col in coluna_pesquisa])
        sql = f"SELECT {', '.join(colunas)} FROM {tabela} WHERE {condicoes}"
        cursor.execute(sql, tuple([busca] * len(coluna_pesquisa)))
    else:
        sql = f"SELECT {', '.join(colunas)} FROM {tabela}"
        cursor.execute(sql)

    dados = cursor.fetchall()
    conn.close()
    return dados


def salvar_generico(conectar_fn, tabela, colunas, id_coluna, item_id, valores):
    conn, cursor = conectar_fn()

    set_clause = ", ".join([f"{col} = ?" for col in colunas])
    sql = f"UPDATE {tabela} SET {set_clause} WHERE {id_coluna} = ?"

    cursor.execute(sql, (*valores, item_id))
    conn.commit()
    conn.close()


def excluir_generico(conectar_fn, tabela, id_coluna, item_id):
    conn, cursor = conectar_fn()
    sql = f"DELETE FROM {tabela} WHERE {id_coluna} = ?"
    cursor.execute(sql, (item_id,))
    conn.commit()
    conn.close()


def editar_generico(
        page,
        titulo,
        colunas,
        valores,
        validar_fn,
        salvar_sql_fn,
        atualizar_callback
):
    campos = [
        ft.TextField(label=colunas[i], value=str(valores[i]))
        for i in range(len(colunas))
    ]

    def salvar(e):
        novos_valores = [c.value.strip() for c in campos]

        if not validar_fn(novos_valores):
            return

        salvar_sql_fn(novos_valores)

        modal.open = False
        page.update()
        atualizar_callback()

    modal = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=20, font_family="JosefinBold"),
                *campos
            ],
            spacing=10,
            tight=True,
            width=340
        ),
        actions=[
            ft.TextButton("Salvar", style=salvar_style, on_click=salvar),
            ft.TextButton("Cancelar", style=cancelar_style, on_click=lambda e: fechar_modal(modal, page))
        ],
        shape=ft.RoundedRectangleBorder(radius=7)
    )

    page.overlay.append(modal)
    modal.open = True
    page.update()


def confirmar_excluir_generico(
        page,
        titulo,
        mensagem,
        conectar_fn,
        tabela,
        id_coluna,
        item_id,
        atualizar_callback
):
    def executar_exclusao(e, dialog):
        excluir_generico(conectar_fn, tabela, id_coluna, item_id)
        dialog.open = False
        page.update()
        atualizar_callback()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(titulo, font_family="JosefinBold", size=20),
        shape=ft.RoundedRectangleBorder(radius=7),
        content=ft.Text(mensagem, font_family="inter"),
        actions=[
            ft.TextButton(
                "Apagar",
                style=ft.ButtonStyle(
                    padding=20,
                    alignment=ft.alignment.center_left,
                    color="#EEEEEE",
                    bgcolor="#E53935",
                    overlay_color="#C62828",
                    shape=ft.RoundedRectangleBorder(radius=7),
                    text_style=ft.TextStyle(size=14, font_family="inter")
                ),
                on_click=lambda e: executar_exclusao(e, dialog)
            ),
            ft.TextButton(
                "Cancelar",
                style=cancelar_style,
                on_click=lambda e: fechar_modal(dialog, page)
            )
        ],
        actions_alignment="end",
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def filtrar_generico(instancia, campo, atualizar_callback):
    def _filter(e):
        setattr(instancia, campo, e.control.value.lower())
        atualizar_callback()
    return _filter

def criar_tabela_generica(
        instancia,
        titulo_tela,
        nome_tabela,
        colunas_config,
        colunas_pesquisa,
        campo_filtro_instancia,
        funcao_atualizar_nome,
        funcao_abrir_modal,
        funcao_validar_editar=None,
        funcao_extra_editar=None
):

    campos_banco = [col["campo"] for col in colunas_config]
    nomes_colunas = [col["nome"] for col in colunas_config]
    larguras_colunas = [col["largura"] for col in colunas_config]

    def montar_rows():
        filtro_atual = getattr(instancia, campo_filtro_instancia, "")

        dados = buscar_generico(
            conectar_fn=instancia.conectar,
            tabela=nome_tabela,
            colunas=campos_banco,
            coluna_pesquisa=colunas_pesquisa,
            texto=filtro_atual
        )

        linhas = []

        for linha in dados:
            cells = []
            for i, valor in enumerate(linha):
                cells.append(
                    ft.DataCell(
                        ft.Container(ft.Text(str(valor) if valor is not None else "-"), width=larguras_colunas[i]))
                )

            item_id = linha[0]

            menu = ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(
                        text="Editar",
                        on_click=lambda e, item_id=item_id, linha=linha: _abrir_editar(
                            instancia,
                            nome_tabela,
                            item_id,
                            campos_banco,
                            nomes_colunas,
                            linha,
                            funcao_validar_editar,
                            funcao_extra_editar
                        )
                    ),
                    ft.PopupMenuItem(
                        text="Apagar",
                        on_click=lambda e, item_id=item_id, linha=linha: _confirmar_excluir(
                            instancia,
                            nome_tabela,
                            campos_banco[0],
                            item_id,
                            linha,
                            nomes_colunas
                        )
                    ),
                ]
            )

            cells.append(ft.DataCell(menu))

            linhas.append(ft.DataRow(cells=cells))

        return linhas

    def _abrir_editar(instancia, nome_tabela, item_id, campos_banco, nomes_colunas, linha, funcao_validar,
                      funcao_extra):
        valores_edicao = linha[1:]
        nomes_edicao = nomes_colunas[1:]
        campos_edicao = campos_banco[1:]

        def validar_padrao(vals):
            return True

        validar_fn = funcao_validar if funcao_validar else validar_padrao

        def salvar_fn(valores):
            salvar_generico(
                conectar_fn=instancia.conectar,
                tabela=nome_tabela,
                colunas=campos_edicao,
                id_coluna=campos_banco[0],
                item_id=item_id,
                valores=valores
            )
            if funcao_extra:
                funcao_extra()

        editar_generico(
            page=instancia.page,
            titulo=f"Editar {titulo_tela[:-1]}",
            colunas=nomes_edicao,
            valores=valores_edicao,
            validar_fn=validar_fn,
            salvar_sql_fn=salvar_fn,
            atualizar_callback=lambda: getattr(instancia, funcao_atualizar_nome)()
        )

    def _confirmar_excluir(instancia, nome_tabela, id_coluna, item_id, linha, nomes_colunas):
        nome_item = linha[1] if len(linha) > 1 else str(item_id)

        confirmar_excluir_generico(
            page=instancia.page,
            titulo="Confirmar exclusão",
            mensagem=f"Tem certeza que deseja excluir '{nome_item}'?",
            conectar_fn=instancia.conectar,
            tabela=nome_tabela,
            id_coluna=id_coluna,
            item_id=item_id,
            atualizar_callback=lambda: getattr(instancia, funcao_atualizar_nome)()
        )

    tabela_body = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("")) for _ in range(len(colunas_config) + 1)],
        rows=montar_rows(),
        heading_row_height=0,
        column_spacing=20,
        show_bottom_border=False,
    )

    def atualizar_tabela():
        novas_linhas = montar_rows()
        tabela_body.rows = novas_linhas
        tabela_body.update()

    setattr(instancia, funcao_atualizar_nome, atualizar_tabela)

    tabela_header = ft.DataTable(
        columns=[
                    ft.DataColumn(ft.Container(content=ft.Text(nome), width=largura))
                    for nome, largura in zip(nomes_colunas, larguras_colunas)
                ] + [ft.DataColumn(ft.Container(content=ft.Text("Ações"), width=100))],
        rows=[],
        heading_row_color="#E0E0E0",
        border=ft.border.only(bottom=ft.BorderSide(1, "#CCCCCC")),
        column_spacing=20,
    )

    tabela_scroll = ft.ListView(
        expand=True,
        controls=[ft.Container(content=tabela_body, expand=True)]
    )

    campo_pesquisa = ft.TextField(
        label="Pesquisar",
        prefix_icon=ft.Icons.SEARCH,
        value=getattr(instancia, campo_filtro_instancia, ""),
        on_change=filtrar_generico(
            instancia=instancia,
            campo=campo_filtro_instancia,
            atualizar_callback=atualizar_tabela
        )
    )

    return {
        "titulo": ft.Text(titulo_tela, size=28, font_family="JosefinBold"),
        "pesquisa": campo_pesquisa,
        "header": tabela_header,
        "body": tabela_body,
        "scroll": tabela_scroll,
        "atualizar": atualizar_tabela
    }