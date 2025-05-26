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


def fetch_orders_with_discounts():
    url = f"{SHOPIFY_STORE}/admin/api/{API_VERSION}/orders.json?status=any&limit=250"
    all_orders = []

    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()["orders"]

        # Filter only orders with discount codes
        orders_with_discount = [o for o in data if o.get("discount_codes")]
        all_orders.extend(orders_with_discount)

        # Pagination
        link_header = response.headers.get("Link")
        if link_header and "rel=\"next\"" in link_header:
            url = link_header.split("<")[1].split(">;")[0]
        else:
            url = None

    return all_orders


def parse_orders_to_df(orders):
    rows = []
    for o in orders:
        code = o["discount_codes"][0]["code"] if o.get("discount_codes") else None
        rows.append({
            "order_id": o["id"],
            "code": code,
            "email": o.get("email"),
            "total_price": float(o["total_price"]),
            "currency": o.get("currency"),
            "created_at": o.get("created_at")
        })
    return pd.DataFrame(rows)


def main():
    print("Fetching Shopify orders...")
    orders = fetch_orders_with_discounts()
    df = parse_orders_to_df(orders)
    df.to_csv("data/shopify_orders_with_coupons.csv", index=False)
    print(f"Saved {len(df)} orders with discount codes to CSV.")


if __name__ == "__main__":
    main()

