import requests
import json

BASE_URL = "https://localhost:4443"

# Ignora warnings de certificado self-signed
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

usuario = {"usuario": "alice", "senha": "senha123"}

try:
    # LOGIN
    res = requests.post(BASE_URL + "/login",
                        json=usuario,
                        verify="certs/myCA.pem")
    if res.status_code == 200:
        token = res.text
        print("Token JWT recebido:\n", token)

        # ACESSO A DADOS PROTEGIDOS
        headers = {"Authorization": f"Bearer {token}"}
        res2 = requests.get(BASE_URL + "/dados",
                            headers=headers,
                            verify="certs/myCA.pem")
        print("\nResposta protegida:")
        print(res2.text)
    else:
        print("Falha no login:", res.text)
except requests.exceptions.RequestException as e:
    print(f"Erro na conexão: {e}")
