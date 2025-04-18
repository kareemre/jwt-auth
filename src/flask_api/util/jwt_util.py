from datetime import datetime, timedelta, timezone
import jwt
from flask import current_app
from flask_api import result

def encode_access_token(user): 
    """Generates a JWT access token for the given user ID.
    :param: user: The user object for which to generate the token.
    :return: A JWT token as a string.
    """

    now = datetime.now(timezone.utc)
    token_age_h = current_app.config("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    exp = now + timedelta(hours=token_age_h, minutes=token_age_m)
    payload = {
        "exp": exp,
        "iat": now,
        "sub": user.id,
        "admin": user.admin,
    }
    key = current_app.config.get("SECRET_KEY")
    token = jwt.encode(payload, key, algorithm="HS256")
    return token

def decode_access_token(token):
    """Decodes a JWT access token and returns the user ID.
    :param: token: The JWT token to decode.
    :return: result object with user information or error
    """

    try:
        key = current_app.config.get("SECRET_KEY")
        payload = jwt.decode(token, key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        error = "Access token expired please log in again"
        return result.Fail(error)
    except jwt.InvalidTokenError:
        error = "Invalid access token, please log in again"
        return result.Fail(error)
    user_dict = dict(
        user_id=payload["sub"],
        admin=payload["admin"],
        token=token,
        expires_at=payload["exp"],
    )
    
    return result.Ok(user_dict)
