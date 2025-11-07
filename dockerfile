FROM python:3.12-slim

# Evitar bytecode y buffering raro en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema mínimas (opcional, aquí muy poco)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiamos solo lo necesario para instalar el paquete
COPY pyproject.toml ./

# Instalar deps (solo runtime, no hace falta dev en imagen final)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# Copiar el código
COPY app ./app

# Puerto interno
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]