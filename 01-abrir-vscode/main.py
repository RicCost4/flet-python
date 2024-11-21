import flet as ft
from tkinter import Tk

from utils.constants import Constants
from components.components import Component
from services.git import Git
from services.terminal import Terminal


constants = Constants()
component = Component()
git = Git()
terminal = Terminal()

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
    pasta_selecionada = component.text(value="Nenhuma pasta selecionada", color=constants.color_red, size=14, weight='bold')
    branch_input = component.inputs(text_label="Nome da Branch")
    commit_message_input = component.inputs(text_label="Mensagem do Commit")
    # Container para saída do terminal
    output_text = component.text(value="Resultado do comando aparecerá aqui", color=constants.color_green, weight='bold')

    # Função para abrir a nova janela de configurações de Git
    def abrir_janela_git_config(e):
        # Inputs para nome, email e URL
        user_name_input = component.inputs(text_label="Nome do Usuário")
        user_email_input = component.inputs(text_label="Email do Usuário")
        set_url_input = component.inputs(text_label="URL do Repositório")

        # Função para fechar o modal
        def fechar_modal(e):
            dlg.open = False
            page.update()

        # Botões na janela de configuração
        botao_user_name = component.button(title="Salvar Nome", function=git.git_config_user_name(evento=e, user_name_input=user_name_input, output_text=output_text, page=page, pasta_selecionada=pasta_selecionada), color=constants.color_white)
        botao_user_email = component.button(title="Salvar Email", function=git.git_config_user_email(evento=e, user_email_input=user_email_input, output_text=output_text, page=page, pasta_selecionada=pasta_selecionada), color=constants.color_white)
        botao_set_url = component.button(title="Salvar URL", function=git.git_config_url(evento=e, set_url_input=set_url_input, output_text=output_text, page=page, pasta_selecionada=pasta_selecionada), color=constants.color_white)
        botao_fechar = component.button(title="Fechar", function=fechar_modal, bg_color=constants.color_red, color=constants.color_white)

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
        title=component.text(value="Git Config", color=constants.color_purple, weight="bold"),
    )

    # Botões da interface
    botao_selecionar = component.button(
        title="Selecionar Pasta",
        function=lambda evento: terminal.selecionar_pasta(
            evento=evento, 
            pasta_selecionada=pasta_selecionada,
            page=page),
        color=constants.color_white
    )
    botao_abrir_vscode = component.button(
        title="Abrir VSCode",
        function=lambda evento: terminal.abrir_vscode(
            evento=evento, 
            pasta_selecionada=pasta_selecionada,
            page=page,
            output_text=output_text),
        color=constants.color_white
    )
    botao_abrir_terminal = component.button(
        title="Abrir Terminal",
        function=lambda evento: terminal.abrir_terminal_powershell(
            evento=evento, 
            pasta_selecionada=pasta_selecionada,
            page=page,
            output_text=output_text),
        color=constants.color_white
    )
    botao_pull = component.button(
        title="Pull", 
        function=lambda evento: git.git_pull(
            evento=evento, 
            page=page, 
            pasta_selecionada=pasta_selecionada, 
            output_text=output_text), 
        color=constants.color_white
    )
    botao_status = component.button(
        title="Status", 
        function=lambda evento: git.git_status(
            evento=evento, 
            page=page, 
            pasta_selecionada=pasta_selecionada, 
            output_text=output_text), 
        color=constants.color_white
    )
    botao_checkout = component.button(
        title="Checkout", 
        function=lambda evento: git.git_checkout(
            evento=evento, 
            branch_input=branch_input, 
            page=page, 
            pasta_selecionada=pasta_selecionada, 
            output_text=output_text), 
        color=constants.color_white
    )
    botao_commit_fix = component.button(
        title="Commit FIX", 
        function=lambda evento: git.commit_fix(
            evento=evento, 
            page=page, 
            pasta_selecionada=pasta_selecionada, 
            output_text=output_text, 
            commit_message_input=commit_message_input), 
        color=constants.color_green, 
        bg_color=constants.color_blue2
    )
    botao_commit_fea = component.button(
        title="Commit FEA", 
        function=lambda evento: git.commit_fea(
            evento=evento, 
            page=page, 
            pasta_selecionada=pasta_selecionada, 
            output_text=output_text, 
            commit_message_input=commit_message_input), 
        color=constants.color_green, 
        bg_color=constants.color_blue2
    )
    botao_commit_arq = component.button(
        title="Commit ARQ", 
        function=lambda evento: git.commit_arq(
            evento=evento, 
            page=page, 
            pasta_selecionada=pasta_selecionada, 
            output_text=output_text, 
            commit_message_input=commit_message_input), 
        color=constants.color_green, 
        bg_color=constants.color_blue2
    )
    botao_push = component.button(
        title="Push", 
        function=lambda evento: git.git_push(
            evento=evento, 
            page=page, 
            pasta_selecionada=pasta_selecionada, 
            output_text=output_text), 
        color=constants.color_white, 
        bg_color=constants.color_blue
    )
    botao_abrir_config_git = component.button(title="Git Config", function=abrir_janela_git_config, color=constants.color_white)

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