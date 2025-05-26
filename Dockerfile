# Dockerfile para FastAPI + PostgreSQL
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /porygon

# Copia os arquivos
COPY . .

# Instala dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Porta exposta
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]