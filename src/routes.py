import logging
from flask import Blueprint, request, jsonify
from http import HTTPStatus

from services import store_document_to_db, get_document_summary

text_routes = Blueprint("text", __name__)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


@text_routes.route("/store_document", methods=["POST"])
def store_document_route():
    """
    Route to store the text to the database in the form of a document.
    """
    try:
        if request.content_type != "application/x-www-form-urlencoded":
            return (
                jsonify({"error": "Unsupported Content-Type"}),
                HTTPStatus.BAD_REQUEST,
            )

        data = request.form.to_dict()

        if not data or "text" not in data:
            logging.error('Required field "text" is missing')
            return (
                jsonify({"error": 'Required field "text" is missing'}),
                HTTPStatus.BAD_REQUEST,
            )

        text = data.get("text")
        document_id = store_document_to_db(text)

        return jsonify({"document_id": document_id}), HTTPStatus.CREATED

    except Exception as e:
        logging.error("An error occurred while storing the document")
        return (
            jsonify({"error": "An error occurred while storing the document"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@text_routes.route("/get_summary/<string:document_id>", methods=["GET"])
def get_document_summary_route(document_id):
    """
    Retrieve the summary of a document from the database using document_id.
    """
    try:
        # if request.content_type != 'application/json':
        #     return jsonify({"error": "Unsupported Content-Type"}), HTTPStatus.BAD_REQUEST

        summary = get_document_summary(document_id)
        return jsonify(summary), HTTPStatus.OK

    except ValueError as val_err:
        logging.error("Bad Request")
        return jsonify({"error": "Bad Request"}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        logging.error("Internal server error")
        return (
            jsonify(
                {
                    "error": "An unexpected error occurred while retrieving the document summary"
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
