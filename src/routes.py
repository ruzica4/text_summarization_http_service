import logging
from flask import Blueprint, request, jsonify
from http import HTTPStatus
from typing import Dict
from pydantic import BaseModel, Field, ValidationError


from services import store_document_to_db, get_document_summary

# log debug or error lines of code
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

text_routes = Blueprint("text", __name__)


class StoreDocumentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text content to summarize")


class StoreDocumentResponse(BaseModel):
    document_id: str


class GetDocumentResponse(BaseModel):
    document_id: str
    summary: str


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
        try:
            validated_data = StoreDocumentRequest(**data)
        except ValidationError as ve:
            return jsonify({"error": ve.errors()}), HTTPStatus.BAD_REQUEST

        document_id: str = store_document_to_db(data["text"])
        response = StoreDocumentResponse(document_id=document_id)
        return jsonify(response.model_dump()), HTTPStatus.CREATED

    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except RuntimeError as re:
        return jsonify({"error": str(re)}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception:
        logging.error("Unexpected error while storing document")
        return (
            jsonify({"error": "Internal Server Error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@text_routes.route("/get_summary/<string:document_id>", methods=["GET"])
def get_document_summary_route(document_id: str):
    """
    Retrieve the summary of a document from the database using document_id.
    """
    try:
        # if request.content_type != 'application/json':
        #     return jsonify({"error": "Unsupported Content-Type"}), HTTPStatus.BAD_REQUEST

        summary: Dict[str, str] = get_document_summary(document_id)
        response = GetDocumentResponse(**summary)
        return jsonify(response.model_dump()), HTTPStatus.OK

    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except FileNotFoundError:
        return jsonify({"error": "Document not found"}), HTTPStatus.NOT_FOUND
    except KeyError:
        return jsonify({"error": "Document summary not found"}), HTTPStatus.NOT_FOUND
    except RuntimeError as re:
        return jsonify({"error": str(re)}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception:
        logging.error("Unexpected error while retrieving document summary")
        return (
            jsonify({"error": "Internal Server Error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
