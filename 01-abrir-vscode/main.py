import flet as ft
import os
from tkinter import filedialog, Tk
import subprocess

def main(page):
    # Define o tamanho da janela e o título
    page.window_width = 600
    page.window_height = 600
    page.title = "Administrar VSCode e GIT - Flet Python"

    # Oculta a janela do Tkinter (usada apenas para selecionar a pasta)
    root = Tk()
    root.withdraw()

    # Variáveis para armazenar o caminho da pasta e entrada de usuário
    pasta_selecionada = ft.Text(value="Nenhuma pasta selecionada", size=14)
    branch_input = ft.TextField(label="Nome da Branch")
    commit_message_input = ft.TextField(label="Mensagem do Commit")
    output_text = ft.Text(value="Resultado do comando aparecerá aqui", size=12)

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
    botao_selecionar = ft.ElevatedButton("Selecionar Pasta", on_click=selecionar_pasta)
    botao_abrir_vscode = ft.ElevatedButton("Abrir VSCode", on_click=abrir_vscode)
    botao_abrir_terminal = ft.ElevatedButton("Abrir Terminal", on_click=abrir_terminal_powershell)
    botao_pull = ft.ElevatedButton("Git Pull", on_click=git_pull)
    botao_status = ft.ElevatedButton("Git Status", on_click=git_status)
    botao_checkout = ft.ElevatedButton("Git Checkout", on_click=git_checkout)
    botao_add = ft.ElevatedButton("Git Add .", on_click=git_add)
    botao_commit = ft.ElevatedButton("Git Commit", on_click=git_commit)
    botao_push = ft.ElevatedButton("Git Push", on_click=git_push)

    # Adiciona os elementos à página dentro de uma coluna com rolagem
    page.add(
        #Coluna com rolagem
        ft.Column(
            controls=[
                pasta_selecionada,
                botao_selecionar,
                botao_abrir_vscode,
                botao_abrir_terminal,
                branch_input,
                botao_checkout,
                botao_pull,
                botao_status,
                botao_add,
                commit_message_input,
                botao_commit,
                botao_push,
                output_text,
            ],
            scroll="auto"
        )
    )

# Executa o aplicativo Flet
ft.app(target=main)