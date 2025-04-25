import functools
from flask import request
from flask_api.util.jwt_util import decode_access_token


def _check_access_token(admin_only=False):
    """check token validation and user role.
    :param: admin_only: boolean, if True, only admin user can access the resource
    """
    token = request.headers.get("Authorization")
    
    if not token:
        return False, "Missing access token"
    
    result = decode_access_token(token)
    