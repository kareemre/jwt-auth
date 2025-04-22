from http import HTTPStatus
from flask import current_app, jsonify
from flask_restx import abort
from flask_api import db
from flask_api.models.user import User
from flask_api.util.jwt_util import encode_access_token, decode_access_token


def process_registration_request(email, password):
    """User registration logic.
    :params: email: the email used in registration
    :params: password: user's input password
    :return: response
    """
    if User.find_by_email(email):
        abort(HTTPStatus.CONFLICT, f"{email} already registered", status="fail")
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    access_token = encode_access_token(new_user)
    response = jsonify(
        {
            "status": "success",
            "message": f"User {email} registered successfully",
            "access_token": access_token,
            "expires_in": _get_token_expire_time,
        }
    )
    response.status_code = HTTPStatus.CREATED
    response.headers["Cache-Control"] = "no-store"
    return response

def _get_token_expire_time():
    """expiration time in seconds.
    :return: expiration time in seconds
    """
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds
    