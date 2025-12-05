import flet as ft
import sqlite3

salvar_style = ft.ButtonStyle(
    padding=20,
    alignment=ft.alignment.center_left,
    color="#EEEEEE",
    bgcolor="#273273",
    shape=ft.RoundedRectangleBorder(radius=7),
    text_style=ft.TextStyle(size=14, font_family="inter")
)
cancelar_style = ft.ButtonStyle(
    padding=20,
    alignment=ft.alignment.center,
    color="#212121",
    bgcolor="#BDBDBD",
    shape=ft.RoundedRectangleBorder(radius=7),
    text_style=ft.TextStyle(size=14, font_family="inter")
)


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

def filtrar_generico(instancia, campo, atualizar_callback):
    def _filter(e):
        setattr(instancia, campo, e.control.value.lower())
        atualizar_callback()
    return _filter

def tabela_generica(
    page,
    instancia,
    conectar_fn,
    tabela,
    colunas,
    coluna_pesquisa,
    filtro_attr,
    titulo,
    header_titles=None,
    editar_labels=None,
    salvar_colunas=None,
    id_coluna="id",
    validar_fn_default=lambda vals: True,

):
    if header_titles is None:
        header_titles = colunas.copy()
    if editar_labels is None:
        editar_labels = colunas[1:]
    if salvar_colunas is None:
        salvar_colunas = colunas[1:]
    def montar_rows():
        texto = getattr(instancia, filtro_attr, "")
        dados = buscar_generico(
            conectar_fn=conectar_fn,
            tabela=tabela,
            colunas=colunas,
            coluna_pesquisa=coluna_pesquisa,
            texto=texto
        )

        linhas = []
        for row in dados:
            row_id = row[0]
            valores = list(row[1:])
            def make_editar_item(row_id=row_id, valores=valores):
                return ft.PopupMenuItem(
                    text="Editar",
                    on_click=lambda e, rid=row_id, vals=valores: editar_generico(
                        page,
                        f"Editar {titulo[:-1] if titulo.endswith('s') else titulo}",
                        editar_labels,
                        vals,
                        validar_fn=lambda vals_new: validar_fn_default(vals_new),
                        salvar_sql_fn=lambda vals_new, rid=rid: salvar_generico(
                            conectar_fn=conectar_fn,
                            tabela=tabela,
                            colunas=salvar_colunas,
                            id_coluna=id_coluna,
                            item_id=rid,
                            valores=vals_new
                        ),
                        atualizar_callback=lambda: atualizar_fn()
                    )
                )

            def make_apagar_item(row_id=row_id, display_text=str(row[1]) if len(row) > 1 else str(row_id)):
                return ft.PopupMenuItem(
                    text="Apagar",
                    on_click=lambda e, rid=row_id, disp=display_text: confirmar_excluir_generico(
                        page=page,
                        titulo="Confirmar exclusão",
                        mensagem=f"Tem certeza que deseja excluir '{disp}'?",
                        conectar_fn=conectar_fn,
                        tabela=tabela,
                        id_coluna=id_coluna,
                        item_id=rid,
                        atualizar_callback=lambda: atualizar_fn()
                    )
                )

            menu = ft.PopupMenuButton(
                items=[
                    make_editar_item(),
                    make_apagar_item()
                ]
            )

            cells = []
            for i, val in enumerate(row):
                txt = "-" if (val is None or (isinstance(val, str) and not val.strip())) else str(val)
                cells.append(ft.DataCell(ft.Container(ft.Text(txt), width=None)))

            cells.append(ft.DataCell(menu))

            linhas.append(ft.DataRow(cells=cells))

        return linhas

    data_body = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("")) for _ in range(len(colunas) + 1)],
        rows=montar_rows(),
        heading_row_height=0,
        column_spacing=20,
        show_bottom_border=False,
    )

    def atualizar_fn():
        novas = montar_rows()
        data_body.rows = novas
        data_body.update()

    campo_pesquisa = ft.TextField(
        label="Pesquisar",
        prefix_icon=ft.Icons.SEARCH,
        value=getattr(instancia, filtro_attr, ""),
        on_change=filtrar_generico(
            instancia=instancia,
            campo=filtro_attr,
            atualizar_callback=atualizar_fn
        )
    )

    container = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=28, font_family="JosefinBold"),
                campo_pesquisa,
                ft.Container(
                    bgcolor="white",
                    padding=10,
                    border_radius=10,
                    border=ft.border.all(1, "#D2D2D2"),
                    height=500,
                    width=1000,
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            ft.DataTable(
                                columns=[ft.DataColumn(ft.Container(content=ft.Text(h), width=250 if i > 0 else 50)) for i, h in enumerate(header_titles + [""])],
                                rows=[],
                                heading_row_color="#E0E0E0",
                                border=ft.border.only(bottom=ft.BorderSide(1, "#CCCCCC")),
                                column_spacing=20,
                            ),
                            ft.ListView(
                                expand=True,
                                controls=[ft.Container(content=data_body, expand=True)]
                            )
                        ]
                    )
                )
            ]
        )
    )
    return container, atualizar_fn, campo_pesquisa, data_body