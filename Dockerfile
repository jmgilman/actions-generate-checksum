FROM python:3.12-slim-bookworm

ARG POETRY_VERSION=1.7.1

ENV POETRY_HOME=/tmp/poetry
ENV PATH=$POETRY_HOME/bin:$PATH

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

WORKDIR /run

COPY . .
RUN poetry install --only main --no-root

ENTRYPOINT ["/run/entrypoint.sh"]