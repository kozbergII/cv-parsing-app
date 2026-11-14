# CV Parsing App

This app lets you upload a CV PDF, extracts useful applicant details, and saves them in MongoDB.

You can view applicants in the dashboard, download their original CV, and delete them when needed.

## What you need

- Docker
- Docker Compose

## First setup

Create a file named `.env` in the project folder:

```env
PORT=8000
MONGO_USER=admin
MONGO_PASSWORD=choose-a-strong-password
MONGO_URI=mongodb://${MONGO_USER}:${MONGO_PASSWORD}@mongo:27017/cv_parser?authSource=admin
```

Do not commit `.env` to Git because it contains your database password.

## Start the app

From the project folder, run:

```bash
docker compose up --build
```

Or run the simple deployment script:

```bash
bash deploy.sh
```

Open the dashboard in your browser:

```text
http://localhost:8000
```

## Stop the app

```bash
docker compose down
```

This stops the containers but keeps the saved applicant data.

To stop the app and permanently delete all applicant data:

```bash
docker compose down -v
```

## Features

- Upload PDF CV files
- Extract personal ID, first name, family name, email, LinkedIn URL, and mobile number
- Store the extracted data, full PDF text, and original PDF in MongoDB
- View applicants in a dashboard
- Download an original CV PDF
- Delete an applicant and their PDF

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/applicants` | Upload a CV as a `file` form field |
| `GET` | `/api/applicants` | Get all applicants |
| `GET` | `/api/applicants/{id}/pdf` | Download an applicant CV |
| `DELETE` | `/api/applicants/{id}` | Delete an applicant |
| `GET` | `/healthz` | Check whether the app is running |
| `GET` | `/readyz` | Check whether the app can reach MongoDB |

## How it runs

Docker Compose starts two services:

- `app`: the Flask application, served by Gunicorn
- `mongo`: the MongoDB database

MongoDB data is stored in a Docker volume, so it remains available after the containers stop and start again.
