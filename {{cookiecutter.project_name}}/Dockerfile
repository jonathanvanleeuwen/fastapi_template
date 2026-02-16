FROM python:3.12-slim

ENV APP_NAME="{{cookiecutter.project_name}}"
ENV UVICORN_ENTRYPOINT="src.{{cookiecutter.project_name}}.main:app"

EXPOSE ${{'{'}}{{cookiecutter.project_name.upper()}}_PORT}

# Copy dependency files
COPY src /opt/app-root/src
COPY pyproject.toml /opt/app-root/
COPY uv.lock .
COPY entrypoint.sh /entrypoint.sh

# Install Git (required for uv to install lib_auth from GitHub)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv
RUN uv venv .venv

ENV PATH=".venv/bin:$PATH"

WORKDIR /opt/app-root/
RUN uv sync --inexact

ENTRYPOINT ["/entrypoint.sh"]

# docker build -t {{cookiecutter.project_name}}:latest .
