FROM python:3.14.3-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv sync --frozen --no-dev

RUN uv run python generate_patients.py

CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
