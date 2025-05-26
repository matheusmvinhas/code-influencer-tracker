# Use a imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY nuvemshop_integration.py .
COPY .env .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Cria o diretório para os dados
RUN mkdir -p /app/data

# Comando para executar o script
CMD ["python", "./nuvemshop_integration.py"]