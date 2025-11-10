import flet as ft
from ui.adm_window import AdmWindow

def main(page: ft.Page):
    adm = AdmWindow()
    adm.run(page)

if __name__ == '__main__':
    ft.app(target=main)