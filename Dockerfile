FROM debian:bullseye

MAINTAINER Luciano Cauzzi "luciano.cauzzi@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev git

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install virtualenv
RUN python3 -m virtualenv --python=/usr/bin/python3 ./venv
RUN . ./venv/bin/activate
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app/

