import os
from flask import Flask, jsonify
from http import HTTPStatus
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

from config import Config, DevelopmentConfig, TestingConfig
from routes import text_routes
from services import Database
from utilities.utility_functions import swagger_ui_setup


def create_app(config_class=Config):
    """
    The entry point for this app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["DATABASE"] = Database(app.config["MONGODB_URI"])

    swagger_ui_blueprint = get_swaggerui_blueprint(
        app.config["SWAGGER_URL"],
        app.config["SWAGGER_UI_LOCATION"],
        config={"app_name": "TextSummarizationApp"},
    )

    app.register_blueprint(text_routes, url_prefix="/text")
    app.register_blueprint(swagger_ui_blueprint, url_prefix=app.config["SWAGGER_URL"])

    @app.errorhandler(404)
    def handle_404(e):
        """
        Handler when user sends a request to a non-existent route
        """
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND

    @app.errorhandler(405)
    def handle_405(e):
        """
        Handler when user sends a request to an endpoint using a non-allowed method
        """
        return jsonify({"error": "Method Not Allowed"}), HTTPStatus.METHOD_NOT_ALLOWED

    return app


if __name__ == "__main__":
    load_dotenv()
    environment = os.getenv("FLASK_ENV", "development")

    config_mapping = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
    }

    config_class = config_mapping.get(environment)
    config_class = config_mapping.get(environment, DevelopmentConfig)

    app = create_app(config_class)
    app.run(host="0.0.0.0", port=5000)
