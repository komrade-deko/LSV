import sqlite3
import os
from src.modules.utils import *

pedidos_producao = 47
menu_lateral_style = ft.ButtonStyle(color="black",text_style=ft.TextStyle(font_family="JosefinLight",size=16,weight=ft.FontWeight.BOLD),alignment=ft.alignment.center_left)

class AdmWindow:
    def __init__(self):
        self.filtro_clientes = ""
        self.filtro_estoque = ""
        self.tabela_body = None
        self.pesquisa_input = None

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DB_PATH = os.path.join(BASE_DIR, "database", "clientes.db")

    def conectar(self):
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        return conn, cursor

    def _adm_window_(self, page: ft.Page):
        page.title = "ADM"
        page.window_width = 554
        page.window_height = 444
        page.padding = ft.padding.only(left=0, top=0, right=0, bottom=0)
        page.bgcolor = "#F8F8F8"

    def _menu_logo_(self):
        lsv = ft.Image(
            src="icon.png",
            width=50,
            height=50
        )
        nome = ft.Text(
            "LSV",
            font_family="JosefinLight",
            size=18,
            color="black",
            weight=ft.FontWeight.BOLD,
        )

        return ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[lsv, nome]
            )
        )

    def _menu_lateral_(self, page: ft.Page):
        def confirmar_saida():
            def fechar(e):
                dialog.open = False
                page.update()

            def sair(e):
                page.window.close()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Sair"),
                content=ft.Text("Tem certeza que deseja sair?"),
                actions=[
                    ft.TextButton("Sair",style=salvar_style ,on_click=sair,),
                    ft.TextButton("Cancelar", on_click=fechar, style=cancelar_style),

                ],
                actions_alignment="end",
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        def go_home(e):
            self.main_content.content = self._pedidos_()
            set_fab(page, "#E47B12", self._abrir_modal_pedido_)
            self.main_content.update()

        def go_clientes(e):
            self.main_content.content = self._clientes_()
            set_fab(page, "pink", self._abrir_modal_clientes_)
            self.main_content.update()
            page.update()

        def go_produtos(e):
            self.main_content.content = self._estoque_()
            set_fab(page, "green", self._abrir_modal_estoque_)
            self.main_content.update()
            page.update()



        links = [
            ft.TextButton(
                "Início",
                width=400,
                on_click=go_home,
                style=menu_lateral_style
            ),

            ft.TextButton(
                "Clientes",
                width=500,
                on_click=go_clientes,
                style=menu_lateral_style
            ),

            ft.TextButton(
                "Produtos",
                width=500,
                on_click=go_produtos,
                style=menu_lateral_style
            ),

            #botao de sair fechar janela

            ft.TextButton(
                "Sair",
                width=500,
                on_click=lambda e: confirmar_saida(),
                style=menu_lateral_style
            )
        ]
        menu = ft.Container(
            width=200,
            bgcolor="#E3E3E3",
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            margin=ft.margin.only(top=10, bottom=10),
            content=ft.Column(
                spacing=10,
                controls=[
                    self._menu_logo_(),
                    *links
                ]
            )
        )

        return menu

    def _abrir_modal_pedido_(self, page):
        opcoes_pedido = [
            "Bandeja", "Bandenja(quina)", "Escora", "Tripe",
            "Andaime Tubular", "Andaime Fachadeiro", "Viga Matalica",
            "Barra de Ancoragem", "Aprumador de Pilar", "Forcado"
        ]

        linhas_container = ft.ListView(spacing=5, height=90, auto_scroll=False)

        def atualizar_opcoes():
            usadas = {linha.dropdown.value for linha in linhas_container.controls if linha.dropdown.value}
            for linha in linhas_container.controls:
                atual = linha.dropdown.value
                linha.dropdown.options = [
                    ft.dropdown.Option(text=s)
                    for s in opcoes_pedido
                    if s == atual or s not in usadas
                ]

        def atualizar_botoes():
            total = len(linhas_container.controls)
            limite = len(opcoes_pedido)

            for i, linha in enumerate(linhas_container.controls):
                linha.btn_add.visible = False
                linha.btn_add.disabled = True
                linha.btn_add.opacity = 0

                linha.btn_remove.visible = True
                linha.btn_remove.disabled = (i == 0)
                linha.btn_remove.opacity = 0 if i == 0 else 1

            if total < limite:
                ultimo = linhas_container.controls[-1]
                ultimo.btn_add.visible = True
                ultimo.btn_add.disabled = False
                ultimo.btn_add.opacity = 1

            page.update()

        def criar_linha():
            linha = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START)

            dropdown = ft.Dropdown(
                label="Pedido",
                hint_text="Selecione uma opção",
                width=180,
                options=[ft.dropdown.Option(text=s) for s in opcoes_pedido],
                on_change=lambda e: (limpar_erro(e), atualizar_opcoes(), atualizar_botoes())
            )

            quantidade = ft.TextField(
                label="Qnt.",
                width=77,
                on_change=lambda e: (apenas_numeros(e), limpar_erro(e))
            )

            btn_add = ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=lambda e: adicionar_linha())
            btn_remove = ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=lambda e, l=linha: remover_linha(l))

            add_container = ft.Container(
                content=btn_add,
                width=40)
            remove_container = ft.Container(
                content=btn_remove,
                width=40)

            linha.controls = [
                add_container,
                ft.Column([dropdown], tight=True),
                ft.Column([quantidade], tight=True),
                remove_container
            ]

            linha.dropdown = dropdown
            linha.quantidade = quantidade
            linha.btn_add = btn_add
            linha.btn_remove = btn_remove

            return linha

        def adicionar_linha():
            if len(linhas_container.controls) >= len(opcoes_pedido):
                return

            nova = criar_linha()
            linhas_container.controls.append(nova)

            atualizar_opcoes()
            atualizar_botoes()

        def remover_linha(linha):
            if linha not in linhas_container.controls:
                return

            if linhas_container.controls.index(linha) == 0:
                return

            linhas_container.controls.remove(linha)
            atualizar_opcoes()
            atualizar_botoes()

        adicionar_linha()

        first = linhas_container.controls[0]
        first.btn_remove.visible = True
        first.btn_remove.disabled = True
        first.btn_remove.opacity = 0

        atualizar_opcoes()
        atualizar_botoes()

        cliente_field = ft.TextField(label="Cliente", on_change=limpar_erro)
        data_field = ft.TextField(
            label="Data de Entrega",
            hint_text="(DD/MM/AAAA)",
            on_change=lambda e: (formatar_data(e), limpar_erro(e))
        )

        def salvar_modal(e):
            erro = False

            if not validar_campos_obrigatorios(cliente_field, data_field):
                erro = True

            pedidos = []

            for linha in linhas_container.controls:
                if not validar_campos_obrigatorios(linha.dropdown, linha.quantidade):
                    erro = True

                pedidos.append({
                    "item": linha.dropdown.value,
                    "qtd": linha.quantidade.value
                })

            if erro:
                return

            print("Cliente:", cliente_field.value)
            print("Data de Entrega:", data_field.value)
            print("Pedidos:", pedidos)

            modal.open = False
            page.update()

        modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Adicionar Pedidos.", font_family="JosefinBold", size=20),
                    cliente_field,
                    data_field,
                    linhas_container
                ],
                spacing=10,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton("Salvar",style=salvar_style, on_click=salvar_modal),
                ft.TextButton("Cancelar",style=cancelar_style, on_click=lambda e: fechar_modal(modal, page)),
            ],
            shape=ft.RoundedRectangleBorder(radius=7)
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def _abrir_modal_clientes_(self, page):
        conn, cursor = self.conectar()

        nome_cliente = ft.TextField(
            label="Cliente",
            on_change=limpar_erro
        )

        email_cliente = ft.TextField(
            label="Email",
            on_change=limpar_erro
        )

        telefone_cliente = ft.TextField(
            label="Telefone",
            hint_text="(XX) XXXXXXXXX",
            on_change=formatar_telefone
        )

        def salvar_modal(e):
            if not validar_campos_obrigatorios(nome_cliente, telefone_cliente):
                return

            cursor.execute("""
                INSERT INTO clientes (nome, email, telefone)
                VALUES (?, ?, ?)
            """, (
                nome_cliente.value.strip(),
                email_cliente.value.strip() if email_cliente.value else None,
                telefone_cliente.value.strip()
            ))

            conn.commit()
            conn.close()

            fechar_modal(modal, page)

            self.main_content.content = self._clientes_()
            self.main_content.update()

        modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Adicionar Cliente", font_family="JosefinBold", size=20),
                    nome_cliente,
                    email_cliente,
                    telefone_cliente,
                ],
                spacing=10,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton(
                    "Salvar", style=salvar_style, on_click=salvar_modal
                ),
                ft.TextButton(
                    "Cancelar", style=cancelar_style,
                    on_click=lambda e: fechar_modal(modal, page)
                )
            ],
            shape=ft.RoundedRectangleBorder(radius=7)
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def _abrir_modal_estoque_(self, page):
        conn, cursor = self.conectar()
        produto = ft.TextField(
            label="Produto",
            on_change=limpar_erro
        )

        preco = ft.TextField(
            label="Preço",
            prefix_text="R$",
            on_change=limpar_erro
        )

        estoque = ft.TextField(
            label = "Estoque",
            on_change=lambda e: (apenas_numeros(e), limpar_erro(e))
        )

        def salvar_modal(e):
            if not validar_campos_obrigatorios(produto, preco, estoque):
                return
            cursor.execute("""
                            INSERT INTO produtos (nome, preco, estoque)
                            VALUES (?, ?, ?)
                        """, (
                produto.value.strip(),
                preco.value.strip(),
                estoque.value.strip()
            ))

            conn.commit()
            conn.close()

            fechar_modal(modal, page)

            self.main_content.content = self._estoque_()
            self.main_content.update()

        modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Adicionar Produto", font_family="JosefinBold", size=20),
                    produto,
                    preco,
                    estoque
                ],
                spacing=10,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton(
                    "Salvar",
                    on_click=salvar_modal,
                    style=salvar_style,
                ),
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: fechar_modal(modal, page),
                    style=cancelar_style,
                )
            ],
            shape=ft.RoundedRectangleBorder(radius=7)
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def _pedidos_(self):
        menu_superior = ft.Container(
            expand=True,
            bgcolor="#FDF4F5",
            width=200,
            border_radius=ft.border_radius.only(top_right=20, top_left=20),
            alignment=ft.alignment.top_left,
            margin=ft.margin.only(top=10, left=5, right=10),
            padding=ft.padding.only(top=10, left=10, right=20),
            content=ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text(
                        "Pedidos",
                        font_family="JosefinBold",
                        size=22,
                    ),
                    ft.Row(
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=300,
                                height=100,
                                bgcolor="white",
                                border_radius=15,
                                padding=ft.padding.all(10),
                                border=ft.border.all(1, "#CBCBCB"),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=15,
                                    controls=[
                                        ft.Container(
                                            ft.Image(
                                                src="loja.svg",
                                                width=50,
                                                height=50,
                                            ),
                                            margin=ft.margin.only(left=20),
                                        ),
                                        ft.Column(
                                            spacing=-10,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    "47",
                                                    font_family="JosefinBold",
                                                    size=26,
                                                ),
                                                ft.Text(
                                                    "Pedidos",
                                                    size=16,
                                                    color="#B7B89F",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(
                                width=300,
                                height=100,
                                bgcolor="white",
                                border_radius=15,
                                padding=ft.padding.all(10),
                                border=ft.border.all(1, "#CBCBCB"),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=15,
                                    controls=[
                                        ft.Container(
                                            ft.Image(
                                                src="calendario.svg",
                                                width=50,
                                                height=50,
                                            ),
                                            margin=ft.margin.only(left=20),
                                        ),
                                        ft.Column(
                                            spacing=-10,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    "47",
                                                    font_family="JosefinBold",
                                                    size=26,
                                                ),
                                                ft.Text(
                                                    "Em Produção",
                                                    size=16,
                                                    color="#B7B89F",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(
                                width=300,
                                height=100,
                                bgcolor="white",
                                border_radius=15,
                                padding=ft.padding.all(10),
                                border=ft.border.all(1, "#CBCBCB"),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.START,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=15,
                                    controls=[
                                        ft.Container(
                                            ft.Image(
                                                src="caminhao.svg",
                                                width=50,
                                                height=50,
                                            ),
                                            margin=ft.margin.only(left=20),
                                        ),
                                        ft.Column(
                                            spacing=-10,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    "47",
                                                    font_family="JosefinBold",
                                                    size=26,
                                                ),
                                                ft.Text(
                                                    "Em Entrega",
                                                    size=16,
                                                    color="#B7B89F",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    ft.Text(
                        "Graficos",
                        font_family="JosefinBold",
                        size=22,
                    ),
                ],
            ),
        )
        return menu_superior

    def _estoque_(self):
        def montar_rows():
            dados = buscar_generico(
                conectar_fn=self.conectar,
                tabela="produtos",
                colunas=["id", "nome", "preco", "estoque"],
                coluna_pesquisa=["nome"],
                texto=self.filtro_estoque
            )

            linhas = []

            for pid, nome, preco, estoque in dados:
                menu = ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Editar",
                            on_click=lambda e, pid=pid, nome=nome, preco=preco, estoque=estoque:
                            editar_generico(
                                self.page,
                                "Editar Produto",
                                ["Nome", "Preço", "Estoque"],
                                [nome, preco, estoque],
                                validar_fn=lambda vals: True,
                                salvar_sql_fn=lambda vals, pid=pid: salvar_generico(
                                    conectar_fn=self.conectar,
                                    tabela="produtos",
                                    colunas=["nome", "preco", "estoque"],
                                    id_coluna="id",
                                    item_id=pid,
                                    valores=vals
                                ),
                                atualizar_callback=lambda: (
                                    setattr(self.main_content, "content", self._estoque_()),
                                    self.main_content.update()
                                )
                            )
                        ),
                        ft.PopupMenuItem(
                            text="Apagar",
                            on_click=lambda e, pid=pid, nome=nome: confirmar_excluir_generico(
                                page=self.page,
                                titulo="Confirmar exclusão",
                                mensagem=f"Tem certeza que deseja excluir o produto '{nome}'?",
                                conectar_fn=self.conectar,
                                tabela="produtos",
                                id_coluna="id",
                                item_id=pid,
                                atualizar_callback=lambda: (
                                    self._atualizar_tabela_estoque(),
                                    self.page.update()
                                )
                            )
                        ),
                    ]
                )

                linhas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Container(ft.Text(str(pid)), width=50)),
                            ft.DataCell(ft.Container(ft.Text(nome), width=200)),
                            ft.DataCell(ft.Container(ft.Text(str(preco)), width=150)),
                            ft.DataCell(ft.Container(ft.Text(str(estoque)), width=150)),
                            ft.DataCell(menu),
                        ]
                    )
                )

            return linhas

        self.tabela_estoque_body = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("")) for _ in range(5)],
            rows=montar_rows(),
            heading_row_height=0,
            column_spacing=20,
            show_bottom_border=False,
        )

        def atualizar_tabela():
            novas = montar_rows()
            self.tabela_estoque_body.rows = novas
            self.tabela_estoque_body.update()

        self._atualizar_tabela_estoque = atualizar_tabela

        tabela_header = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Container(content=ft.Text("ID"), width=100)),
                ft.DataColumn(ft.Container(content=ft.Text("Produto"), width=250)),
                ft.DataColumn(ft.Container(content=ft.Text("Preço"), width=200)),
                ft.DataColumn(ft.Container(content=ft.Text("Estoque"), width=210)),
                ft.DataColumn(ft.Container(content=ft.Text("Menu"), width=100)),
            ],
            rows=[],
            heading_row_color="#E0E0E0",
            border=ft.border.only(bottom=ft.BorderSide(1, "#CCCCCC")),
            column_spacing=20,
        )

        tabela_scroll = ft.ListView(
            expand=True,
            controls=[ft.Container(content=self.tabela_estoque_body, expand=True)]
        )

        self.campo_pesquisa_estoque = ft.TextField(
            label="Pesquisar",
            prefix_icon=ft.Icons.SEARCH,
            value=self.filtro_estoque,
            on_change=filtrar_generico(
                instancia=self,
                campo="filtro_estoque",
                atualizar_callback=self._atualizar_tabela_estoque
            )
        )

        return ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Estoque", size=28, font_family="JosefinBold"),
                    self.campo_pesquisa_estoque,
                    ft.Container(
                        bgcolor="white",
                        padding=10,
                        border_radius=10,
                        border=ft.border.all(1, "#D2D2D2"),
                        height=500,
                        width=1000,
                        content=ft.Column(
                            spacing=0,
                            controls=[tabela_header, tabela_scroll]
                        )
                    )
                ]
            )
        )

    def _clientes_(self):
        def montar_rows():
            dados = buscar_generico(
                conectar_fn=self.conectar,
                tabela="clientes",
                colunas=["id", "nome", "email", "telefone", "criado_em"],
                coluna_pesquisa=["nome", "telefone"],
                texto=self.filtro_clientes
            )

            linhas = []

            for cid, nome, email, telefone, criado in dados:
                menu = ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Editar",
                            on_click=lambda e, cid=cid, nome=nome, email=email, telefone=telefone:
                            editar_generico(
                                self.page,
                                "Editar Cliente",
                                ["Nome", "Email", "Telefone"],
                                [nome, email, telefone],
                                validar_fn=lambda vals: validar_campos_obrigatorios(
                                    ft.TextField(value=vals[0]),
                                    ft.TextField(value=vals[2])
                                ),
                                salvar_sql_fn=lambda vals, cid=cid: salvar_generico(
                                    conectar_fn=self.conectar,
                                    tabela="clientes",
                                    colunas=["nome", "email", "telefone"],
                                    id_coluna="id",
                                    item_id=cid,
                                    valores=vals
                                ),
                                atualizar_callback=lambda: (
                                    setattr(self.main_content, "content", self._clientes_()),
                                    self.main_content.update()
                                )
                            )
                        ),
                        ft.PopupMenuItem(
                            text="Apagar",
                            on_click=lambda e, cid=cid, nome=nome: confirmar_excluir_generico(
                                page=self.page,
                                titulo="Confirmar exclusão",
                                mensagem=f"Tem certeza que deseja apagar o cliente '{nome}'?",
                                conectar_fn=self.conectar,
                                tabela="clientes",
                                id_coluna="id",
                                item_id=cid,
                                atualizar_callback=lambda: (
                                    self._atualizar_tabela(),
                                    self.page.update()
                                )
                            )
                        ),
                    ]
                )

                linhas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Container(ft.Text(str(cid)), width=50)),
                            ft.DataCell(ft.Container(ft.Text(nome), width=200)),
                            ft.DataCell(ft.Container(ft.Text(email if email else "-"), width=250)),
                            ft.DataCell(ft.Container(ft.Text(telefone if telefone else "-"), width=150)),
                            ft.DataCell(ft.Container(ft.Text(str(criado)), width=150)),
                            ft.DataCell(menu),
                        ]
                    )
                )

            return linhas

        self.tabela_body = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("")) for _ in range(6)],
            rows=montar_rows(),
            heading_row_height=0,
            column_spacing=20,
            show_bottom_border=False,
        )

        def atualizar_tabela():
            novas = montar_rows()
            self.tabela_body.rows = novas
            self.tabela_body.update()

        self._atualizar_tabela = atualizar_tabela

        tabela_header = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Container(content=ft.Text("ID"), width=50)),
                ft.DataColumn(ft.Container(content=ft.Text("Nome"), width=200)),
                ft.DataColumn(ft.Container(content=ft.Text("Email"), width=250)),
                ft.DataColumn(ft.Container(content=ft.Text("Telefone"), width=150)),
                ft.DataColumn(ft.Container(content=ft.Text("Criado em"), width=150)),
                ft.DataColumn(ft.Container(content=ft.Text("Menu"), width=50)),
            ],
            rows=[],
            heading_row_color="#E0E0E0",
            border=ft.border.only(bottom=ft.BorderSide(1, "#CCCCCC")),
            column_spacing=20,
        )

        tabela_scroll = ft.ListView(
            expand=True,
            controls=[ft.Container(content=self.tabela_body, expand=True)]
        )

        self.campo_pesquisa = ft.TextField(
            label="Pesquisar",
            prefix_icon=ft.Icons.SEARCH,
            value=self.filtro_clientes,
            on_change=filtrar_generico(
                instancia=self,
                campo="filtro_clientes",
                atualizar_callback=self._atualizar_tabela
            )
        )

        return ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Clientes", size=28, font_family="JosefinBold"),
                    self.campo_pesquisa,
                    ft.Container(
                        bgcolor="white",
                        padding=10,
                        border_radius=10,
                        border=ft.border.all(1, "#D2D2D2"),
                        height=500,
                        width=1000,
                        content=ft.Column(
                            spacing=0,
                            controls=[tabela_header, tabela_scroll]
                        )
                    )
                ]
            )
        )

    def run(self, page: ft.Page):
        self.page = page
        self._adm_window_(page)

        self.main_content = ft.Container(
            expand=True,
            content=self._pedidos_()
        )

        layout = ft.Row(
            expand=True,
            controls=[
                self._menu_lateral_(page),
                self.main_content,
            ]
        )

        page.add(layout)
        set_fab(page, "#E47B12", self._abrir_modal_pedido_)