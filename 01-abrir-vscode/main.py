import flet as ft
import os
from tkinter import filedialog, Tk

from utils.constants import Constants
from utils.commands import Comandos
from utils.flet_tags import Flet_tags

constants = Constants()
flet_tags = Flet_tags()

def main(page: ft.Page) -> None:
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
    pasta_selecionada = flet_tags.text(value="Nenhuma pasta selecionada", color=constants.color_red, size=14, weight='bold')
    branch_input = flet_tags.inputs(text_label="Nome da Branch")
    commit_message_input = flet_tags.inputs(text_label="Mensagem do Commit")
    # Container para saída do terminal
    output_text = flet_tags.text(value="Resultado do comando aparecerá aqui", color=constants.color_green, weight='bold')

    # Função para abrir a nova janela de configurações de Git
    def abrir_janela_git_config(e):
        # Inputs para nome, email e URL
        user_name_input = flet_tags.inputs(text_label="Nome do Usuário")
        user_email_input = flet_tags.inputs(text_label="Email do Usuário")
        set_url_input = flet_tags.inputs(text_label="URL do Repositório")

        # Funções para configurar valores
        def git_config_user_name(e):
            user_name = user_name_input.value
            if user_name:
                output_text.value = f"Usuário configurado: {user_name}"
                Comandos.executar_comando_git(comando=["git", "config", "user.name", user_name], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
            else:
                output_text.value = "Por favor, insira o nome do usuário."
            page.update()

        def git_config_user_email(e):
            user_email = user_email_input.value
            if user_email:
                output_text.value = f"Email configurado: {user_email}"
                Comandos.executar_comando_git(comando=["git", "config", "user.email", user_email], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
            else:
                output_text.value = "Por favor, insira o email do usuário."
            page.update()

        def git_config_url(e):
            url = set_url_input.value
            if url:
                output_text.value = f"URL configurada: {url}"
                Comandos.executar_comando_git(comando=["git", "remote", "set-url", "origin", url], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
            else:
                output_text.value = "Por favor, insira a URL do repositório."
            page.update()

        # Função para fechar o modal
        def fechar_modal(e):
            dlg.open = False
            page.update()

        # Botões na janela de configuração
        botao_user_name = flet_tags.button(title="Salvar Nome", function=git_config_user_name, color=constants.color_white)
        botao_user_email = flet_tags.button(title="Salvar Email", function=git_config_user_email, color=constants.color_white)
        botao_set_url = flet_tags.button(title="Salvar URL", function=git_config_url, color=constants.color_white)
        botao_fechar = flet_tags.button(title="Fechar", function=fechar_modal, color=constants.color_red, bg_color=constants.color_white)

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
        title=flet_tags.text(value="Git Config", color=constants.color_purple, weight="bold"),
    )

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
        Comandos.executar_comando_git(comando=["git", "pull"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)

    def git_status(e):
        Comandos.executar_comando_git(comando=["git", "status"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)

    def git_checkout(e):
        branch = branch_input.value
        if branch:
            Comandos.executar_comando_git(comando=["git", "checkout", branch], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        else:
            Comandos.executar_comando_git(comando=["git", "checkout"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)

    def git_commit(e, mensagem: str | None):
        Comandos.executar_comando_git(comando=["git", "add", "."], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        Comandos.executar_comando_git(comando=["git", "commit", "-m", mensagem], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
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
        Comandos.executar_comando_git(comando=["git", "push"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)

    # Botões e elementos da interface
    botao_selecionar = flet_tags.button(title="Selecionar Pasta", function=selecionar_pasta, color=constants.color_white)
    botao_abrir_vscode = flet_tags.button(title="Abrir VSCode", function=abrir_vscode, color=constants.color_white)
    botao_abrir_terminal = flet_tags.button(title="Abrir Terminal", function=abrir_terminal_powershell, color=constants.color_white)
    botao_pull = flet_tags.button(title="Pull", function=git_pull, color=constants.color_white)
    botao_status = flet_tags.button(title="Status", function=git_status, color=constants.color_white)
    botao_checkout = flet_tags.button(title="Checkout", function=git_checkout, color=constants.color_white)
    botao_commit_fix = flet_tags.button(title="Commit FIX", function=commit_fix, color=constants.color_green, bg_color=constants.color_blue2)
    botao_commit_fea = flet_tags.button(title="Commit FEA", function=commit_fea, color=constants.color_orange, bg_color=constants.color_blue2)
    botao_commit_arq = flet_tags.button(title="Commit ARQ", function=commit_arq, color=constants.color_red, bg_color=constants.color_blue2)
    botao_push = flet_tags.button(title="Push", function=git_push, color=constants.color_white, bg_color=constants.color_blue)
    botao_abrir_config_git = flet_tags.button(title="Git Config", function=abrir_janela_git_config, color=constants.color_white)

    #Alinhando as interface em container
    container_um = ft.Container(
        content=ft.Row(
            controls=[
                botao_selecionar,
                botao_abrir_vscode,
                botao_abrir_terminal,
            ],
            alignment=constants.ft_alignment
        ),
        alignment=ft.alignment.center
    )
    container_dois = ft.Container(
        content=ft.Row(
            controls=[
                botao_pull,
                botao_status,
                botao_checkout,
                botao_abrir_config_git,
                dlg,
            ],
            alignment=constants.ft_alignment
        ),
        alignment=ft.alignment.center
    )
    container_tres = ft.Container(
        content=ft.Row(
            controls=[
                botao_commit_fix,
                botao_commit_fea,
                botao_commit_arq,
                botao_push,
            ],
            alignment=constants.ft_alignment
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