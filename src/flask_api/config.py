"""Config settings for for development, testing and production environments."""
import os
from pathlib import Path


HERE = Path(__file__).parent
POSTGRES_DEV = 'postgresql://postgres:111002@localhost:5433/test_api_db'



class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "open sesame")
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(Config):
    """Development configuration."""

    TOKEN_EXPIRE_MINUTES = 15
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", POSTGRES_DEV)


class ProductionConfig(Config):
    """Production configuration."""

    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", '')
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
