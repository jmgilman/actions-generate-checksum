FROM python:3.9

COPY entrypoint.sh /entrypoint.sh
COPY checksum.py /checksum.py

ENTRYPOINT ["/entrypoint.sh"]