# --- Stage 1: Build dependencies ---
FROM python:3.10-slim-buster as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    binutils \
    libproj-dev \
    gdal-bin \
    python3-gdal \
    libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
WORKDIR /app
RUN python -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# --- Stage 2: Run application ---
FROM python:3.10-slim-buster as application

WORKDIR /app

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy installed python dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Install GDAL and other necessary system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL library path
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# Copy entrypoint and start scripts
COPY ./compose/production/django/entrypoint /entrypoint
COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /entrypoint /start \
  && chmod +x /entrypoint /start

# Copy the Django application from the context
COPY . .

# Use the start script as the entrypoint
ENTRYPOINT ["/entrypoint"]
