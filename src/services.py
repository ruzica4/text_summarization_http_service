from bson.objectid import ObjectId  # type: ignore
import logging

from utilities.utility_functions import db_setup, gridFS_setup
from utilities.nltk_setup import create_summary_from_given_text

# log debug or error lines of cod
logging.basicConfig(
    level=logging.DEBUG,
)


def store_document_to_db(text):
    """
    Save the provided text and its summary to the database.
    """
    db = db_setup()
    gridFS = gridFS_setup(db)

    try:
        # Create a summary for the provided text
        summary = create_summary_from_given_text(text)
        logging.debug(f"Generated summary: {summary}")

        # Data to be stored to the db
        data = {"text": text, "summary": summary}
        document_id = gridFS.put(summary.encode("utf-8"), metadata=data)

        return str(document_id)
    except Exception as e:
        logging.error(f"Error occurred while saving text to the database: {str(e)}")
        raise RuntimeError(f"Error occurred while saving text to the database.")


def get_document_summary(document_id):
    """
    Function that retrieves document summary by providing documet id.
    """
    db = db_setup()
    gridFS = gridFS_setup(db)

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
            raise ValueError("Document not found")

        document = gridFS.get(document_object_id)
        metadata = document.metadata

        if "summary" not in metadata:
            logging.error(
                f"No summary found in metadata for document with id: {document_id}"
            )
            raise ValueError("Document summary not found")

        return {"document_id": str(document_id), "summary": metadata["summary"]}

    except Exception as e:
        logging.error(f"Error occurred while fetching data for document {document_id}")
        raise Exception("Error occurred while fetching data for document")
