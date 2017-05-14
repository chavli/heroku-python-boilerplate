"""
   handles hashes, encryption, and token generation
"""
import traceback
import jwt
import os
import time
import datetime as dt
from passlib.context import CryptContext

_cryptcxt = CryptContext(
        schemes=["sha256_crypt"],
        sha256_crypt__default_rounds=1000,
        sha256_crypt__salt_size=16
    )


def generate_token(payload: dict, exp_seconds: int) -> str:
    """ generate a JWT with the given payload. uses HMAC + SHA-256 hash algorithm. the token 
    expires after the given number of seconds. """
    jwt_secret = os.getenv("JWT_SECRET")
    jwt_iss = os.getenv("JWT_ISS")

    if os.getenv("DEBUG"):
        # if running in debug mode, use timezone of machine
        payload["iat"] = int(dt.datetime.now().timestamp())
        payload["exp"] = int((dt.datetime.now() + dt.timedelta(seconds=exp_seconds)).timestamp())
    else:
        # if running in production, use UTC
        payload["iat"] = int(dt.datetime.utcnow().timestamp())
        payload["exp"] = int((dt.datetime.utcnow() + dt.timedelta(seconds=exp_seconds)).timestamp())

    payload["iss"] = jwt_iss

    try:
        token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        return token.decode("utf-8")
    except Exception as e:
        raise(e)


def verify_token(token: str) -> bool:
    """ verify a fetchy fox JWT """
    jwt_secret = os.getenv("JWT_SECRET")
    jwt_iss = os.getenv("JWT_ISS")
    try:
        jwt.decode(token, jwt_secret, issuer=jwt_iss)
        return True
    except Exception as e:
        traceback.print_exc()
        return False


def generate_hash(text: str) -> str:
    """ hash the given text data using pbkdf2_sha256. this should be used for passwords and other sensitive
    info """
    h = _cryptcxt.encrypt(text)
    return h


def verify_hash(text: str, hash: str) -> bool:
    """ verify the given text against the given hash. """
    return _cryptcxt.verify(text, hash)
