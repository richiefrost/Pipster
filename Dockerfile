FROM ubuntu:latest

COPY ./src /app
COPY requirements.txt /
COPY config.json /app

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && \
    apt-get install ffmpeg python3-pip python3 -y && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python3", "/app/api.py"]
