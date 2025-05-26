import os
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env se houver
load_dotenv()

def copy_csv_to_postgres(table_name, csv_path, conn):
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM influencer.{table_name}")
        with open(csv_path, 'r', encoding='utf-8') as f:
            next(f)  # pula o header
            cur.copy_expert(f"COPY influencer.{table_name} FROM STDIN WITH CSV", f)
            print(f"[OK] Inserido: {table_name}")
    conn.commit()

def main():
    conn = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE", "influencer_db"),
        user=os.getenv("PGUSER", "admin"),
        password=os.getenv("PGPASSWORD", "admin"),
        port=os.getenv("PGPORT", 5432)
    )

    base_path = os.path.join(os.path.dirname(__file__), '../data')

    files = {
        'brands': 'brands.csv',
        'creators': 'creators.csv',
        'brand_creator_links': 'brand_creator_links.csv',
        'creator_codes': 'creator_codes.csv',
        'orders': 'orders.csv',
        'order_lines': 'order_lines.csv',
        'commissions': 'commissions.csv',
        'code_logs': 'code_logs.csv'
    }

    for table, file_name in files.items():
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            copy_csv_to_postgres(table, file_path, conn)
        else:
            print(f"[WARN] Arquivo CSV não encontrado para {table}: {file_name}")

    conn.close()

if __name__ == "__main__":
    main()