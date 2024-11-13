import flet as ft
from flet import Page
import os
from tkinter import filedialog, Tk
import subprocess

color_purple = "#7d3c98"
color_white = "#ffffff"

def main(page: Page) -> None:
    # Define o tamanho da janela e o título
    page.title = "Administrar VSCode e GIT - Flet Python"
    page.window_height = 700
    page.window_width = 550
    # Implementar cor de fundo da página
    # page.bgcolor = "#f0f0f0"

    # Oculta a janela do Tkinter (usada apenas para selecionar a pasta)
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.lift()

    # Variáveis para armazenar o caminho da pasta e entrada de usuário
    pasta_selecionada = ft.Text(
        value="Nenhuma pasta selecionada",
        size=14, color=color_purple,
        weight='bold',
    )
    branch_input = ft.TextField(
        label="Nome da Branch",
    )
    commit_message_input = ft.TextField(
        label="Mensagem do Commit",
    )
    # Container para saída do terminal
    output_text = ft.Text(
        value="Resultado do comando aparecerá aqui",
        size=12, color=color_purple,
        weight='bold'
    )

    # Função para executar comandos Git na pasta selecionada
    def executar_comando_git(comando):
        try:
            # Executa o comando na pasta selecionada
            resultado = subprocess.run(
                comando, cwd=pasta_selecionada.value.replace("Pasta selecionada: ", ""),
                text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output_text.value = resultado.stdout or resultado.stderr
            page.update()
        except Exception as erro:
            output_text.value = f"Erro ao executar comando: {erro}"
            page.update()

    # Funções para cada comando VSCode, Terminal e GIT
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

    def git_pull(e):
        executar_comando_git(["git", "pull"])

    def git_status(e):
        executar_comando_git(["git", "status"])

    def git_checkout(e):
        branch = branch_input.value
        if branch:
            executar_comando_git(["git", "checkout", branch])
        else:
            executar_comando_git(["git", "checkout"])
            page.update()

    def git_add(e):
        executar_comando_git(["git", "add", "."])
        output_text.value = "Mapeados arquivos para commits"
        page.update()

    def git_commit(e):
        mensagem = commit_message_input.value
        if mensagem:
            executar_comando_git(["git", "commit", "-m", mensagem])
        else:
            output_text.value = "Por favor, insira a mensagem de commit."
            page.update()

    def git_push(e):
        executar_comando_git(["git", "push"])

    # Botões e elementos da interface
    botao_selecionar = ft.ElevatedButton("Selecionar Pasta", on_click=selecionar_pasta, bgcolor=color_purple, color=color_white)
    botao_abrir_vscode = ft.ElevatedButton("Abrir VSCode", on_click=abrir_vscode, bgcolor=color_purple, color=color_white)
    botao_abrir_terminal = ft.ElevatedButton("Abrir Terminal", on_click=abrir_terminal_powershell, bgcolor=color_purple, color=color_white)
    botao_pull = ft.ElevatedButton("Git Pull", on_click=git_pull, bgcolor=color_purple, color=color_white)
    botao_status = ft.ElevatedButton("Git Status", on_click=git_status, bgcolor=color_purple, color=color_white)
    botao_checkout = ft.ElevatedButton("Git Checkout", on_click=git_checkout, bgcolor=color_purple, color=color_white)
    botao_add = ft.ElevatedButton("Git Add .", on_click=git_add, bgcolor=color_purple, color=color_white)
    botao_commit = ft.ElevatedButton("Git Commit", on_click=git_commit, bgcolor=color_purple, color=color_white)
    botao_push = ft.ElevatedButton("Git Push", on_click=git_push, bgcolor=color_purple, color=color_white)

    #Alinhando as interface em container
    container_um = ft.Container(
        content=ft.Row(
            controls=[
                botao_selecionar,
                botao_abrir_vscode,
                botao_abrir_terminal,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )
    container_dois = ft.Container(
        content=ft.Row(
            controls=[
                botao_pull,
                botao_status,
                botao_checkout,
                botao_add
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        alignment=ft.alignment.center
    )
    container_tres = ft.Container(
        content=ft.Row(
            controls=[
                botao_commit,
                botao_push,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )

    # Adiciona os elementos à página dentro de uma coluna com barra de rolagem
    page.add(
        ft.Column(
            [
                pasta_selecionada,
                container_um,
                branch_input,
                container_dois,
                commit_message_input,
                container_tres,
                output_text,
            ],
            scroll="always"
        )
    )

# Executa o aplicativo Flet
ft.app(target=main)