FROM python:3.11.6

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml .
RUN poetry update

COPY . .
