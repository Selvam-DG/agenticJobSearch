
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /service
ENV JOBSCOUT_ROOT=/service
COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir . \
    && useradd \
        --create-home \
        --uid 10001 \
        appuser

COPY alembic.ini ./
COPY alembic ./alembic

COPY templates ./templates
COPY static ./static

USER appuser

EXPOSE 8084

HEALTHCHECK \
  --interval=30s \
  --timeout=5s \
  --start-period=15s \
  --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://0.0.0.0:8084/health/live', timeout=3)" || exit 1

CMD ["uvicorn", "jobscout.main:app", "--host", "0.0.0.0", "--port", "8084"]