FROM ubuntu:22.04

WORKDIR /app



RUN apt-get update && apt-get install -y curl ca-certificates

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY .python-version main.py pyproject.toml uv.lock ./

RUN uv sync

COPY src/ src/
COPY tests/ tests/

EXPOSE 8980

CMD ["uv", "run", "python", "-m", "tests.acceptance.test_runner"]
