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
    return _create_auth_successful_response(
        token=access_token.decode(),
        status_code=HTTPStatus.CREATED,
        message="successfully registered",
    )
    
    
def process_login_request(email, password):
    """User login logic.
    :params: email: the email used in login
    :params: password: user's input password
    :return: response
    """
    
    user = User.find_by_email(email)
    if not user or not user.check_password(password):
        abort(HTTPStatus.UNAUTHORIZED, "email or password does not match", status="fail")
    access_token = encode_access_token(user)
    return _create_auth_successful_response(
        token=access_token.decode(),
        status_code=HTTPStatus.OK,
        message="successfully logged in",
    )


def _create_auth_successful_response(token, status_code, message):
    """Creates a response for successful authentication.
    :param: token: JWT token
    :param: status_code: HTTP status code
    :param: message: success message
    :return: JSON response with token and message
    """
    response = jsonify(
        
            status="success",
            message=message,
            access_token=token,
            expires_in=_get_token_expire_time(),
    )
    response.status_code = status_code
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
    