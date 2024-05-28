FROM python:3.8.19-slim

RUN apt-get update -y && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /todo-list

COPY LICENSE LICENSE
COPY app app
COPY alembic alembic
COPY main.py main.py
COPY insert_todo.py insert_todo.py

ENV PYTHONUNBUFFERED="True"
ENV FLASK_APP=app
CMD flask run --host=0.0.0.0 --port 5050
