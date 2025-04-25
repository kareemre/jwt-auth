from functools import wraps

from flask import request
from flask_api.util.jwt_util import decode_access_token
from flask_api.api.auth.exceptions import ApiUnauthorized, ApiForbidden


def token_required(f):
    """Decorator to check if the request has a valid access token.
    :param: f: function to be decorated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_payload = _check_access_token()
        for name, val in token_payload.items():
            setattr(decorated_function, name, val)
        return f(*args, **kwargs)
    
    return decorated_function

def admin_token_required(f):
    """Decorator to check if the request has a valid access token and if the user is an admin.
    :param: f: function to be decorated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_payload = _check_access_token(admin_only=True)
        
        if not token_payload["admin"]:
            raise ApiForbidden()
        for name, val in token_payload.items():
            setattr(decorated_function, name, val)
        return f(*args, **kwargs)
    
    return decorated_function

def _check_access_token(admin_only=False):
    """check token validation and user role.
    :param: admin_only: boolean, if True, only admin user can access the resource
    """
    token = request.headers.get("Authorization")
    
    if not token:
        raise ApiUnauthorized(description="Unauthorized", admin_only=admin_only)
    
    result = decode_access_token(token)
    if result.failure:
        raise ApiUnauthorized(
            description=result.error, 
            admin_only=admin_only,
            error="invalid_token", 
            error_description=result.error
        )
    return result.value
    
    
    