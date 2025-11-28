import flet as ft
salvar_style= ft.ButtonStyle(padding=20, alignment=ft.alignment.center_left, color="#EEEEEE", bgcolor="#273273", shape=ft.RoundedRectangleBorder(radius=7), text_style=ft.TextStyle(size=14, font_family="inter"))
cancelar_style = ft.ButtonStyle(padding=20,alignment=ft.alignment.center,color="#212121",bgcolor="#BDBDBD",shape=ft.RoundedRectangleBorder(radius=7),text_style=ft.TextStyle(size=14, font_family="inter"))

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


def formatar_telefone(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])[:11]  # máximo 11 dígitos

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