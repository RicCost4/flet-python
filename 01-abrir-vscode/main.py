import flet as ft
from flet import Page
import os
from tkinter import filedialog, Tk
import subprocess

color_purple = "#7d3c98"
color_red = "#FF0000"
color_orange = "#FF8000"
color_green = "#00FF00"
color_white = "#ffffff"
ft_alignment = ft.MainAxisAlignment.START

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
    pasta_selecionada = ft.Text(value="Nenhuma pasta selecionada",size=14, color=color_red,weight='bold')
    branch_input = ft.TextField(label="Nome da Branch")
    commit_message_input = ft.TextField(label="Mensagem do Commit")
    # Container para saída do terminal
    output_text = ft.Text(value="Resultado do comando aparecerá aqui",size=12, color=color_green,weight='bold')

    # Função para abrir a nova janela de configurações de Git
    def abrir_janela_git_config(e):
        # Inputs para nome, email e URL
        user_name_input = ft.TextField(label="Nome do Usuário")
        user_email_input = ft.TextField(label="Email do Usuário")
        set_url_input = ft.TextField(label="URL do Repositório")

        # Funções para configurar valores
        def git_config_user_name(e):
            user_name = user_name_input.value
            if user_name:
                output_text.value = f"Usuário configurado: {user_name}"
                subprocess.run(["git", "config", "user.name", user_name], text=True)
            else:
                output_text.value = "Por favor, insira o nome do usuário."
            page.update()

        def git_config_user_email(e):
            user_email = user_email_input.value
            if user_email:
                output_text.value = f"Email configurado: {user_email}"
                subprocess.run(["git", "config", "user.email", user_email], text=True)
            else:
                output_text.value = "Por favor, insira o email do usuário."
            page.update()

        def git_config_url(e):
            url = set_url_input.value
            if url:
                output_text.value = f"URL configurada: {url}"
                subprocess.run(["git", "remote", "set-url", "origin", url], text=True)
            else:
                output_text.value = "Por favor, insira a URL do repositório."
            page.update()
        
        # Função para fechar o modal
        def fechar_modal(e):
            dlg.open = False
            page.update()

        # Botões na janela de configuração
        botao_user_name = ft.ElevatedButton(
            "Salvar Nome", on_click=git_config_user_name, bgcolor=color_purple, color=color_white
        )
        botao_user_email = ft.ElevatedButton(
            "Salvar Email", on_click=git_config_user_email, bgcolor=color_purple, color=color_white
        )
        botao_set_url = ft.ElevatedButton(
            "Salvar URL", on_click=git_config_url, bgcolor=color_purple, color=color_white
        )
        botao_fechar = ft.ElevatedButton(
            "Fechar", on_click=fechar_modal, bgcolor="#ff0000", color=color_white
        )

        # Diálogo
        dlg.content = ft.Column(
            [
                user_name_input,
                botao_user_name,
                user_email_input,
                botao_user_email,
                set_url_input,
                botao_set_url,
                botao_fechar,
            ],
            tight=True,
        )
        dlg.open = True
        page.update()

    # Dialog para configurações
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Configurações Git", color=color_purple, weight="bold"),
        on_dismiss=lambda e: print("Janela fechada!"),
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

    def git_commit(e, mensagem: str | None):
        executar_comando_git(["git", "add", "."])
        executar_comando_git(["git", "commit", "-m", mensagem])
        commit_message_input.value = None
        page.update()

    def commit_fix(e):
        mensagem = commit_message_input.value
        if mensagem:
            git_commit(e, f'Fix: {mensagem}')
        else:
            output_text.value = "Por favor, insira a mensagem de commit."
            page.update()
    
    def commit_fea(e):
        mensagem = commit_message_input.value
        if mensagem:
            git_commit(e, f'Fea: {mensagem}')
        else:
            output_text.value = "Por favor, insira a mensagem de commit."
            page.update()

    def commit_arq(e):
        mensagem = commit_message_input.value
        if mensagem:
            git_commit(e, f'Arq: {mensagem}')
        else:
            output_text.value = "Por favor, insira a mensagem de commit."
            page.update()

    def git_push(e):
        executar_comando_git(["git", "push"])

    # Botões e elementos da interface
    botao_selecionar = ft.ElevatedButton("Selecionar Pasta", on_click=selecionar_pasta, bgcolor=color_purple, color=color_white)
    botao_abrir_vscode = ft.ElevatedButton("Abrir VSCode", on_click=abrir_vscode, bgcolor=color_purple, color=color_white)
    botao_abrir_terminal = ft.ElevatedButton("Abrir Terminal", on_click=abrir_terminal_powershell, bgcolor=color_purple, color=color_white)
    botao_pull = ft.ElevatedButton("Pull", on_click=git_pull, bgcolor=color_purple, color=color_white)
    botao_status = ft.ElevatedButton("Status", on_click=git_status, bgcolor=color_purple, color=color_white)
    botao_checkout = ft.ElevatedButton("Checkout", on_click=git_checkout, bgcolor=color_purple, color=color_white)
    botao_commit_fix = ft.ElevatedButton("Commit FIX", on_click=commit_fix, bgcolor=color_purple, color=color_green)
    botao_commit_fea = ft.ElevatedButton("Commit FEA", on_click=commit_fea, bgcolor=color_purple, color=color_orange)
    botao_commit_arq = ft.ElevatedButton("Commit ARQ", on_click=commit_arq, bgcolor=color_purple, color=color_red)
    botao_push = ft.ElevatedButton("Push", on_click=git_push, bgcolor=color_purple, color=color_white)
    botao_abrir_config_git = ft.ElevatedButton("Configurações Git", on_click=abrir_janela_git_config, bgcolor=color_purple, color=color_white)

    #Alinhando as interface em container
    container_um = ft.Container(
        content=ft.Row(
            controls=[
                botao_selecionar,
                botao_abrir_vscode,
                botao_abrir_terminal,
            ],
            alignment=ft_alignment
        ),
        alignment=ft.alignment.center
    )
    container_dois = ft.Container(
        content=ft.Row(
            controls=[
                botao_pull,
                botao_status,
                botao_checkout,
                botao_push,
            ],
            alignment=ft_alignment
        ),
        alignment=ft.alignment.center
    )
    container_tres = ft.Container(
        content=ft.Row(
            controls=[
                botao_commit_fix,
                botao_commit_fea,
                botao_commit_arq,
            ],
            alignment=ft_alignment
        ),
        alignment=ft.alignment.center
    )
    container_quatro = ft.Container(
        content=ft.Row(
            controls=[
                botao_abrir_config_git,
                dlg,
            ],
            alignment=ft_alignment
        ),
        alignment=ft.alignment.center
    )

    # Adiciona os elementos à página dentro de uma coluna com barra de rolagem
    page.add(
        ft.Column(
            [
                pasta_selecionada,
                container_um,
                container_quatro,
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