import flet as ft
from datetime import date, datetime



cliente = 'Maxloc'
entrega = '25/11'
escoras_prontas = 1
escoras_falta = 7
total_pedido = 10
agenda_cliente = 'Saida de Escoras'
horario_chegada = '11:00'
horario_saida = '12:00'
agenda_pedidos = f'{horario_chegada} - {horario_saida}'
pedido_total = 500
data_entrega = '07/10'

class Janela:
    def __init__(self):
        pass

    def _configurar_janela_(self, page: ft.Page):
        page.title = "LSV"
        page.window_width = 554
        page.window_height = 444
        page.padding = ft.padding.only(left=20, top=20, right=20, bottom=0)
        page.bgcolor = "#F8F8F8"

    def _card_(self, page: ft.Page):
        progresso = escoras_prontas / total_pedido
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
                                'card 1',
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
                    ft.Column(
                        spacing=5,
                        controls=[
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
                                        size=15,
                                        weight="bold",
                                        font_family="inter"
                                    ),
                                ]
                            ),
                            ft.ProgressBar(
                                width=330,
                                height=15,
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
        card2 = ft.Container(
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
                                'card 2',
                                size=18,
                                weight="bold",
                                font_family="inter"
                            ),
                            ft.Column(
                                spacing=-5,
                                controls=[
                                ft.Text(
                                    f'Entrega',
                                    size=16,
                                    font_family="inter"
                                    ),
                                ft.Text(
                                    entrega,
                                    size=16,
                                    font_family="inter"
                                )
                                ]
                            )

                        ]
                    ),
                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Column(
                                spacing=-5,
                                controls=[
                                    ft.Text(
                                        "Total:",
                                        font_family="inter"
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
                                        "Prontas:",
                                        font_family="inter"
                                    ),
                                    ft.Text(
                                        f"{escoras_prontas} Escoras.",
                                        font_family="inter"
                                    )
                                ]
                            ),
                            ft.Column(
                                spacing=-5,
                                controls=[
                                    ft.Text(
                                        "Faltam:",
                                        font_family="inter"
                                    ),
                                    ft.Text(
                                        f"{total_pedido - escoras_prontas} Escoras.",
                                        font_family="inter"
                                    )
                                ]
                            )
                        ]
                    ),
                    ft.Column(
                        spacing=5,
                        controls=[
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
                            ft.ProgressBar(
                                width=330,
                                height=15,
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
        return ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    content=card,
                    bottom=10,
                    left=200,
                ),
                ft.Container(
                    content= card2,
                    bottom =10,
                    left = 550,
                )

            ]
        )

    def _grafico_(self, page: ft.Page):
        dia = '40'
        background = ft.Container(
            width = 850,
            height = 600,
            bgcolor="#F5F5F5",
            border_radius=21,
            alignment=ft.alignment.bottom_center
        )
        linha = ft.Container(
            width = 1.5,
            height = 240,
            bgcolor="#A6A6A6",

        )
        texto = ft.Container(
            content=ft.Text(
                dia,
                font_family="inter",
                size = 10
            )
        )

        return ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    bottom=0,
                    left=100,
                    content = ft.Stack(
                        controls=[
                            background,
                            ft.Container(
                                content=linha,
                                top=60,
                                left=100,
                            ),
                            ft.Container(
                                content=texto,
                                top=40,
                                left=95
                            )
                        ]
                    )
                )
            ]
        )

    def _logo_(self, page:ft.Page ):
        lsv = ft.Image(
            src="logo.jpg",
            width=200,
            height=200
        )
        return ft.Stack(
            controls=[
                ft.Container(
                    content=lsv,
                    right = 50,
                    top=0
                )
            ]
        )

    def _calendario_(self, page:ft.Page):
        data = date.today()
        data_formatado = data.strftime("%d/%m")
        calendario = ft.Container(
            content=ft.Column(
                spacing=-5,
                controls=[
                    ft.Text('Atividades',
                            font_family="Josefin",
                            size=35, ),
                    ft.Text(data_formatado,
                            font_family="Josefin",
                            size=35)
                ]
            )
        )
        return ft.Stack(
        expand=True,
            controls=[
                ft.Container(
                    content= calendario,
                    top=170,
                    right=50,
                )
            ]
        )

    def _atividades_(self, page: ft.Page):
        agenda = ft.Container(
            bgcolor="#F9E2CB",
            padding = ft.padding.only(left=5, top=-2, bottom=3, right=50),
                border=ft.border.only(
                    right=ft.BorderSide(3, "#E47B12")
                ),
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Text(
                        agenda_cliente,
                        font_family="inter",
                        size=20
                    ),
                    ft.Text(
                        agenda_pedidos,
                        font_family="inter",
                        size=16
                    )
                ]
            )
        )
        return ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        content=agenda,
                        top= 290,
                        right=27,
                    )
                ]
        )

    def _concluidos_(self, page:ft.Page):
        titulo = ft.Text(
            "Concluidos",
            font_family="Josefin",
            size=20,
        )
        concluidos = ft.Container(
            bgcolor="#F2F2F2",
            border_radius= 8,
            padding=ft.padding.all(12),
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "China",
                            font_family="inter",
                            weight="bold",
                            size=25),
                            padding = ft.padding.only(
                            left=-5,
                            top=-10
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Total:",
                            font_family="inter",
                            size=15
                        ),
                        margin=ft.margin.only(
                            top=-3,
                            left=-5
                        ),
                    ),
                    ft.Container(
                      content=ft.Text(
                          f"{pedido_total} Escora",
                          font_family="inter",
                          size=15
                      ),
                        margin=ft.margin.only(
                            top=-15,
                            left=-5
                        )
                    ),

                    ft.Container(
                        content=ft.Text(
                            f"Entregue: {data_entrega}",
                            font_family="inter",
                            weight="bold",
                            size=20
                        ),
                        margin=ft.margin.only(
                            top=0,
                            left=-5
                        )
                    ),
                ]
            )
        )

        return ft.Stack(
            expand=True,
            controls=[
            ft.Container(
                content=titulo,
                top=100,
                left=50
                ),
            ft.Container(
                content=concluidos,
                top=200,
                left=50
                )
            ]
        )

    def run(self, page: ft.Page):
        self._configurar_janela_(page)
        layout = ft.Stack(
            expand=True,
            controls=[
                self._grafico_(page),
                self._card_(page),
                self._logo_(page),
                self._calendario_(page),
                self._atividades_(page),
                self._concluidos_(page)
            ]
        )
        page.add(layout)