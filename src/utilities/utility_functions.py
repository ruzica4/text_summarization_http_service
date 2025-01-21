from flask import current_app
from gridfs import GridFS
from pymongo import MongoClient
from flask_swagger_ui import get_swaggerui_blueprint


def db_setup():
    """
    Function that manages and sets up the database connection
    """
    mongodb_uri = current_app.config["MONGODB_URI"]
    mongo_client = MongoClient(mongodb_uri)
    db_name = mongodb_uri.split("/")[-1]

    return mongo_client[db_name]


def gridFS_setup(db):
    """
    Function that sets up GridFS
    """
    return GridFS(db)


def swagger_ui_setup(app):
    """
    Function that sets up the Swagger UI blueprint
    """
    swagger_url = app.config["SWAGGER_URL"]
    api_url = app.config["SWAGGER_UI_LOCATION"]

    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url, api_url, config={"app_name": "TextSummarizationApp"}
    )
    return swaggerui_blueprint
