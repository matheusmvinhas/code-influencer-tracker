import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

NUVEMSHOP_STORE = os.getenv("NUVEMSHOP_STORE")
NUVEMSHOP_TOKEN = os.getenv("NUVEMSHOP_TOKEN")

HEADERS  = {
        "Authentication": f"bearer {NUVEMSHOP_TOKEN}",
        "Content-Type": "application/json"
  }

def get_table_X(store_id, table_X):
    """
    Traz dados da tabela X da loja de ID store_id
    Args:
        store_id (str): ID da loja
        table_X (str): Nome da tabela X
    Returns:
        response: Resposta da API
    """

    url = f"https://api.nuvemshop.com.br/v1/{store_id}/{table_X}"

    # headers = {
    #     "Authentication": f"bearer {access_token}",
    #     "Content-Type": "application/json"
    # }

    response = requests.get(url, headers=HEADERS)

    return response

def response_to_df(response, fields_target=None):
    """
    Converte a resposta da API em um DataFrame do Pandas para as colunas no segundo argumento
    Args:
        response: Resposta da API
        fields_target: Lista de colunas que deseja ter
    Returns:
        df: DataFrame com os dados da tabela X
    """
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df_filt = df[fields_target] if fields_target else df
        return df_filt
    else:
        raise Exception(f"Erro ao obter dados: {response.status_code} - {response.text}")
    

def main():
    brand_id = 14

    ##Orders
    fields_target = [
                "id",
                "id",
                "created_at",
                #"brand_id",
                "coupon",
                "subtotal",
                "discount",
                "total",
                "currency",
                "status",
                "contact_email",
                "created_at",
                "updated_at" 
                ]
    
    orders = get_table_X(NUVEMSHOP_STORE, NUVEMSHOP_TOKEN, "orders")
    df_orders = response_to_df(orders, fields_target=fields_target)

    #Renomeia as colunas
    df_orders.columns = [
                    "id",
                    "external_order_id",
                    "date",
                    # "brand_id",
                    "code",
                    "order_price",
                    "discount",
                    "total_paid",
                    "currency",
                    "status",
                    "customer_email",
                    "created_at",
                    "updated_at",
                    ]

    #Ajust created_at
    df_orders["date"] = df_orders["created_at"].str[:10]

    #Adição da coluna brand_id
    df_orders.insert(loc=3, column="brand_id", value=brand_id) 

    df_orders.to_csv("data/nuvemshop_orders.csv", index=False)

if __name__ == "__main__":
    main()