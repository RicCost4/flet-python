import flet as ft
from utils.constants import color_purple, color_white

def create_git_config_dialog(output_text: ft.Text, page: ft.Page):
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Configurações Git", color=color_purple, weight="bold"),
    )

    user_name_input = ft.TextField(label="Nome do Usuário")
    user_email_input = ft.TextField(label="Email do Usuário")
    set_url_input = ft.TextField(label="URL do Repositório")

    def git_config_user_name(e):
        # Lógica para configurar nome de usuário
        output_text.value = f"Usuário configurado: {user_name_input.value}"
        page.update()

    def git_config_user_email(e):
        # Lógica para configurar email
        output_text.value = f"Email configurado: {user_email_input.value}"
        page.update()

    def git_config_url(e):
        # Lógica para configurar URL
        output_text.value = f"URL configurada: {set_url_input.value}"
        page.update()

    dlg.content = ft.Column(
        [
            user_name_input,
            ft.ElevatedButton("Salvar Nome", on_click=git_config_user_name, bgcolor=color_purple, color=color_white),
            user_email_input,
            ft.ElevatedButton("Salvar Email", on_click=git_config_user_email, bgcolor=color_purple, color=color_white),
            set_url_input,
            ft.ElevatedButton("Salvar URL", on_click=git_config_url, bgcolor=color_purple, color=color_white),
        ]
    )
    return dlg