# Container for validating the Movie Mode blueprint with Home Assistant's config checker
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install build deps required by Home Assistant wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        libjpeg-dev \
        zlib1g-dev \
        libturbojpeg0-dev \
        libxml2-dev \
        libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
# Install dependencies required by validator and Home Assistant CLI
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt homeassistant==2024.6.3

COPY . .

# Default command validates the included blueprint and runs hass --script check_config
CMD ["python", "validator.py", "movie-mode.yaml", "--run-check-config"]
