FROM python:3.9-slim-bullseye

RUN pip install poetry

COPY . /run
RUN cd /run && poetry install

ENTRYPOINT ["/run/entrypoint.sh"]