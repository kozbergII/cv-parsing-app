from io import BytesIO

from flask import Flask, request, jsonify, send_file, render_template
from pymongo.errors import PyMongoError

from parser import extract_cv_data
from database import *


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# Dashboard
@app.get("/")
def home():
    return render_template("index.html")


# Upload a CV
@app.post("/api/applicants")
def upload_cv():
    file = request.files.get("file")

    if not file or not file.filename:
        return jsonify({"error": "No file uploaded"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    pdf_bytes = file.read()
    data = extract_cv_data(pdf_bytes)

    applicant_id = save_applicant(data, pdf_bytes, file.filename)

    data.pop("rawData")

    return jsonify({"id": applicant_id, **data}), 201


# Get all applicants
@app.get("/api/applicants")
def list_applicants():
    return jsonify(get_applicants())


# Download an applicant's CV
@app.get("/api/applicants/<applicant_id>/pdf")
def download_cv(applicant_id):
    applicant = get_applicant(applicant_id)

    if applicant is None:
        return jsonify({"error": "Applicant not found"}), 404

    return send_file(
        BytesIO(applicant["pdfData"]),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=applicant["fileName"]
    )


# Delete an applicant and their PDF
@app.delete("/api/applicants/<applicant_id>")
def remove_applicant(applicant_id):
    if not delete_applicant(applicant_id):
        return jsonify({"error": "Applicant not found"}), 404

    return "", 204


# Liveness check
@app.get("/healthz")
def health():
    return jsonify({"status": "alive"}), 200


# Database readiness check
@app.get("/readyz")
def ready():
    try:
        database_ready()
        return jsonify({"status": "ready"})
    except PyMongoError:
        return jsonify({"status": "unavailable"}), 503


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({"error": "Upload too large"}), 413
