FROM python:3.11-buster


RUN apt-get update && \
    apt-get install apt-utils \
    openssl \
    g++ \
    gcc \
    libghc-persistent-postgresql-dev -y

RUN pip3 install --upgrade pip