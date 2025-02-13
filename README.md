# Trabalho2SEG
Este trabalho explora o funcionamento do protocolo HTTPS, responsável por implementar uma comunicação segura entre navegadores e servidores Web, através de métodos de criptografia, autenticação e integridade dos dados.

# Bibliotecas Utilizadas
http.server	    ->  HTTP básico em Python
ssl	Adiciona    ->  Adiciona segurança HTTPS ao servidor
requests	    ->  Cliente HTTP para fazer requisições
OpenSSL         ->	Geração e gerenciamento de certificados SSL/TLS

# Protocolos Utilizados
HTTPS (HTTP over TLS/SSL)           ->  Protocolo seguro para comunicação web
TLS (Transport Layer Security)      ->  Protocolo de criptografia para comunicação segura
SSL (Secure Sockets Layer)          ->  Antigo protocolo de segurança substituído pelo TLS
X.509                               ->  Formato de certificados digitais usado para autenticação

# Versões Utilizadas
Python	    ->  3.12.3 
OpenSSL	    ->  3.0.13
TLS	        ->  O código usa ssl.PROTOCOL_TLS_SERVER, que seleciona automaticamente a melhor versão suportada (TLS 1.2 ou 1.3)
Requests	->  2.31.0