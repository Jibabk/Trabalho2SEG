import jwt
import datetime

SECRET_KEY = "segredo-super-seguro"

def gerar_token(usuario):
    payload = {
        "sub": usuario,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # dicionário válido
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
