import requests # type: ignore
import urllib3 # type: ignore

# Desativando aviso de certificado autoassinado (apenas para testes)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://localhost:4443"

try:
    response = requests.get(URL, verify=False)  # Não verifica SSL (apenas para testes locais)
    print(f"Status Code: {response.status_code}")
    print(f"Resposta:\n{response.text}")
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
