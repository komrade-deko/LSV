import flet as ft

pedidos_producao = 47

class AdmWindow:
    def __init__(self):
        pass

    def _adm_window_(self, page: ft.Page):
        page.title = "ADM"
        page.window_width = 554
        page.window_height = 444
        page.padding = ft.padding.only(left=0, top=0, right=0, bottom=0) # é necessario colocar padding 0 em cada lado para que o python coloque esses cards no ponto zero
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

    def _adicionar_pedidos_ (self, page):
        page.floating_action_button = ft.Container(
            content=ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                bgcolor="#E47B12",
                on_click=lambda e: self._abrir_modal_pedido_(page)
            ),
        )

    def _abrir_modal_pedido_(self, page):
        def _fechar_modal_(e):
            modal.open = False
            page.update()

        def _salvar_modal(e):
            pass

        def formatar_data(e):
            global formato_timer

            valor = e.control.value
            numeros = ''.join(filter(str.isdigit, valor))[:8]

            formatado = ''
            if len(numeros) >= 1:
                formatado += numeros[:2]
            if len(numeros) >= 3:
                formatado += '/' + numeros[2:4]
            if len(numeros) >= 5:
                formatado += '/' + numeros[4:8]

            e.control.value = formatado
            e.control.update()

        modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Adicionar Pedidos.",
                            font_family="JosefinBold",
                            size=20),
                    ft.TextField(
                        label="Cliente"
                    ),
                    ft.TextField(
                        label="Data (DD/MM/AAAA)",
                        on_change=formatar_data
                    ),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                label="Qnt.",
                                width=77
                            ),
                            ft.Dropdown(
                                label="Pedido",
                                hint_text="Selecione uma opção",
                                options=[
                                    ft.dropdown.Option("Escoras"),
                                    ft.dropdown.Option("Andaime")
                                ]
                            ),
                        ]
                    ),
                ],
                height=200,
            ),

            actions=[
                ft.TextButton(
                    "Salvar",
                    on_click=_salvar_modal,
                    style=ft.ButtonStyle(
                        padding=20,
                        alignment=ft.alignment.center_left,
                        color="#EEEEEE",
                        bgcolor="#273273",
                        overlay_color="#181F46",
                        shape=ft.RoundedRectangleBorder(radius=7),
                        text_style=ft.TextStyle(
                            size=14,
                            font_family="inter",
                        )
                    )
                ),
                ft.TextButton(
                    "Cancelar",
                    on_click=_fechar_modal_,
                    style=ft.ButtonStyle(
                        padding=20,
                        alignment=ft.alignment.center,
                        color="#212121",
                        bgcolor="#BDBDBD",
                        overlay_color="#9E9E9E",
                        shape=ft.RoundedRectangleBorder(radius=7),
                        text_style=ft.TextStyle(
                            size=14,
                            font_family="inter",
                        )
                    )
                )
            ],
            shape=ft.RoundedRectangleBorder(
                radius=ft.border_radius.all(7))
        )

        if modal not in page.overlay:
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