up:
	docker-compose up -d

down:
	docker-compose down

ingest:
	conda run -n influencer_env python scripts/ingest/ingest_csv.py

generate:
	conda run -n influencer_env python scripts/generate/generate_fake_data.py

reload:
	make generate && make ingest

backup-db:
	docker exec -t porygon-postgres-1 pg_dump -U admin influencer_db > metabase_pg_backup.sql

restore-db-clean:
	docker exec -i porygon-postgres-1 psql -U admin -d influencer_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	docker exec -i porygon-postgres-1 psql -U admin -d influencer_db < metabase_pg_backup.sql

reset:
	docker-compose down -v
	docker volume rm pg_data || true
	docker-compose up -d

ingest-shopify:
	conda run -n influencer_env python scripts/ingest/ingest_shopfy_orders.py

run-api:
	uvicorn api.main:app --reload