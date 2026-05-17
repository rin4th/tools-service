# syntax=docker/dockerfile:1.7
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /storage \
    && chown -R appuser:appuser /storage

COPY . ./worker

USER appuser

CMD ["python", "-m", "worker.main"]
