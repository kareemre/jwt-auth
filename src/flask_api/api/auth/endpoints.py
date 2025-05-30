from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api.api.auth.dto import auth_request_parser
from flask_api.api.auth.business import (
    process_registration_request,
    process_login_request,
)

auth_ns = Namespace("auth", validate=True)

@auth_ns.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/register."""

    @auth_ns.expect(auth_request_parser)
    @auth_ns.response(int(HTTPStatus.CREATED), "New user was successfully created.")
    @auth_ns.response(int(HTTPStatus.CONFLICT), "Email address is already registered.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Register a new user and return an access token."""
        request_data = auth_request_parser.parse_args()
        email = request_data.get("email")
        password = request_data.get("password")
        return process_registration_request(email, password)
    
@auth_ns.route("/login", endpoint="auth_login")
class LoginUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/login."""

    @auth_ns.expect(auth_request_parser)
    @auth_ns.response(int(HTTPStatus.OK), "User successfully logged in.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Email or password does not match.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Login a user and return an access token."""
        request_data = auth_request_parser.parse_args()
        email = request_data.get("email")
        password = request_data.get("password")
        return process_login_request(email, password)