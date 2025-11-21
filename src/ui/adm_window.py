import flet as ft

pedidos_producao = 47

class AdmWindow:
    def __init__(self):
        pass

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

    def _menu_lateral_(self):
        links = [
            ft.TextButton("Início",
                          width = 400,
                          style=ft.ButtonStyle(
                              color="black",
                              text_style=ft.TextStyle(
                                  font_family="JosefinLight",
                                  size=16,
                                  weight=ft.FontWeight.BOLD,
                              ),
                              alignment=ft.alignment.center_left
                          )
            ),
            ft.TextButton("Clientes",
                          width = 500,
                          style=ft.ButtonStyle(
                              color= "black",
                              text_style=ft.TextStyle(
                                  font_family="JosefinLight",
                                  size=16,
                                  weight=ft.FontWeight.BOLD,
                              ),
                              alignment=ft.alignment.center_left
                          )
            ), ft.TextButton("Configurações",
                          width = 500,
                          style=ft.ButtonStyle(
                              color= "black",
                              text_style=ft.TextStyle(
                                  font_family="JosefinLight",
                                  size=16,
                                  weight=ft.FontWeight.BOLD,

                              ),
                              alignment=ft.alignment.center_left,
                          )
            ),
            ft.TextButton("Sair",
                          width = 500,
                          style=ft.ButtonStyle(
                              color= "black",
                              text_style=ft.TextStyle(
                                  font_family="JosefinLight",
                                  size=16,
                                  weight=ft.FontWeight.BOLD,

                              ),
                              alignment=ft.alignment.center_left,
                          )
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
                            # CARD 1
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
                            # CARD 2
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
                            # CARD 3
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

    def _adicionar_pedidos_(self, page):
        page.floating_action_button = ft.Container(
            content=ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                bgcolor="#E47B12",
                on_click=lambda e: self._abrir_modal_pedido_(page)
            )
        )

    def _abrir_modal_pedido_(self, page):

        def formatar_data(e):
            v = ''.join([c for c in e.control.value if c.isdigit()])[:8]
            e.control.value = (v[:2] + ("/" + v[2:4] if len(v) >= 3 else "") +
                               ("/" + v[4:8] if len(v) >= 5 else ""))
            e.control.update()

        def limpar_erro(e):
            c = e.control
            if c.value and c.value.strip():
                c.error_text = None
                c.border_color = None
                c.update()

        def fechar_modal(e=None):
            modal.open = False
            page.update()

        opcoes_pedido = ["Escoras", "Andaime", "Sapatas"]

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

        # 🔥 Função para permitir apenas números no campo quantidade
        def apenas_numeros(e):
            v = ''.join([c for c in e.control.value if c.isdigit()])
            e.control.value = v
            e.control.update()
            limpar_erro(e)

        def criar_linha():
            linha = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START)

            dropdown = ft.Dropdown(
                label="Pedido",
                hint_text="Selecione uma opção",
                options=[ft.dropdown.Option(text=s) for s in opcoes_pedido],
                on_change=lambda e: (limpar_erro(e), atualizar_opcoes(), atualizar_botoes())
            )

            quantidade = ft.TextField(
                label="Qnt.",
                width=77,
                on_change=apenas_numeros  # 🔥 aplica o filtro numérico
            )

            btn_add = ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e: adicionar_linha())
            btn_remove = ft.IconButton(icon=ft.Icons.REMOVE, on_click=lambda e, l=linha: remover_linha(l))

            add_container = ft.Container(content=btn_add, width=40)
            remove_container = ft.Container(content=btn_remove, width=40)

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

            if not cliente_field.value:
                cliente_field.error_text = "⚠️ Campo Obrigatório"
                cliente_field.border_color = "#E53935"
                cliente_field.update()
                erro = True

            if not data_field.value:
                data_field.error_text = "⚠️ Campo Obrigatório"
                data_field.border_color = "#E53935"
                data_field.update()
                erro = True

            pedidos = []
            for linha in linhas_container.controls:
                if not linha.dropdown.value:
                    linha.dropdown.error_text = "⚠️ Obrigatório"
                    linha.dropdown.border_color = "#E53935"
                    linha.dropdown.update()
                    erro = True

                if not linha.quantidade.value:
                    linha.quantidade.error_text = "⚠️ Obrigatório"
                    linha.quantidade.border_color = "#E53935"
                    linha.quantidade.update()
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
                ft.TextButton("Salvar", on_click=salvar_modal, style=ft.ButtonStyle(
                    padding=20,
                    alignment=ft.alignment.center_left,
                    color="#EEEEEE",
                    bgcolor="#273273",
                    overlay_color="#181F46",
                    shape=ft.RoundedRectangleBorder(radius=7),
                    text_style=ft.TextStyle(size=14, font_family="inter")
                )),
                ft.TextButton("Cancelar", on_click=fechar_modal, style=ft.ButtonStyle(
                    padding=20,
                    alignment=ft.alignment.center,
                    color="#212121",
                    bgcolor="#BDBDBD",
                    overlay_color="#9E9E9E",
                    shape=ft.RoundedRectangleBorder(radius=7),
                    text_style=ft.TextStyle(size=14, font_family="inter")
                )),
            ],
            shape=ft.RoundedRectangleBorder(radius=7)
        )

        page.overlay.append(modal)

        modal.open = True
        page.update()

    def run(self, page: ft.Page):
        self._adm_window_(page),
        self._adicionar_pedidos_(page)
        layout = ft.Row(
            expand=True,
            controls=[
                self._menu_lateral_(),
                self._pedidos_(),
            ]
        )

        page.add(layout)