from ui.main_window import Janela
import flet as ft


def main(page: ft.Page):
    app = Janela()
    app.run(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')