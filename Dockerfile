FROM python:3.9

RUN pip install poetry

COPY . /run
RUN cd /run && poetry install

ENTRYPOINT ["/run/entrypoint.sh"]