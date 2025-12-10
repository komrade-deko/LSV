import flet as ft
from ui.main_window import Janela

def main(page: ft.Page):
    page.fonts = {
        "Josefin": "assets/fonts/JosefinSans/JosefinSans-Medium.ttf",
        "JosefinSans": "assets/fonts/JosefinSans/JosefinSans-Bold.ttf"
    }
    app = Janela()
    app.run(page)

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets/images')