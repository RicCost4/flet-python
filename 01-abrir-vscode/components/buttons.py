import flet as ft
from utils.constants import color_purple, color_white

def create_buttons(on_select_folder, on_open_vscode, on_open_terminal):
    return [
        ft.ElevatedButton("Selecionar Pasta", on_click=on_select_folder, bgcolor=color_purple, color=color_white),
        ft.ElevatedButton("Abrir VSCode", on_click=on_open_vscode, bgcolor=color_purple, color=color_white),
        ft.ElevatedButton("Abrir Terminal", on_click=on_open_terminal, bgcolor=color_purple, color=color_white),
    ]