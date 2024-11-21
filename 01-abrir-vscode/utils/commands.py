import subprocess
import flet as ft

class Comandos:
    # Função para executar comandos Git na pasta selecionada
    @classmethod
    def executar_comando_git(cls, comando:list[str], page:ft.Page, pasta_selecionada:ft.Text, output_text:ft.Text = None) -> None:
        try:
            # Executa o comando na pasta selecionada
            resultado = subprocess.run(
                comando, cwd=pasta_selecionada.value.replace("Pasta selecionada: ", ""),
                text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if output_text:
                output_text.value = resultado.stdout or resultado.stderr
                page.update()
        except Exception as erro:
            print(f"Erro ao executar comando: {erro}")
            if output_text:
                output_text.value = f"Erro ao executar comando: {erro}"
                page.update()
