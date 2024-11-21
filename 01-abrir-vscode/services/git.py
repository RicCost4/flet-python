import flet as ft

from utils.commands import Comandos

class Git:
    # Funções GIT
    @classmethod
    def git_config_user_name(cls, evento, user_name_input:ft.TextField, output_text:ft.Text, page:ft.Page, pasta_selecionada:ft.Text) -> None:
        user_name = user_name_input.value
        if user_name:
            output_text.value = f"Usuário configurado: {user_name}"
            Comandos.executar_comando_git(comando=["git", "config", "user.name", user_name], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        else:
            output_text.value = "Por favor, insira o nome do usuário."
        page.update()

    @classmethod
    def git_config_user_email(cls, evento, user_email_input:ft.TextField, output_text:ft.Text, page:ft.Page, pasta_selecionada:ft.Text) -> None:
        user_email = user_email_input.value
        if user_email:
            output_text.value = f"Email configurado: {user_email}"
            Comandos.executar_comando_git(comando=["git", "config", "user.email", user_email], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        else:
            output_text.value = "Por favor, insira o email do usuário."
        page.update()

    @classmethod
    def git_config_url(cls, evento, set_url_input:ft.TextField, output_text:ft.Text, page:ft.Page, pasta_selecionada:ft.Text) -> None:
        url = set_url_input.value
        if url:
            output_text.value = f"URL configurada: {url}"
            Comandos.executar_comando_git(comando=["git", "remote", "set-url", "origin", url], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        else:
            output_text.value = "Por favor, insira a URL do repositório."
        page.update()

    @classmethod
    def git_pull(cls, evento, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text):
        Comandos.executar_comando_git(comando=["git", "pull"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)

    @classmethod
    def git_status(cls, evento, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text):
        Comandos.executar_comando_git(comando=["git", "status"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)

    @classmethod
    def git_checkout(cls, evento, branch_input:ft.TextField, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text):
        branch = branch_input.value
        if branch:
            Comandos.executar_comando_git(comando=["git", "checkout", branch], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        else:
            Comandos.executar_comando_git(comando=["git", "checkout"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)

    @classmethod
    def git_commit(cls, evento, mensagem: str | None, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text, commit_message_input:ft.TextField):
        Comandos.executar_comando_git(comando=["git", "add", "."], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        Comandos.executar_comando_git(comando=["git", "commit", "-m", mensagem], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)
        commit_message_input.value = None
        page.update()

    @classmethod
    def commit_fix(cls, evento, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text, commit_message_input:ft.TextField):
        mensagem = commit_message_input.value
        if mensagem:
            cls.git_commit(evento=evento, mensagem=f'Fix: {mensagem}', page=page, pasta_selecionada=pasta_selecionada, output_text=output_text, commit_message_input=commit_message_input)
        else:
            output_text.value = "Por favor, insira a mensagem de commit."
            page.update()
    
    @classmethod
    def commit_fea(cls, evento, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text, commit_message_input:ft.TextField):
        mensagem = commit_message_input.value
        if mensagem:
            cls.git_commit(evento=evento, mensagem=f'Fea: {mensagem}', page=page, pasta_selecionada=pasta_selecionada, output_text=output_text, commit_message_input=commit_message_input)
        else:
            output_text.value = "Por favor, insira a mensagem de commit."
            page.update()

    @classmethod
    def commit_arq(cls, evento, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text, commit_message_input:ft.TextField):
        mensagem = commit_message_input.value
        if mensagem:
            cls.git_commit(evento=evento, mensagem=f'Arq: {mensagem}', page=page, pasta_selecionada=pasta_selecionada, output_text=output_text, commit_message_input=commit_message_input)
        else:
            output_text.value = "Por favor, insira a mensagem de commit."
            page.update()

    @classmethod
    def git_push(cls, evento, page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text):
        Comandos.executar_comando_git(comando=["git", "push"], page=page, pasta_selecionada=pasta_selecionada, output_text=output_text)