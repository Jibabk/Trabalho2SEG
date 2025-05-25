import jwt
import datetime

PRIVATE_KEY_PATH = "keys/private.pem"
PUBLIC_KEY_PATH = "keys/public.pem"
SECRET_KEY = "segredo-super-seguro"

def gerar_token(usuario, algoritmo="hmac"):
    payload = {
        "sub": usuario,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
    }

    if algoritmo == "pss":
        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = f.read()
        token = jwt.encode(payload, private_key, algorithm="PS256")
    elif algoritmo == "hmac":
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    else:
        raise ValueError("Algoritmo desconhecido")

    return token

def verificar_token(token, algoritmo="hmac"):
    try:
        if algoritmo == "pss":
            with open(PUBLIC_KEY_PATH, "rb") as f:
                public_key = f.read()
            payload = jwt.decode(token, public_key, algorithms=["PS256"])
        elif algoritmo == "hmac":
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # dicionário válido
        else:
            raise ValueError("Algoritmo desconhecido")
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
