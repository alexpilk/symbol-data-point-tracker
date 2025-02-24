FROM python:3.13.2-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install globally, do not use venv
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

ADD . /app

WORKDIR ./app

RUN uv sync --frozen

CMD ["fastapi", "run", "tracker/api", "--port", "80", "--host", "0.0.0.0"]
