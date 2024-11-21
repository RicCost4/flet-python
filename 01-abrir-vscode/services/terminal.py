import flet as ft
import os
from tkinter import filedialog

class Terminal:
    # Funções para cada comando VSCode, Terminal e GIT
    @classmethod
    def selecionar_pasta(cls, evento, pasta_selecionada:ft.Text, page:ft.Page):
        caminho_pasta = filedialog.askdirectory(title="Selecione uma pasta")
        if caminho_pasta:
            pasta_selecionada.value = f"Pasta selecionada: {caminho_pasta}"
            page.update()

    @classmethod
    def abrir_terminal_powershell(cls, evento, pasta_selecionada:ft.Text, output_text:ft.Text, page:ft.Page):
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

    @classmethod
    def abrir_vscode(cls, evento, pasta_selecionada:ft.Text, output_text:ft.Text, page:ft.Page):
        caminho_pasta = pasta_selecionada.value.replace("Pasta selecionada: ", "")
        if caminho_pasta and os.path.isdir(caminho_pasta):
            os.system(f"code \"{caminho_pasta}\"")
            output_text.value = "Visual Studio Code aberto com sucesso!"
            page.update()
        else:
            output_text.value = "Por favor, selecione uma pasta válida primeiro!"
            page.update()
