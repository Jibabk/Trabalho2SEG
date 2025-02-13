import requests # type: ignore

URL = "https://localhost:4443"

try:
    response = requests.get(URL, verify="certs/myCA.pem")  # Verifica o certificado da CA
    print(f"Status Code: {response.status_code}")
    print(f"Resposta:\n{response.text}")
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
