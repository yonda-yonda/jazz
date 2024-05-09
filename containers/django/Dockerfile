FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /root/workspace
COPY Pipfile Pipfile.lock /root/workspace/
WORKDIR /root/workspace

RUN pip install --upgrade pip pipenv && \
    pipenv install --system

