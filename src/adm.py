import flet as ft
from ui.adm_window import AdmWindow

def main(page: ft.Page):
    page.fonts = {
        "Josefin": "assets/fonts/JosefinSans/JosefinSans-Medium.ttf",
        "JosefinLight": "assets/fonts/JosefinSans/JosefinSans-ExtraLight.ttf",
        "JosefinBold" : "assets/fonts/JosefinSans/JosefinSans-Bold.ttf"
    }
    adm = AdmWindow()
    adm.run(page)

if __name__ == '__main__':
    ft.app(target=main,assets_dir='assets/images')