from flask_restx.inputs import email
from flask_restx import requestparse


auth_request_parser = requestparse.RequestParser(bundle_errors=True)
auth_request_parser.add_argument(name="email", type=email(), required=True, nullable=False)
auth_request_parser.add_argument(name="password", type=str, required=True, nullable=False)