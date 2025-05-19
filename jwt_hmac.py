import jwt
import datetime

SECRET_KEY = "segredo-super-seguro"

def gerar_token(usuario):
    payload = {
        "sub": usuario,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expirado"
    except jwt.InvalidTokenError:
        return "Token inválido"
