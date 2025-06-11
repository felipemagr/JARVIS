FROM python:3.11-slim

ARG GENAI_ENVIRONMENT

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GENAI_ENVIRONMENT=${GENAI_ENVIRONMENT:-local} \
    APP_DIR=/app \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_WARNINGS_EXPORT=false \
    POETRY_VERSION=1.8.5 \
    POETRY_NO_INTERACTION=1

WORKDIR ${APP_DIR}

ENV PYTHONPATH=/app/src

COPY ./pyproject.toml ./poetry.lock ${APP_DIR}/
COPY ./src ${APP_DIR}/src

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry config virtualenvs.create false && \
    poetry install --without dev

CMD ["uvicorn", "jarvis.app.main:app", "--host", "0.0.0.0", "--port", "8000"]