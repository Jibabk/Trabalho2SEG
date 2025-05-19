import jwt
import datetime

PRIVATE_KEY_PATH = "keys/private.pem"
PUBLIC_KEY_PATH = "keys/public.pem"

def gerar_token(usuario):
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = f.read()

    payload = {
        "sub": usuario,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
    }

    return jwt.encode(payload, private_key, algorithm="RS256")

def verificar_token(token):
    try:
        with open(PUBLIC_KEY_PATH, "rb") as f:
            public_key = f.read()

        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
