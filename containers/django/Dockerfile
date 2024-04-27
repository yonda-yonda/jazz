FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /root/workspace
COPY requirements.txt /root/workspace/
WORKDIR /root/workspace

RUN pip install --upgrade pip\
    && pip install -r requirements.txt
