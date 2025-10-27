import flet as ft

cliente = 'Maxloc'
entrega = '25/11'
escoras_prontas = 1
escoras_falta = 7
total_pedido = 10

class Janela:
    def __init__(self):
        pass

    def _configurar_janela(self, page: ft.Page):
        page.title = "LSV"
        page.window_width = 250
        page.window_height = 300
        page.padding = 20
        page.bgcolor = "#F5F5F5"

    def _max_loc(self, page: ft.Page):
        progresso = escoras_prontas / total_pedido

        # Container pai (card)
        card = ft.Container(
            width=300,
            height=250,
            padding=ft.padding.only(top=5, right=10, bottom=5, left=10),
            bgcolor="#E3E3E3",
            border_radius=10,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Text(
                                cliente,
                                size=18,
                                weight="bold",

                            ),
                            ft.Column(
                                spacing=-5,
                                controls=[
                                ft.Text(
                                    f'Entrega',
                                    size=16,
                                    ),
                                ft.Text(
                                    entrega,
                                    size=16,
                                    color="#555555"
                                )
                                ]
                            )

                        ]
                    ),
                    # Informações do pedido
                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Column(
                                spacing=-5,
                                controls=[
                                    ft.Text(
                                        "Total:"
                                    ),
                                    ft.Text(
                                        f"{total_pedido} Escoras."
                                    )
                                ]
                            ),
                            ft.Column(
                                spacing=-5,
                                controls=[
                                    ft.Text(
                                        "Prontas:"
                                    ),
                                    ft.Text(
                                        f"{escoras_prontas} Escoras."
                                    )
                                ]
                            ),
                            ft.Column(
                                spacing=-5,
                                controls=[
                                    ft.Text(
                                        "Faltam:"
                                    ),
                                    ft.Text(
                                        f"{total_pedido - escoras_prontas} Escoras."
                                    )
                                ]
                            )
                        ]
                    ),
                    # Barra de progresso
                    ft.Column(
                        spacing=5,
                        controls=[
                            # Linha com "Progresso:" e percentual
                            ft.Row(
                                spacing=20,
                                controls=[
                                    ft.Text(
                                            "Progresso:",
                                            size=10,
                                            font_family="inter"
                                            ),
                                    ft.Text(
                                        f"{int(progresso * 100)}%",
                                        size=15, weight="bold",
                                        font_family="inter"
                                    ),
                                ]
                            ),
                            # Barra de progresso embaixo
                            ft.ProgressBar(
                                width=330,
                                height=20,
                                value=progresso,
                                border_radius=10,
                                bgcolor="#E3AE78",
                                color='#E47B12'
                            )
                        ]
                    )
                ]
            )
        )

        page.add(card)

    def run(self, page: ft.Page):
        self._configurar_janela(page)
        self._max_loc(page)


