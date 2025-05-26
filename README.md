# 📊 Porygon — Influencer Marketing Tracker

Este projeto conecta marcas e influenciadores, rastreando vendas feitas com cupons personalizados.

## ✅ Pré-requisitos

Antes de começar, certifique-se de que você tem instalado:

### 🔧 Ferramentas obrigatórias:

| Ferramenta | Versão Recomendada | Descrição |
|-----------|--------------------|-----------|
| [Docker](https://www.docker.com/products/docker-desktop/) | 20+ | Para rodar o PostgreSQL e Metabase |
| [Docker Compose](https://docs.docker.com/compose/) | 1.29+ | Para orquestrar os serviços |
| [Conda (Miniconda ou Anaconda)](https://docs.conda.io/en/latest/miniconda.html) | 4.10+ | Gerenciar o ambiente Python local |
| `make` | (nativo em Mac/Linux) | Automatiza comandos úteis |

### 💡 Alternativas:
- Se estiver no Windows sem WSL, recomenda-se usar [WSL2 + Ubuntu](https://learn.microsoft.com/pt-br/windows/wsl/install).


## 🔧 Stack
- PostgreSQL para armazenamento dos dados
- Metabase para visualização
- Docker para orquestração
- Python (pandas + psycopg2) para ingestão de dados

## 🚀 Como rodar localmente

```bash
# 1. Clone o projeto
git clone https://github.com/sua-conta/code-influencer-tracker.git

# 2. Ative o ambiente Conda e ingira os dados
conda env create -f environment.yml
conda activate influencer_env

# 3. Crie seu .env com base no exemplo
cp .env.example .env

# 4. Suba o ambiente
docker-compose up -d
OU
make up

# 5. Recria o Volume do Metabase
docker exec -i code-influencer-tracker-postgres-1 psql -U admin -d influencer_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker exec -i code-influencer-tracker-postgres-1 psql -U admin -d influencer_db < metabase_pg_backup.sql

OU 

make restore-db-clean

# (optional) 6. Use o Makefile
make generate
make ingest
make reload

```

## 📈 Acessar o Metabase

Abra [http://localhost:3000](http://localhost:3000) e siga o setup inicial. Use:

- Host: `postgres`
- DB: `influencer_db`
- User: `admin` / `admin`
- port: `5432`
- schema: `influencer`

## DataBase ERD

[ERD](https://dbdiagram.io/d/680814e41ca52373f5f371e2)

## 📂 Estrutura de Diretórios
```
├── data/               # Arquivos CSV (não versionados)
├── initdb/             # SQL de schema do banco
├── scripts/            # Scripts Python
├── .env.example        # Exemplo de config
├── docker-compose.yml  # Stack
├── environment.yml     # Conda env
├── Makefile            # Comandos úteis
└── README.md
```
## 🗃️ Exportar e importar dados do Metabase

### 🔄 Exportar o volume `metabase_data` para compartilhamento:

```bash
docker exec -t code-influencer-tracker-postgres-1 pg_dump -U admin influencer_db > metabase_pg_backup.sql
```

### 📥 Importar o volume em outro ambiente:

```bash
docker exec -i code-influencer-tracker-postgres-1 psql -U admin -d influencer_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker exec -i code-influencer-tracker-postgres-1 psql -U admin -d influencer_db < metabase_pg_backup.sql
```

## 🛠️ Comandos do Makefile

| Comando              | Ação                                                                 |
|----------------------|----------------------------------------------------------------------|
| `make up`            | Sobe o ambiente com Docker Compose                                   |
| `make down`          | Derruba os containers                                                |
| `make generate`      | Gera dados fictícios com Faker                                       |
| `make ingest`        | Faz ingestão dos arquivos `.csv` no PostgreSQL                      |
| `make reload`        | Executa `generate` + `ingest` em sequência                          |
| `make backup-db` | Isso gera um arquivo `metabase_pg_backup.sql` com todas as configurações, perguntas, dashboards, conexões etc |
| `make restore-db-clean` | Limpa o banco atual e restaura a partir do arquivo `metabase_pg_backup.sql` |
| `make reset`         | Derruba tudo (`down -v`), remove volumes e sobe o ambiente limpo     |
| `make ingest-shopify`     | Faz append dos pedidos da Shopify nas tabelas orders e order_lines |


## API

Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

## Exemplo de uso com `curl`

### GET `/brands`

```bash
curl http://localhost:8000/brands
```

### POST `/brands`

```bash
curl -X POST http://localhost:8000/brands \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Marca X",
        "cnpj": "12345678000100",
        "contact_email": "contato@marcax.com",
        "website": "https://marcax.com",
        "instagram_handle": "@marcax"
    }'
```
