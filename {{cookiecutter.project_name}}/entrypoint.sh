#!/bin/sh
echo "Installed packages:"
uv pip list

echo "Starting the application..."
echo "Using port: ${{'{'}}{{cookiecutter.project_name.upper()}}_PORT}"
exec uvicorn $UVICORN_ENTRYPOINT --proxy-headers --forwarded-allow-ips "*" --host 0.0.0.0 --port ${{'{'}}{{cookiecutter.project_name.upper()}}_PORT}
