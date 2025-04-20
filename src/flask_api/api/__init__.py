from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_blueprint,
    version="1.0",
    title="Flask API",
    description="Flask API with JWT authentication",
    doc="/docs",
    authorizations=authorizations,
)
