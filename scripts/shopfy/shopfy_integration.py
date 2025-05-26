import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

API_VERSION = "2023-04"


def fetch_all_orders():
    url = f"{SHOPIFY_STORE}/admin/api/{API_VERSION}/orders.json?status=any&limit=250"
    all_orders = []

    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()["orders"]
        all_orders.extend(data)

        # Pagination
        link_header = response.headers.get("Link")
        if link_header and "rel=\"next\"" in link_header:
            url = link_header.split("<")[1].split(">;")[0]
        else:
            url = None

    return all_orders


def parse_orders_to_df(orders):
    order_rows = []
    order_line_rows = []
    order_line_id = 1

    for o in orders:
        code = o["discount_codes"][0]["code"] if o.get("discount_codes") else None
        brand_id = 11  # mock value; replace with actual logic if needed
        order_total = float(o.get("total_price", 0))
        discount = float(o.get("total_discounts", 0))

        order_rows.append({
            "id": o["order_number"],
            "external_order_id": o.get("id"),
            "date": o.get("created_at", "")[:10],
            "brand_id": brand_id,
            "code": code,
            "order_price": order_total,
            "discount": discount,
            "total_paid": order_total - discount,
            "currency": o.get("currency"),
            "status": o.get("financial_status"),
            "customer_email": o.get("email"),
            "created_at": o.get("created_at"),
            "updated_at": o.get("updated_at")
        })

        for item in o.get("line_items", []):
            order_line_rows.append({
                "id": order_line_id,
                "order_id": o["order_number"],
                "product_id": item.get("product_id"),
                "product_name": item.get("title"),
                "sku": item.get("sku"),
                "quantity": item.get("quantity"),
                "unit_price": float(item.get("price", 0)),
                "created_at": o.get("created_at")
            })
            order_line_id += 1

    return pd.DataFrame(order_rows), pd.DataFrame(order_line_rows)


def main():
    print("Fetching all Shopify orders...")
    orders = fetch_all_orders()
    df_orders, df_lines = parse_orders_to_df(orders)
    df_orders.to_csv("data/shopify_orders.csv", index=False)
    df_lines.to_csv("data/shopify_order_lines_all.csv", index=False)


if __name__ == "__main__":
    main()