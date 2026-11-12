import os

from bson import Binary, ObjectId
from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient(
    os.environ["MONGO_URI"],
    serverSelectionTimeoutMS=3000
)

db = client["cv_parser"]
collection = db["applicants"]


def save_applicant(data, pdf_bytes, filename):
    document = {
        **data,
        "fileName": filename,
        "pdfData": Binary(pdf_bytes)
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_applicants():
    applicants = collection.find(
        {},
        {"pdfData": 0, "rawData": 0}
    )

    result = []
    for applicant in applicants:
        applicant["_id"] = str(applicant["_id"])
        result.append(applicant)

    return result


def get_applicant(applicant_id):
    if not ObjectId.is_valid(applicant_id):
        return None

    return collection.find_one({
        "_id": ObjectId(applicant_id)
    })


def delete_applicant(applicant_id):
    if not ObjectId.is_valid(applicant_id):
        return False

    result = collection.delete_one({
        "_id": ObjectId(applicant_id)
    })

    return result.deleted_count > 0


def database_ready():
    client.admin.command("ping")
