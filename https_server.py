import http.server
import ssl
import json

from utils import check_password
from jwt_hmac import gerar_token, verificar_token

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
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"Token JWT ausente ou malformado")
                return

            token = auth_header.split()[1]
            payload = verificar_token(token)

            if isinstance(payload, dict) and "sub" in payload:
                self.send_response(200)
                self.end_headers()
                response = f"Bem-vindo(a), {payload['sub']}! Aqui estão os dados secretos."
                self.wfile.write(response.encode())
            else:
                self.send_response(403)
                self.end_headers()
                self.wfile.write("Token inválido ou expirado".encode("utf-8"))

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            usuario = data.get("usuario")
            senha = data.get("senha")

            with open("users.json") as f:
                usuarios = json.load(f)

            if usuario in usuarios and check_password(senha, usuarios[usuario]):
                token = gerar_token(usuario)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(token.encode())
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write("Credenciais inválidas".encode("utf-8"))
        elif self.path == "/registro":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            usuario = data.get("usuario")
            senha = data.get("senha")

            if not usuario or not senha:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("Usuário e senha são obrigatórios".encode("utf-8"))
                return

            try:
                with open("users.json", "r") as f:
                    usuarios = json.load(f)
            except FileNotFoundError:
                usuarios = {}

            if usuario in usuarios:
                self.send_response(409)
                self.end_headers()
                self.wfile.write("Usuário já existe".encode("utf-8"))
                return

            from utils import hash_password
            usuarios[usuario] = hash_password(senha)

            with open("users.json", "w") as f:
                json.dump(usuarios, f, indent=4)

            self.send_response(201)
            self.end_headers()
            self.wfile.write("Usuário criado com sucesso".encode("utf-8"))


server_address = (HOST, PORT)
httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Servidor HTTPS rodando em https://{HOST}:{PORT}")
httpd.serve_forever()
