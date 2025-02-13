import requests # type: ignore

URL = "https://localhost:4443"

try:
    response = requests.get(URL, 
                            cert=("certs/client.crt", "certs/client.key"), 
                            verify="certs/myCA.pem") 
    print(f"Status Code: {response.status_code}")
    print(f"Resposta:\n{response.text}")
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
