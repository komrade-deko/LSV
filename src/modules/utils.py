import flet as ft

def apenas_numeros(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])
    e.control.value = v
    e.control.update()

def limpar_erro(e):
    c = e.control
    if c.value and c.value.strip():
        c.error_text = None
        c.border_color = None
        c.update()

def formatar_data(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])[:8]
    e.control.value = (v[:2] + ("/" + v[2:4] if len(v) >= 3 else "") +
                               ("/" + v[4:8] if len(v) >= 5 else ""))
    e.control.update()

def fechar_modal(modal, page):
    modal.open = False
    page.update()


def formatar_telefone(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])[:11]

    if len(v) >= 1:
        v = "(" + v
    if len(v) >= 3:
        v = v[:3] + ") " + v[3:]
    if len(v) >= 6:
        v = v[:6] + v[6:]

    e.control.value = v
    e.control.update()
    limpar_erro(e)


def formatar_telefone(e):
    v = ''.join([c for c in e.control.value if c.isdigit()])[:11]  # máximo 11 dígitos

    if len(v) >= 1:
        v = "(" + v
    if len(v) >= 3:
        v = v[:3] + ") " + v[3:]
    if len(v) >= 6:
        v = v[:6] + v[6:]

    e.control.value = v
    e.control.update()
    limpar_erro(e)

def validar_campos_obrigatorios(*campos):
    valido = True
    for campo in campos:
        if not campo.value or not campo.value.strip():
            campo.error_text = "⚠️ Campo Obrigatório"
            campo.border_color = "#E53935"
            campo.update()
            valido = False
    return valido

def set_fab(page, color, callback):
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=color,
        on_click=lambda e: callback(page)
    )
    page.update()
