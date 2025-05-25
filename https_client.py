import requests
import json

BASE_URL = "https://localhost:4443" # URL utilizada no programa

# Ignora warnings de certificado self-signed
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

usuario = {"usuario": "alice", "senha": "senha123"} # Cria objeto json com login e senha

try:
    # LOGIN
    res = requests.post(BASE_URL + "/login", # Cria requisição para logar (request POST)
                        json=usuario,
                        verify="certs/myCA.pem")
    if res.status_code == 200: # Caso seja bem sucedida a autenticação
        token = res.text # Coleta corpo da resposta HTTP em string
        print("Token JWT recebido:\n", token)

        # ACESSO A DADOS PROTEGIDOS
        headers = {"Authorization": f"Bearer {token}"} # Cria o cabeçalho do request GET
        res2 = requests.get(BASE_URL + "/dados",
                            headers=headers,
                            verify="certs/myCA.pem")
        print("\nResposta protegida:")
        print(res2.text)
    else:
        print("Falha no login:", res.text)
except requests.exceptions.RequestException as e: # Coleta o erro que ocorreu junto da requisição
    print(f"Erro na conexão: {e}")
