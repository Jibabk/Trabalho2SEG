import http.server 
import ssl         

HOST = 'localhost'
PORT = 4443

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

server_address = (HOST, PORT)
httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")


httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Servidor HTTPS rodando em https://{HOST}:{PORT}")
httpd.serve_forever()
