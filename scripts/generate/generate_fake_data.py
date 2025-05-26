# scripts/generate_fake_data.py
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os
import logging

# Configura logger
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

fake = Faker("pt_BR")
Faker.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
os.makedirs(DATA_DIR, exist_ok=True)

def generate_brands(n=10):
    logger.info("Gerando brands.csv")
    return pd.DataFrame([{
        "id": i,
        "name": fake.company(),
        "cnpj": fake.cnpj(),
        "contact_email": fake.company_email(),
        "website": fake.url(),
        "instagram_handle": "@" + fake.user_name(),
        "created_at": fake.date_time_this_year(),
        "updated_at": fake.date_time_this_year()
    } for i in range(1, n + 1)])

def generate_creators(n=10):
    logger.info("Gerando creators.csv")
    return pd.DataFrame([{
        "id": i,
        "cpf": fake.cpf(),
        "username": fake.user_name(),
        "email": fake.email(),
        "instagram_handle": "@" + fake.user_name(),
        "role": random.choice(["influencer", "affiliate"]),
        "bio": fake.text(max_nb_chars=150),
        "created_at": fake.date_time_this_year(),
        "updated_at": fake.date_time_this_year()
    } for i in range(1, n + 1)])

def generate_brand_creator_links(creators_df, brands_df):
    logger.info("Gerando brand_creator_links.csv")
    rows = []
    contagem = 1
    for i in range(1, len(creators_df) + 1):
        for j in range(1, len(brands_df) + 1):
            rows.append({
                "id": contagem,
                "creator_id": creators_df["id"].iloc[i - 1],
                "brand_id": brands_df["id"].iloc[j - 1],
                "partnership_type": random.choice(["affiliate", "ambassador"]),
                "status": random.choice(["active", "inactive", "pending"]),
                "created_at": fake.date_time_this_year(),
                "updated_at": fake.date_time_this_year()
            })
            contagem += 1
    return pd.DataFrame(rows)

def generate_creator_codes(brand_creator_links_df):
    logger.info("Gerando creator_codes.csv")
    rows = []
    for i, row in brand_creator_links_df.iterrows():
        rows.append({
            "id": i,
            "creator_id": row["creator_id"],
            "brand_id": row["brand_id"],
            "code": fake.unique.lexify(text='????10'),
            "discount": round(random.uniform(5, 20), 2),
            "commission": round(random.uniform(1, 10), 2),
            "is_percentage": random.choice([True, False]),
            "usage_limit": random.randint(10, 100),
            "times_used": random.randint(0, 50),
            "status": random.choice(["active", "inactive"]),
            "started_at": fake.date_time_this_year(),
            "disabled_at": fake.date_time_this_year(),
            "created_at": fake.date_time_this_year(),
            "updated_at": fake.date_time_this_year()
        })
    return pd.DataFrame(rows)

def generate_orders(codes_df, n=1000):
    logger.info("Gerando orders.csv")

    # Correção de tipos para evitar erros
    codes_df = codes_df.copy()
    codes_df["discount"] = pd.to_numeric(codes_df["discount"], errors="coerce").fillna(0.0)
    codes_df["is_percentage"] = codes_df["is_percentage"].astype(str).str.lower().isin(["true", "1"])

    rows = []
    for i in range(1, n + 1):
        has_code = random.random() < 0.8
        price = float(round(random.uniform(50, 500), 2))

        if has_code and not codes_df.empty:
            code_row = codes_df.sample().iloc[0]
            brand_id = int(code_row["brand_id"])
            code = code_row["code"]
            try:
                discount_raw = float(code_row["discount"])
            except (ValueError, TypeError):
                logger.warning(f"Valor inválido de discount: {code_row['discount']}, assumindo 0")
                discount_raw = 0.0

            discount = (
                round(price * (discount_raw / 100), 2)
                if bool(code_row["is_percentage"])
                else discount_raw
            )
        else:
            brand_id = random.randint(1, 10)
            code = None
            discount = 0.0

        total_paid = price - discount

        rows.append({
            "id": i,
            "external_order_id": fake.uuid4(),
            "date": fake.date_this_year(),
            "brand_id": brand_id,
            "code": code,
            "order_price": price,
            "discount": discount,
            "total_paid": total_paid,
            "currency": "BRL",
            "status": random.choice(["paid", "refunded", "canceled"]),
            "customer_email": fake.email(),
            "created_at": fake.date_time_this_year(),
            "updated_at": fake.date_time_this_year()
        })
    return pd.DataFrame(rows)

# def generate_orders(codes_df, n=100):
#     logger.info("Gerando orders.csv")
#     rows = []
#     for i in range(1, n + 1):
#         code_row = codes_df.sample().iloc[0]
#         price = round(random.uniform(50, 500), 2)
#         discount = round(price * (code_row["discount"] / 100), 2) if code_row["is_percentage"] else code_row["discount"]
#         rows.append({
#             "id": i,
#             "external_order_id": fake.uuid4(),
#             "date": fake.date_this_year(),
#             "brand_id": code_row["brand_id"],
#             "code": code_row["code"],
#             "order_price": price,
#             "discount": discount,
#             "total_paid": price - discount,
#             "currency": "BRL",
#             "status": random.choice(["paid", "refunded", "canceled"]),
#             "customer_email": fake.email(),
#             "created_at": fake.date_time_this_year(),
#             "updated_at": fake.date_time_this_year()
#         })
#     return pd.DataFrame(rows)

def generate_order_lines(orders_df, n=3000):
    logger.info("Gerando order_lines.csv")
    rows = []
    for i in range(1, n + 1):
        order = orders_df.sample().iloc[0]
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(10, 150), 2)
        rows.append({
            "id": i,
            "order_id": order["id"],
            "product_id": str(fake.ean13()),
            "product_name": fake.word(),
            "sku": fake.bothify(text='SKU-####'),
            "quantity": quantity,
            "unit_price": unit_price,
            "created_at": fake.date_time_this_year()
        })
    return pd.DataFrame(rows)

def generate_commissions(codes_df, orders_df):
    logger.info("Gerando commissions.csv")
    rows = []
    i = 1
    for _, order in orders_df.iterrows():
        if pd.notnull(order["code"]):
            code_row_df = codes_df[codes_df["code"] == order["code"]]
            if not code_row_df.empty:
                code_row = code_row_df.iloc[0]
                try:
                    commission_raw = float(code_row["commission"])
                except (ValueError, TypeError):
                    logger.warning(f"Valor inválido de commission: {code_row['commission']}, assumindo 0")
                    commission_raw = 0.0

                commission_value = (
                    round(order["order_price"] * (commission_raw / 100), 2)
                    if code_row["is_percentage"]
                    else commission_raw
                )

                rows.append({
                    "id": i,
                    "creator_id": code_row["creator_id"],
                    "order_id": order["id"],
                    "code_id": code_row["id"],
                    "commission_value": commission_value,
                    "status": random.choice(["pending", "paid", "reversed"]),
                    "paid_at": fake.date_time_this_year(),
                    "created_at": fake.date_time_this_year()
                })
                i += 1
    return pd.DataFrame(rows)

def generate_code_logs(codes_df, n=150):
    logger.info("Gerando code_logs.csv")
    rows = []
    for i in range(1, n + 1):
        code = codes_df.sample().iloc[0]
        rows.append({
            "id": i,
            "code_id": code["id"],
            "event": random.choice(["used", "created", "updated", "disabled"]),
            "metadata": "{}",
            "created_at": fake.date_time_this_year()
        })
    return pd.DataFrame(rows)

def main():
    logger.info("Iniciando geração de dados fake...")
    brands = generate_brands()
    creators = generate_creators()
    brand_creator_links = generate_brand_creator_links(creators, brands)
    codes = generate_creator_codes(brand_creator_links)
    orders = generate_orders(codes)
    order_lines = generate_order_lines(orders)
    commissions = generate_commissions(codes, orders)
    code_logs = generate_code_logs(codes)

    logger.info("Salvando CSVs...")
    brands.to_csv(f"{DATA_DIR}/brands.csv", index=False)
    creators.to_csv(f"{DATA_DIR}/creators.csv", index=False)
    brand_creator_links.to_csv(f"{DATA_DIR}/brand_creator_links.csv", index=False)
    codes.to_csv(f"{DATA_DIR}/creator_codes.csv", index=False)
    orders.to_csv(f"{DATA_DIR}/orders.csv", index=False)
    order_lines.to_csv(f"{DATA_DIR}/order_lines.csv", index=False)
    commissions.to_csv(f"{DATA_DIR}/commissions.csv", index=False)
    code_logs.to_csv(f"{DATA_DIR}/code_logs.csv", index=False)

    print("[OK] Dados fake gerados para todas as tabelas em /data")

if __name__ == "__main__":
    main()