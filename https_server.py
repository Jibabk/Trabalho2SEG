import http.server
import ssl

HOST = 'localhost'
PORT = 4443

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Servidor HTTPS funcionando!</h1>")

server_address = (HOST, PORT)
httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)

# Criando um contexto SSL mais moderno
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")

# Envolvendo o socket no contexto SSL
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Servidor HTTPS rodando em https://{HOST}:{PORT}")
httpd.serve_forever()
