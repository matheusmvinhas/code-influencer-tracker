import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)
DB_NAME = os.getenv("POSTGRES_DB", "influencer_db")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "admin")

ORDER_CSV = "data/shopify_orders.csv"
ORDER_LINE_CSV = "data/shopify_order_lines_all.csv"


def copy_csv_to_table(file_path, table_name, conn):
    with conn.cursor() as cur, open(file_path, "r") as f:
        next(f)  # skip header
        try:
            cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV", f)
        except psycopg2.errors.UniqueViolation as e:
            print(f"Erro de chave duplicada ao inserir em {table_name}: {e}")
            conn.rollback()
            return
        conn.commit()


def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

    print("Ingesting shopify_orders_all.csv into influencer.orders...")
    copy_csv_to_table(ORDER_CSV, "influencer.orders", conn)

    print("Ingesting shopify_order_lines_all.csv into influencer.order_lines...")
    copy_csv_to_table(ORDER_LINE_CSV, "influencer.order_lines", conn)

    conn.close()
    print("Ingest complete.")


if __name__ == "__main__":
    main()
