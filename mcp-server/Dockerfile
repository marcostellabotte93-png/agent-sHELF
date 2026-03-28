FROM python:3.11-slim

WORKDIR /app

# Installa dipendenze in layer separato per sfruttare la cache
COPY pyproject.toml .
RUN pip install --no-cache-dir \
    "fastmcp>=2.0" \
    "httpx>=0.27" \
    "pydantic-settings>=2.0" \
    "uvicorn[standard]>=0.29"

# Copia sorgente
COPY main.py .
COPY providers/ ./providers/
COPY tools/ ./tools/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
