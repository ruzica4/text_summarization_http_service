import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Common configuration for all environments
    """

    DEBUG = False
    TESTING = False
    SWAGGER_UI_LOCATION = os.getenv("SWAGGER_UI_LOCATION")
    SWAGGER_URL = os.getenv("SWAGGER_URL")


class DevelopmentConfig(Config):
    """
    Configuration used for the development environment
    """

    DEBUG = True
    ENV = "development"
    MONGODB_URI = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:{os.getenv('MONGO_PORT', '27017')}/{os.getenv('DEV_DB')}"


class TestingConfig(Config):
    """
    Configuration used for the testing environment
    """

    DEBUG = True
    TESTING = True
    ENV = "testing"
    MONGODB_URI = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:{os.getenv('MONGO_PORT', '27017')}/{os.getenv('TEST_DB')}"
