FROM python:3.12-slim

# Avoid bytecode and weird logging buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal system dependencies (optional, here very little)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary to install the package
COPY pyproject.toml ./

# Install deps (only runtime, no need for dev in final image)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# Copy the code
COPY app ./app

# Internal port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]