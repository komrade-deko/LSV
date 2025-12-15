import flet as ft
import sqlite3
# #E53935 Background

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

def formatar_valor(e):
    v = e.control.value

    numeros = ""
    decimais = ""
    tem_virgula = False

    for c in v:
        if c.isdigit():
            if not tem_virgula:
                numeros += c
            else:
                if len(decimais) < 2:
                    decimais += c
        elif c == "," and not tem_virgula:
            tem_virgula = True

    if numeros == "":
        numeros = "0"

    parte_int = numeros[::-1]
    grupos = [parte_int[i:i+3] for i in range(0, len(parte_int), 3)]
    parte_int = ".".join(grupos)[::-1]

    if tem_virgula:
        num = parte_int + "," + decimais
    else:
        num = parte_int

    e.control.value = num
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

def _abrir_detalhes(instancia, nome_tabela, item_id, linha, nomes_colunas):
    numero_pedido = item_id
    cliente_nome = "N/A"
    data_entrega = "N/A"
    valor = "N/A"
    status = "N/A"

    if nome_tabela in ["pedidos", "pedidos_com_clientes"]:
        if len(linha) > 0:
            numero_pedido = linha[0] if len(linha) > 0 else item_id
            cliente_nome = linha[1] if len(linha) > 1 else "N/A"
            data_entrega = linha[2] if len(linha) > 2 else "N/A"
            valor = linha[3] if len(linha) > 3 else "N/A"
            status = linha[4] if len(linha) > 4 else "N/A"

        titulo = f"Detalhes do Pedido #{numero_pedido}"

        conn, cursor = instancia.conectar()
        cursor.execute("""
            SELECT 
                produto_nome,
                quantidade,
                preco_unitario,
                total_item
            FROM vw_itens_pedido_detalhados
            WHERE pedido_id = ?
            ORDER BY id
        """, (item_id,))

        itens = cursor.fetchall()
        conn.close()

    else:
        titulo = f"Detalhes do {nome_tabela.capitalize()} #{item_id}"
        itens = []

    tabela_info = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(content=ft.Text("Número Pedido"), width=190)),
            ft.DataColumn(ft.Container(content=ft.Text("Cliente"), width=150)),
            ft.DataColumn(ft.Container(content=ft.Text("Data Entrega"), width=100)),
            ft.DataColumn(ft.Container(content=ft.Text("Valor"), width=150)),
            ft.DataColumn(ft.Container(content=ft.Text("Status"), width=200)),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(ft.Text(str(numero_pedido)), width=190)),
                    ft.DataCell(ft.Container(ft.Text(str(cliente_nome)), width=150)),
                    ft.DataCell(ft.Container(ft.Text(str(data_entrega)), width=100)),
                    ft.DataCell(ft.Container(ft.Text(f"R$ {str(valor)}"), width=150)),
                    ft.DataCell(ft.Container(ft.Text(str(status)), width=200)),
                ]
            )
        ],
        heading_row_color="#E0E0E0",
        border=ft.border.only(bottom=ft.BorderSide(1, "#CCCCCC")),
        column_spacing=20,
    )

    container_info = ft.Container(
        bgcolor="white",
        padding=10,
        border_radius=10,
        border=ft.border.all(1, "#D2D2D2"),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    content=ft.Text("Informações do Pedido", font_family="JosefinBold", size=16, color="#273273"),
                    margin=ft.margin.only(bottom=10)
                ),
                tabela_info
            ]
        )
    )

    rows_itens = []
    for item in itens:
        produto_nome = item[0]
        quantidade = item[1]
        preco_unitario = item[2]
        total_item = item[3]

        rows_itens.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(ft.Text(produto_nome), width=400)),
                    ft.DataCell(ft.Container(ft.Text(str(quantidade)), width=200)),
                ]
            )
        )

    if not rows_itens:
        rows_itens.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(ft.Text("Nenhum item encontrado"), width=400)),
                    ft.DataCell(ft.Container(ft.Text(""), width=200)),
                ]
            )
        )

    tabela_itens = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(content=ft.Text("Produto"), width=400)),
            ft.DataColumn(ft.Container(content=ft.Text("Quantidade"), width=200)),
        ],
        rows=rows_itens,
        heading_row_color="#E0E0E0",
        border=ft.border.only(bottom=ft.BorderSide(1, "#CCCCCC")),
        column_spacing=20,
    )

    container_itens = ft.Container(
        bgcolor="white",
        padding=10,
        border_radius=10,
        border=ft.border.all(1, "#D2D2D2"),
        height=250,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    content=ft.Text("Itens do Pedido", font_family="JosefinBold", size=16, color="#273273"),
                    margin=ft.margin.only(bottom=10)
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[tabela_itens],
                        scroll=ft.ScrollMode.AUTO
                    )
                )
            ]
        )
    )

    conteudo = ft.Column(
        controls=[
            container_info,
            ft.Container(height=20),
            container_itens
        ],
        spacing=0,
        width=900,
    )

    modal = ft.AlertDialog(
        bgcolor="white",
        modal=True,
        title=ft.Text(titulo, font_family="JosefinBold", size=20, color="#273273"),
        content=conteudo,
        actions=[
            ft.TextButton("Fechar",
                          style=cancelar_style,
                          on_click=lambda e: (setattr(modal, 'open', False), instancia.page.update()))
        ],
        shape=ft.RoundedRectangleBorder(radius=7)
    )

    instancia.page.overlay.append(modal)
    modal.open = True
    instancia.page.update()

def validar_duplicado_generico(e, conectar_fn, tabela, coluna, item_id=None):
    valor = e.control.value.strip() if e.control.value else ""

    if not valor:
        e.control.error_text = None
        e.control.update()
        return

    conn, cursor = conectar_fn()

    if item_id:
        cursor.execute(
            f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} = ? AND id != ?",
            (valor, item_id)
        )
    else:
        cursor.execute(
            f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} = ?",
            (valor,)
        )

    existe = cursor.fetchone()[0] > 0
    conn.close()

    nome_label = e.control.label if hasattr(e.control, "label") else coluna.capitalize()

    if existe:
        e.control.error_text = f"{nome_label} já existe"
    else:
        e.control.error_text = None

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

def editar_generico(page,titulo,colunas,valores,validar_fn,salvar_sql_fn,atualizar_callback,on_change_handlers=None):
    campos = []
    for i in range(len(colunas)):
        label = colunas[i]
        value = str(valores[i])

        handler = None
        if on_change_handlers and i < len(on_change_handlers):
            handler = on_change_handlers[i]

        read_only = False
        lbl_lower = label.lower()

        if not handler:
            if "telefone" in lbl_lower:
                handler = lambda e: formatar_telefone(e)
            elif "data" in lbl_lower:
                handler = lambda e: formatar_data(e)

        if lbl_lower in ("criado em", "criado_em", "data_pedido"):
            read_only = True

        campo = ft.TextField(
            label=label,
            value=value,
            on_change=handler,
            read_only=read_only
        )

        campos.append(campo)

    def salvar(e):
        novos_valores = [c.value.strip() for c in campos]

        for c in campos:
            if c.error_text:
                return

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

def confirmar_excluir_generico(page,titulo,mensagem,conectar_fn,tabela,id_coluna,item_id,atualizar_callback):
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

def criar_tabela_generica(instancia, titulo_tela, nome_tabela, colunas_config, colunas_pesquisa, campo_filtro_instancia,funcao_atualizar_nome, funcao_abrir_modal, funcao_validar_editar=None, funcao_extra_editar=None):
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
            itens_menu = []

            if nome_tabela in ["pedidos", "pedidos_com_clientes"]:
                itens_menu.append(
                    ft.PopupMenuItem(
                        text="Detalhes",
                        on_click=lambda e, item_id=item_id, linha=linha: _abrir_detalhes(
                            instancia,
                            nome_tabela,
                            item_id,
                            linha,
                            nomes_colunas
                        )
                    )
                )

            itens_menu.extend([
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
                        funcao_extra_editar,
                        colunas_config
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
            ])

            menu = ft.PopupMenuButton(items=itens_menu)
            cells.append(ft.DataCell(menu))
            linhas.append(ft.DataRow(cells=cells))

        return linhas

    def _abrir_editar(instancia, nome_tabela, item_id, campos_banco, nomes_colunas, linha,funcao_validar, funcao_extra, colunas_config):

        tabela_update = "pedidos" if nome_tabela == "pedidos_com_clientes" else nome_tabela
        titulo_tabela = "Pedidos" if nome_tabela == "pedidos_com_clientes" else nome_tabela.capitalize()

        colunas_editaveis = []
        nomes_editaveis = []
        valores_editaveis = []
        on_change_handlers = []

        for i, col in enumerate(colunas_config):
            if col.get("editable", True):
                colunas_editaveis.append(col["campo"])
                nomes_editaveis.append(col["nome"])
                valores_editaveis.append(linha[i] if i < len(linha) else "")

                handler = col.get("on_change")

                if handler == validar_duplicado_generico:
                    def wrap_dup(e, campo=col["campo"]):
                        validar_duplicado_generico(
                            e,
                            instancia.conectar,
                            tabela_update,
                            campo,
                            item_id
                        )
                    on_change_handlers.append(wrap_dup)
                elif handler:
                    def wrap_handler(e, h=handler):
                        h(e)
                    on_change_handlers.append(wrap_handler)
                else:
                    on_change_handlers.append(None)

        def validar_padrao(vals):
            return True

        validar_fn = funcao_validar if funcao_validar else validar_padrao

        campos = []
        for i in range(len(colunas_editaveis)):
            campo = ft.TextField(
                label=nomes_editaveis[i],
                value=str(valores_editaveis[i]) if valores_editaveis[i] is not None else "",
                on_change=on_change_handlers[i] if i < len(on_change_handlers) else None
            )
            campos.append(campo)

        def salvar(e):
            novos_valores = [c.value.strip() for c in campos]

            for c in campos:
                if c.error_text:
                    return

            if not validar_fn(novos_valores):
                return

            salvar_generico(
                conectar_fn=instancia.conectar,
                tabela=tabela_update,
                colunas=colunas_editaveis,
                id_coluna=campos_banco[0],
                item_id=item_id,
                valores=novos_valores
            )

            if funcao_extra:
                funcao_extra()

            modal.open = False
            instancia.page.update()
            getattr(instancia, funcao_atualizar_nome)()

        modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                controls=[
                    ft.Text(f"Editar {titulo_tabela}", size=20, font_family="JosefinBold"),
                    *campos
                ],
                spacing=10,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton("Salvar", style=salvar_style, on_click=salvar),
                ft.TextButton("Cancelar",
                              style=cancelar_style,
                              on_click=lambda e: (setattr(modal, 'open', False), instancia.page.update()))
            ],
            shape=ft.RoundedRectangleBorder(radius=7)
        )

        instancia.page.overlay.append(modal)
        modal.open = True
        instancia.page.update()

    def _confirmar_excluir(instancia, nome_tabela, id_coluna, item_id, linha, nomes_colunas):
        tabela_delete = "pedidos" if nome_tabela == "pedidos_com_clientes" else nome_tabela
        nome_item = linha[1] if len(linha) > 1 else str(item_id)

        confirmar_excluir_generico(
            page=instancia.page,
            titulo="Confirmar exclusão",
            mensagem=f"Tem certeza que deseja excluir '{nome_item}'?",
            conectar_fn=instancia.conectar,
            tabela=tabela_delete,
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
        tabela_body.rows = montar_rows()
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
