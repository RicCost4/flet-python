import flet as ft

def main(page):
    # Define um TextField para exibir uma mensagem
    mensagem = ft.Text(value="Olá, Flet!", size=20)

    # Função para atualizar o texto ao clicar no botão
    def clique_botao(e):
        mensagem.value = "Você clicou no botão!"
        page.update()

    # Define um botão com um evento de clique
    botao = ft.ElevatedButton(text="Clique aqui", on_click=clique_botao)

    # Adiciona os elementos à página
    page.add(mensagem, botao)

# Executa o aplicativo com a função principal
ft.app(target=main)
