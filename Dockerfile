# syntax=docker/dockerfile:1

FROM python:3.9.2

WORKDIR python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["uwsgi", "--http", "127.0.0.1:8000", "--master", "-p", "4", "-w", "wsgi:app"]