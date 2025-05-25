import http.server
import ssl
import json

from utils import check_password
from jwt_auth import gerar_token, verificar_token

HOST = 'localhost'
PORT = 4443

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        if self.path == "/dados":
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                self.send_response(401) # Não autorizado (sem token ou token malformado)
                self.end_headers()
                self.wfile.write(b"Token JWT ausente ou malformado")
                return

            token = auth_header.split()[1] #Pega primera string do payload
            payload = verificar_token(token, algoritmo=ALGORITMO_JWT)

            if isinstance(payload, dict) and "sub" in payload: #Sub é um tipo de claim
                self.send_response(200) # 200-> Ok
                self.end_headers()
                response = f"Bem-vindo(a), {payload['sub']}! Aqui estão os dados secretos."
                self.wfile.write(response.encode())
            else:
                self.send_response(403) # 403 -> Proibido (token inválido)
                self.end_headers()
                self.wfile.write("Token inválido ou expirado".encode("utf-8"))

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers.get('Content-Length', 0)) #retorna 0 por padrão
            body = self.rfile.read(content_length) # Lê determinada quantidade de bytes (content_length)
            data = json.loads(body) # Transforma o payload em json, isto é, dados

            usuario = data.get("usuario")   # Coleta informações para autenticar
            senha = data.get("senha")

            with open("users.json") as f: # Abre arquivo para fazer consulta
                usuarios = json.load(f)

            if usuario in usuarios and check_password(senha, usuarios[usuario]): # Verifica par usuário e senha estão no dicionário
                token = gerar_token(usuario, algoritmo=ALGORITMO_JWT) # Gera token com atributos "sub" & "exp" 
                self.send_response(200) # 200 -> Ok
                self.end_headers()
                self.wfile.write(token.encode()) #Retorna o token para ser utilizado
            else: # Caso contrário
                self.send_response(401) # Não autorizado (sem token ou token malformado)
                self.end_headers()
                self.wfile.write("Credenciais inválidas".encode("utf-8"))
        elif self.path == "/registro":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            usuario = data.get("usuario")
            senha = data.get("senha")

            if not usuario or not senha:
                self.send_response(400) # 400 -> "Bad Request" (Solicitação Inválida)
                self.end_headers()
                self.wfile.write("Usuário e senha são obrigatórios".encode("utf-8"))
                return

            try:
                with open("users.json", "r") as f:
                    usuarios = json.load(f)
            except FileNotFoundError:
                usuarios = {}

            if usuario in usuarios:
                self.send_response(409) # 409 -> Conflict
                self.end_headers()
                self.wfile.write("Usuário já existe".encode("utf-8"))
                return

            from utils import hash_password  # Caso nenhuma das condições erro ocorram
            usuarios[usuario] = hash_password(senha) # Atualiza objeto json 

            with open("users.json", "w") as f:
                json.dump(usuarios, f, indent=4) # Sobrescreve o arquivo atualizado

            self.send_response(201) # 201 -> Created
            self.end_headers()
            self.wfile.write("Usuário criado com sucesso".encode("utf-8"))



option = input(f"Antes de iniciar, escolha o cenário de autenticação (1- HMAC, 2- PSS ou 3-Sair:)")

if option == "1":
    ALGORITMO_JWT = "hmac"
elif option == "2":
    ALGORITMO_JWT = "pss"
else:
    exit()

server_address = (HOST, PORT) # Cria socket
httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler) # Cria servidor HTTP

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) # Contexto SSL/TLS criado para implementar HTTPS
context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key") # Carrega certificado do servidor junto de sua chave PK
httpd.socket = context.wrap_socket(httpd.socket, server_side=True) # Atualiza socket padrão para implementar SSL

print(f"Servidor HTTPS rodando em https://{HOST}:{PORT}")
httpd.serve_forever()
