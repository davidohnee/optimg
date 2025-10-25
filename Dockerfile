FROM python:3.13-alpine

RUN pip install --no-cache-dir optimg

ENTRYPOINT [ "optimg", "-i", "/in", "-o", "/out" ]
