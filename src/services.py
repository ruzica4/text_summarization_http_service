from bson.objectid import ObjectId  # type: ignore
import logging
from pymongo import MongoClient
from gridfs import GridFS
from flask import current_app
from typing import Dict, Any

from utilities.nltk_setup import create_summary_from_given_text

# log debug or error lines of code
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Database:
    def __init__(self, uri: str):
        self.client = MongoClient(uri, maxPoolSize=10, minPoolSize=2)
        self.db_name = uri.split("/")[-1]
        self.db = self.client[self.db_name]
        self.gridfs = GridFS(self.db)

    def get_db(self):
        return self.db

    def get_gridfs(self):
        return self.gridfs


def get_database() -> Database:
    return current_app.config["DATABASE"]


def store_document_to_db(text: str) -> str:
    """
    Save the provided text and its summary to the database.
    """
    db = get_database()
    gridFS = db.get_gridfs()

    try:
        # Create a summary for the provided text
        summary: str = create_summary_from_given_text(text)
        logging.debug(f"Generated summary: {summary}")

        # Data to be stored to the db
        data: Dict[str, Any] = {"text": text, "summary": summary}
        with gridFS.new_file(metadata=data) as document:
            document.write(summary.encode("utf-8"))
            document_id: str = str(document._id)

        return document_id
    except ValueError as ve:
        logging.error(f"Validation error: {str(ve)}")
        raise
    except ConnectionError as ce:
        logging.error(f"Database connection error: {str(ce)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while saving text to the database: {str(e)}")
        raise RuntimeError("Internal Server Error")


def get_document_summary(document_id: str) -> Dict[str, str]:
    """
    Function that retrieves document summary by providing documet id.
    """
    db = get_database()
    gridFS = db.get_gridfs()

    # User will  provide document_id and we will check whether the document id
    # is of good type(containing only numbers and having certain length)
    if not ObjectId.is_valid(document_id):
        logging.error(f"Invalid document ID format: {document_id}")
        raise ValueError("Invalid document ID format")

    # We will transform it to a proper format and try and fetch the document from MongoDb
    document_object_id = ObjectId(document_id)

    try:
        if not gridFS.exists(document_object_id):
            logging.error(
                f"Document not found after attepting to retrieve it: {document_id}"
            )
            raise FileNotFoundError("Document not found")

        document = gridFS.get(document_object_id)
        metadata = document.metadata

        if "summary" not in metadata:
            logging.error(
                f"No summary found in metadata for document with id: {document_id}"
            )
            raise KeyError("Document summary not found")

        return {"document_id": str(document_id), "summary": metadata["summary"]}

    except FileNotFoundError:
        raise
    except KeyError:
        raise
    except Exception as e:
        logging.error(f"Unexpected error fetching document {document_id}: {str(e)}")
        raise RuntimeError("Internal Server Error")
