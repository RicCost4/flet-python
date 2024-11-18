import flet as ft
import os
from tkinter import Tk, filedialog
from utils.commands import executar_comando_git
from utils.constants import color_green, color_red
from components.git_config_dialog import create_git_config_dialog
from components.buttons import create_buttons

def main(page: ft.Page):
    page.title = "Administrar VSCode e GIT - Flet Python"
    page.window_height = 700
    page.window_width = 550

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.lift()

    pasta_selecionada = ft.Text(value="Nenhuma pasta selecionada", size=14, color=color_red, weight="bold")
    output_text = ft.Text(value="Resultado do comando aparecerá aqui", size=12, color=color_green, weight="bold")

    dlg = create_git_config_dialog(output_text, page)

    def selecionar_pasta(e):
        caminho_pasta = filedialog.askdirectory(title="Selecione uma pasta")
        if caminho_pasta:
            pasta_selecionada.value = f"Pasta selecionada: {caminho_pasta}"
            page.update()

    def abrir_terminal_powershell(e):
        caminho_pasta = pasta_selecionada.value.replace("Pasta selecionada: ", "")
        if caminho_pasta and os.path.isdir(caminho_pasta):
            # Caminho para o PowerShell 7 no Windows
            pwsh_path = r"C:\Program Files\PowerShell\7\pwsh.exe"
            if os.path.exists(pwsh_path):
                os.system(f'start "" "{pwsh_path}" -NoExit -Command "cd \'{caminho_pasta}\'"')
            else:
                output_text.value = "PowerShell 7.4.6 não encontrado no caminho padrão, abrindo o padrão."
                os.system(f"start powershell -NoExit -Command \"cd '{caminho_pasta}'\"")
                page.update()
        else:
            output_text.value = "Por favor, selecione uma pasta válida primeiro!"
            page.update()

    def abrir_vscode(e):
        caminho_pasta = pasta_selecionada.value.replace("Pasta selecionada: ", "")
        if caminho_pasta and os.path.isdir(caminho_pasta):
            os.system(f"code \"{caminho_pasta}\"")
            output_text.value = "Visual Studio Code aberto com sucesso!"
            page.update()
        else:
            output_text.value = "Por favor, selecione uma pasta válida primeiro!"
            page.update()

    page.add(
        ft.Column(
            [
                pasta_selecionada,
                ft.Row(create_buttons(selecionar_pasta, abrir_vscode, abrir_terminal_powershell)),
                dlg,
                output_text,
            ],
            scroll="always"
        )
    )

ft.app(target=main)
