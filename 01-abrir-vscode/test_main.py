import pytest
import subprocess
from unittest.mock import patch, MagicMock
import main  # Importe seu arquivo principal

@patch("main.subprocess.run")
def test_executar_comando_git(mock_subprocess_run):
    # Configura o mock para simular um resultado do subprocess
    mock_subprocess_run.return_value = MagicMock(stdout="Pull realizado com sucesso", stderr="")

    # Chama a função que queremos testar
    main.executar_comando_git(["git", "pull"])

    # Verifica se o subprocess foi chamado com o comando correto
    mock_subprocess_run.assert_called_with(
        ["git", "pull"], cwd="Nenhuma pasta selecionada", text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
