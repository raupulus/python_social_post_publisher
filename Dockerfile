# Uso Python 3.13 como imagen base
FROM python:3.13-slim

# Establezco el directorio de trabajo
WORKDIR /app

# Establezco las variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Instalo las dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    libpng-dev \
    libffi-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copio el archivo de requisitos
COPY requirements.txt .

# Instalo las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copio solo app y docs (no data)
COPY app/ ./app/
COPY docs/ ./docs/

# Creo un usuario no root para ejecutar la aplicación
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expongo el puerto para Flask
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app/app.py"]