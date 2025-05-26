import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
TOKEN = os.getenv("SHOPIFY_TOKEN")

headers = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

# response = requests.get(f"{SHOPIFY_STORE}/admin/api/2025-04/orders.json", headers=headers)
# print(response.json())

response = requests.get(f"{SHOPIFY_STORE}/admin/api/2025-04/discount_codes.json", headers=headers)
print(response.json())

