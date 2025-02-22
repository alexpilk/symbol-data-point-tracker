FROM python:3.13.2-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install globally, do not use venv
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR ./app/tracker

RUN uv sync --frozen

# Presuming there is a `my_app` command provided by the project
CMD ["fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]
