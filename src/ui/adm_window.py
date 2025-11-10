import flet as ft

class AdmWindow:
    def __init__(self):
        pass

    def _adm_window_(self,page: ft.Page):
        page.title = "ADM"
        page.window_width = 554
        page.window_height = 444
        page.padding = ft.padding.only(left=20, top=20, right=20, bottom=0)
        page.bgcolor = "#F8F8F8"

    def run (self, page: ft.Page):
        self._adm_window_(page)
        page.add()
