FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app ./app

RUN apt-get update && apt-get install -y --no-install-recommends curl

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "app.routes:app"]