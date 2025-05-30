"""Flask CLI/Application entry point."""
import os

from flask_api import create_app, db
from flask_api.models.user import User

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": User}

