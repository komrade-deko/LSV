import os
import sqlite3
from src.modules.utils import *

menu_lateral_style = ft.ButtonStyle(color="black",text_style=ft.TextStyle(font_family="JosefinLight",size=16,weight=ft.FontWeight.BOLD),alignment=ft.alignment.center_left)

class AdmWindow:
    def __init__(self):
        self.filtro_clientes = ""
        self.filtro_estoque = ""
        self.filtro_pedidos = ""
        self.tabela_body = None
        self.pesquisa_input = None

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DB_PATH = os.path.join(BASE_DIR, "database", "clientes.db")

    def conectar(self):
        conn = sqlite3.connect(self.DB_PATH)
        return conn, conn.cursor()

    def _adm_window_(self, page: ft.Page):
        page.title = "ADM"
        page.window_width = 1200
        page.window_height = 800
        page.padding = 0
        page.bgcolor = "#F8F8F8"

    def _menu_logo_(self):
        lsv = ft.Image(src="icon.png", width=50, height=50)
        nome = ft.Text(
            "LSV",
            font_family="JosefinLight",
            size=18,
            color="black",
            weight=ft.FontWeight.BOLD,
        )

        return ft.Container(
            padding=10,
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
                    ft.TextButton("Sair", style=salvar_style, on_click=sair),
                    ft.TextButton("Cancelar", on_click=fechar, style=cancelar_style),
                ],
                actions_alignment="end",
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        links = [
            ft.TextButton("Início", width=400, on_click=lambda e: self._navegar_para("pedidos"),
                          style=menu_lateral_style),
            ft.TextButton("Clientes", width=500, on_click=lambda e: self._navegar_para("clientes"),
                          style=menu_lateral_style),
            ft.TextButton("Produtos", width=500, on_click=lambda e: self._navegar_para("estoque"),
                          style=menu_lateral_style),
            ft.TextButton("Sair", width=500, on_click=lambda e: confirmar_saida(), style=menu_lateral_style)
        ]

        return ft.Container(
            width=200,
            bgcolor="#E3E3E3",
            padding=10,
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            margin=ft.margin.only(top=10, bottom=10),
            content=ft.Column(
                spacing=10,
                controls=[self._menu_logo_(), *links]
            )
        )

    def _navegar_para(self, destino):
        destinos = {
            "pedidos": (self._pedidos_, "#E47B12", self._abrir_modal_pedido_),
            "clientes": (self._clientes_, "pink", self._abrir_modal_clientes_),
            "estoque": (self._estoque_, "green", self._abrir_modal_estoque_)
        }

        if destino in destinos:
            func, cor, modal_func = destinos[destino]
            self.main_content.content = func()
            set_fab(self.page, cor, modal_func)
            self.main_content.update()
            self.page.update()

    def _abrir_modal_pedido_(self, page):
        conn, cursor = self.conectar()
        cursor.execute("SELECT id, nome, preco FROM produtos")
        produtos_info = cursor.fetchall()
        conn.close()

        produtos_map = {}
        opcoes_pedido = []

        for prod_id, nome, preco in produtos_info:
            try:
                preco_clean = str(preco).replace('R$', '').replace('.', '').replace(',', '.').strip()
                preco_float = float(preco_clean)
            except:
                preco_float = 0.0

            produtos_map[nome] = {"id": prod_id, "preco": preco_float}
            opcoes_pedido.append(nome)

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

            if total < limite and linhas_container.controls:
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

            btn_add = ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e: adicionar_linha())
            btn_remove = ft.IconButton(icon=ft.Icons.REMOVE, on_click=lambda e, l=linha: remover_linha(l))

            linha.controls = [
                ft.Container(content=btn_add, width=40),
                ft.Column([dropdown], tight=True),
                ft.Column([quantidade], tight=True),
                ft.Container(content=btn_remove, width=40)
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
            if linha not in linhas_container.controls or linhas_container.controls.index(linha) == 0:
                return

            linhas_container.controls.remove(linha)
            atualizar_opcoes()
            atualizar_botoes()

        adicionar_linha()

        first = linhas_container.controls[0]
        first.btn_remove.disabled = True
        first.btn_remove.opacity = 0

        cliente_field = ft.TextField(label="Cliente", on_change=limpar_erro)
        data_field = ft.TextField(
            label="Data de Entrega",
            hint_text="(DD/MM/AAAA)",
            on_change=lambda e: (formatar_data(e), limpar_erro(e))
        )

        def abrir_confirmacao_criar_cliente():
            def cancelar(e):
                dialog.open = False
                page.update()

            def criar(e):
                dialog.open = False
                page.update()
                self._abrir_modal_clientes_(page)

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Cliente não encontrado"),
                content=ft.Text("Cliente não encontrado, deseja criar o cliente?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar, style=cancelar_style),
                    ft.TextButton("Criar", on_click=criar, style=salvar_style),
                ],
                actions_alignment="end",
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        def salvar_modal(e):
            if not validar_campos_obrigatorios(cliente_field, data_field):
                return

            pedidos = []
            valor_total = 0.0

            for linha in linhas_container.controls:
                if not validar_campos_obrigatorios(linha.dropdown, linha.quantidade):
                    return

                produto_nome = linha.dropdown.value
                quantidade = linha.quantidade.value

                if produto_nome and quantidade:
                    produto_info = produtos_map.get(produto_nome)
                    if produto_info:
                        preco_unitario = produto_info["preco"]
                        try:
                            qtd_int = int(quantidade) if quantidade else 0
                            valor_item = preco_unitario * qtd_int
                            valor_total += valor_item

                            pedidos.append({
                                "produto_id": produto_info["id"],
                                "produto_nome": produto_nome,
                                "quantidade": quantidade,
                                "preco_unitario": preco_unitario,
                                "valor_item": valor_item
                            })
                        except ValueError:
                            linha.quantidade.error_text = "Quantidade inválida"
                            linha.quantidade.update()
                            return

            nome_cliente = cliente_field.value.strip()
            conn, cursor = self.conectar()

            cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome_cliente,))
            row = cursor.fetchone()

            if not row:
                abrir_confirmacao_criar_cliente()
                conn.close()
                return

            cliente_id = row[0]
            cursor.execute("SELECT COALESCE(MAX(numero_pedido), 22) + 1 FROM pedidos")
            proximo_numero = cursor.fetchone()[0]

            data_entrega = data_field.value
            if data_entrega:
                try:
                    partes = data_entrega.split('/')
                    if len(partes) == 3:
                        dia, mes, ano = partes
                        data_entrega_sql = f"{ano}-{mes}-{dia}"
                    else:
                        data_field.error_text = "Formato inválido (DD/MM/AAAA)"
                        data_field.update()
                        conn.close()
                        return
                except:
                    data_field.error_text = "Data inválida"
                    data_field.update()
                    conn.close()
                    return
            else:
                data_entrega_sql = ""

            try:
                cursor.execute("""
                    INSERT INTO pedidos (cliente_id, data_entrega, numero_pedido, valor, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (cliente_id, data_entrega_sql, proximo_numero, valor_total, "Em Produção"))

                pedido_id = cursor.lastrowid

                for item in pedidos:
                    cursor.execute("""
                        INSERT INTO itens_pedido (produto_id, pedido_id, quantidade)
                        VALUES (?, ?, ?)
                    """, (item["produto_id"], pedido_id, int(item["quantidade"])))

                conn.commit()
                fechar_modal(modal, page)
                if hasattr(self, '_atualizar_tabela_pedidos'):
                    self._atualizar_tabela_pedidos()

            except Exception as ex:
                print(f"Erro ao salvar pedido: {ex}")
            finally:
                conn.close()

        modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Adicionar Pedidos", font_family="JosefinBold", size=20),
                    cliente_field,
                    data_field,
                    linhas_container
                ],
                spacing=10,
                tight=True,
                width=400
            ),
            actions=[
                ft.TextButton("Salvar", style=salvar_style, on_click=salvar_modal),
                ft.TextButton("Cancelar", style=cancelar_style, on_click=lambda e: fechar_modal(modal, page)),
            ],
            shape=ft.RoundedRectangleBorder(radius=7)
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def _abrir_modal_clientes_(self, page):
        conn, cursor = self.conectar()

        nome_cliente = ft.TextField(label="Cliente", on_change=limpar_erro)
        email_cliente = ft.TextField(label="Email", on_change=limpar_erro)
        telefone_cliente = ft.TextField(
            label="Telefone",
            hint_text="(XX) XXXXXXXXX",
            on_change=lambda e: (formatar_telefone(e), limpar_erro(e))
        )

        def salvar_modal(e):
            nome = nome_cliente.value.strip()
            email = email_cliente.value.strip() if email_cliente.value else None
            tel = telefone_cliente.value.strip()

            if not validar_campos_obrigatorios(nome_cliente, telefone_cliente):
                return

            cursor.execute("SELECT COUNT(*) FROM clientes WHERE nome = ?", (nome,))
            if cursor.fetchone()[0] > 0:
                nome_cliente.error_text = "Cliente já existe"
                nome_cliente.update()
                return

            if email:
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE email = ?", (email,))
                if cursor.fetchone()[0] > 0:
                    email_cliente.error_text = "Email já existe"
                    email_cliente.update()
                    return

            cursor.execute("SELECT COUNT(*) FROM clientes WHERE telefone = ?", (tel,))
            if cursor.fetchone()[0] > 0:
                telefone_cliente.error_text = "Telefone já existe"
                telefone_cliente.update()
                return

            try:
                cursor.execute("""
                    INSERT INTO clientes (nome, email, telefone)
                    VALUES (?, ?, ?)
                """, (nome, email, tel))
                conn.commit()
                conn.close()
                fechar_modal(modal, page)
                self._atualizar_tabela_clientes()
            except Exception:
                email_cliente.error_text = "Erro ao salvar"
                email_cliente.update()

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
                ft.TextButton("Salvar", style=salvar_style, on_click=salvar_modal),
                ft.TextButton("Cancelar", style=cancelar_style, on_click=lambda e: fechar_modal(modal, page))
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
            on_change=lambda e: (validar_duplicado_generico(e, self.conectar, "produtos", "nome"), limpar_erro(e))
        )
        preco = ft.TextField(
            label="Preço Unitário",
            prefix_text="R$",
            on_change=lambda e: (formatar_valor(e), limpar_erro(e))
        )
        estoque = ft.TextField(
            label="Estoque",
            on_change=lambda e: (apenas_numeros(e), limpar_erro(e))
        )

        def salvar_modal(e):
            nome = produto.value.strip()
            preco_valor = preco.value.strip()
            estoque_valor = estoque.value.strip()

            if not validar_campos_obrigatorios(produto, preco, estoque):
                return

            conn2, cursor2 = self.conectar()
            cursor2.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))

            if cursor2.fetchone():
                produto.error_text = "Produto já existe"
                produto.update()
                conn2.close()
                return
            conn2.close()

            if produto.error_text:
                return

            try:
                cursor.execute(
                    "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
                    (nome, preco_valor, estoque_valor)
                )
                conn.commit()
                conn.close()
                fechar_modal(modal, page)
                self._atualizar_tabela_estoque()
            except Exception:
                produto.error_text = "Erro ao salvar"
                produto.update()

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
                ft.TextButton("Salvar", on_click=salvar_modal, style=salvar_style),
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(modal, page), style=cancelar_style)
            ],
            shape=ft.RoundedRectangleBorder(radius=7)
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    def _pedidos_(self):
        self.txt_em_producao = ft.Text("0", font_family="JosefinBold", size=26)
        self.txt_em_entrega = ft.Text("0", font_family="JosefinBold", size=26)

        colunas_config = [
            {"nome": "Número Pedido", "campo": "numero_pedido", "largura": 190, "tipo": "int", "editable": False},
            {"nome": "Cliente", "campo": "cliente_nome", "largura": 150, "tipo": "str", "editable": False},
            {"nome": "Data Entrega", "campo": "data_entrega", "largura": 100, "tipo": "str", "editable": True,"on_change": formatar_data},
            {"nome": "Valor", "campo": "valor", "largura": 150, "tipo": "float", "editable": True,"on_change": formatar_valor},
            {"nome": "Status", "campo": "status", "largura": 200, "tipo": "str", "editable": False},
        ]

        tabela = criar_tabela_generica(
            instancia=self,
            titulo_tela="Pedidos",
            nome_tabela="pedidos_com_clientes",
            colunas_config=colunas_config,
            colunas_pesquisa=["cliente_nome", "numero_pedido"],
            campo_filtro_instancia="filtro_pedidos",
            funcao_atualizar_nome="_atualizar_tabela_pedidos",
            funcao_abrir_modal=self._abrir_modal_pedido_,
            funcao_validar_editar=None
        )

        atualizar_cards_pedidos(self)

        cards_estatisticas = ft.Row(
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=300, height=100, bgcolor="white",
                    border_radius=15, padding=10, border=ft.border.all(1, "#CBCBCB"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            ft.Container(ft.Image(src="calendario.svg", width=50, height=50),
                                         margin=ft.margin.only(left=20)),
                            ft.Column(
                                spacing=-10, alignment=ft.MainAxisAlignment.CENTER,
                                controls=[self.txt_em_producao, ft.Text("Em Produção", size=16, color="#B7B89F")],
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    width=300, height=100, bgcolor="white",
                    border_radius=15, padding=10, border=ft.border.all(1, "#CBCBCB"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            ft.Container(ft.Image(src="caminhao.svg", width=50, height=50),
                                         margin=ft.margin.only(left=20)),
                            ft.Column(
                                spacing=-10, alignment=ft.MainAxisAlignment.CENTER,
                                controls=[self.txt_em_entrega, ft.Text("Em Entrega", size=16, color="#B7B89F")],
                            ),
                        ],
                    ),
                ),
            ],
        )

        return ft.Container(
            expand=True, bgcolor="#FDF4F5", width=200,
            border_radius=ft.border_radius.only(top_right=20, top_left=20),
            alignment=ft.alignment.top_left,
            margin=ft.margin.only(top=10, left=5, right=10),
            padding=ft.padding.only(top=10, left=10, right=20, bottom=20),
            content=ft.Column(
                spacing=20, horizontal_alignment=ft.CrossAxisAlignment.START,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text("Pedidos", font_family="JosefinBold", size=28),
                    cards_estatisticas,
                    tabela["titulo"],
                    tabela["pesquisa"],
                    ft.Container(
                        bgcolor="white", padding=10, border_radius=10,
                        border=ft.border.all(1, "#D2D2D2"),
                        height=500, width=1000,
                        content=ft.Column(
                            spacing=0,
                            controls=[tabela["header"], tabela["scroll"], ft.Container(height=40)]
                        )
                    ),
                    ft.Container(height=10)
                ],
            ),
        )

    def _estoque_(self):
        colunas_config = [
            {"nome": "ID", "campo": "id", "largura": 50, "tipo": "int", "editable": False},
            {"nome": "Produto", "campo": "nome", "largura": 300, "tipo": "text", "editable": True,"on_change": validar_duplicado_generico},
            {"nome": "Preço", "campo": "preco", "largura": 200, "tipo": "float", "editable": True,"on_change": formatar_valor},
            {"nome": "Estoque", "campo": "estoque", "largura": 250, "tipo": "int", "editable": True,"on_change": apenas_numeros},
        ]

        def validar_produto(vals):
            nome, preco, estoque = vals[0].strip(), vals[1].replace(",", ".").strip(), vals[2].strip()
            if not all([nome, preco, estoque]):
                return False
            try:
                float(preco)
                int(estoque)
                return True
            except:
                return False

        tabela = criar_tabela_generica(
            instancia=self,
            titulo_tela="Estoque",
            nome_tabela="produtos",
            colunas_config=colunas_config,
            colunas_pesquisa=["nome"],
            campo_filtro_instancia="filtro_estoque",
            funcao_atualizar_nome="_atualizar_tabela_estoque",
            funcao_abrir_modal=self._abrir_modal_estoque_,
            funcao_validar_editar=validar_produto
        )

        return ft.Container(
            padding=20,
            content=ft.Column(controls=[
                tabela["titulo"], tabela["pesquisa"],
                ft.Container(
                    bgcolor="white", padding=10, border_radius=10,
                    border=ft.border.all(1, "#D2D2D2"),
                    height=500, width=1000,
                    content=ft.Column(spacing=0, controls=[tabela["header"], tabela["scroll"]])
                )
            ])
        )

    def _clientes_(self):
        colunas_config = [
            {"nome": "ID", "campo": "id", "largura": 50, "tipo": "int", "editable": False},
            {"nome": "Nome", "campo": "nome", "largura": 200, "tipo": "text", "editable": True,"on_change": validar_duplicado_generico},
            {"nome": "Email", "campo": "email", "largura": 250, "tipo": "text", "editable": True,"on_change": validar_duplicado_generico},
            {"nome": "Telefone", "campo": "telefone", "largura": 150, "tipo": "text", "editable": True,"on_change": validar_duplicado_generico},
            {"nome": "Criado em", "campo": "criado_em", "largura": 150, "tipo": "date", "editable": False},
        ]

        def validar_cliente(vals):
            return bool(vals[0] and vals[0].strip() and vals[2] and vals[2].strip())

        tabela = criar_tabela_generica(
            instancia=self,
            titulo_tela="Clientes",
            nome_tabela="clientes",
            colunas_config=colunas_config,
            colunas_pesquisa=["nome", "telefone"],
            campo_filtro_instancia="filtro_clientes",
            funcao_atualizar_nome="_atualizar_tabela_clientes",
            funcao_abrir_modal=self._abrir_modal_clientes_,
            funcao_validar_editar=validar_cliente
        )

        return ft.Container(
            padding=20,
            content=ft.Column(controls=[
                tabela["titulo"], tabela["pesquisa"],
                ft.Container(
                    bgcolor="white", padding=10, border_radius=10,
                    border=ft.border.all(1, "#D2D2D2"),
                    height=500, width=1000,
                    content=ft.Column(spacing=0, controls=[tabela["header"], tabela["scroll"]])
                )
            ])
        )

    def run(self, page: ft.Page):
        self.page = page
        self._adm_window_(page)

        self.main_content = ft.Container(expand=True, content=self._pedidos_())
        layout = ft.Row(expand=True, controls=[self._menu_lateral_(page), self.main_content])

        page.add(layout)
        set_fab(page, "#E47B12", self._abrir_modal_pedido_)