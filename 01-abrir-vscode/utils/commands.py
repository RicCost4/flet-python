import subprocess

def executar_comando_git(comando, cwd):
    try:
        resultado = subprocess.run(
            comando, cwd=cwd, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return resultado.stdout or resultado.stderr
    except Exception as erro:
        return f"Erro ao executar comando: {erro}"