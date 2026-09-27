import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUTPUT_DIR = Path("data_landing")
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Définir un catalogue produit fixe pour assurer la cohérence
PRODUCTS = [
    {"product_id": "PROD-001", "title": "Wireless Noise-Canceling Headphones", "sku": "TECH-WNC-01", "cost": 45.00, "base_price": 120.00},
    {"product_id": "PROD-002", "title": "Ergonomic Mechanical Keyboard", "sku": "TECH-EMK-02", "cost": 35.00, "base_price": 95.00},
    {"product_id": "PROD-003", "title": "Ultra-Wide Gaming Monitor 34\"", "sku": "TECH-UWM-03", "cost": 210.00, "base_price": 450.00},
    {"product_id": "PROD-004", "title": "Smart Fitness Watch V2", "sku": "WEAR-SFW-04", "cost": 28.00, "base_price": 79.99},
    {"product_id": "PROD-005", "title": "USB-C Multi-Port Hub", "sku": "ACC-UCH-05", "cost": 9.50, "base_price": 29.99},
]

# 2. Générer un pool de clients réguliers pour simuler la rétention / LTV
CUSTOMERS = []
for _ in range(120):
    CUSTOMERS.append({
        "customer_id": f"CUST-{uuid.uuid4().hex[:8].upper()}",
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "city": fake.city(),
        "country": "Morocco"
    })

def generate_shopify_orders(num_orders=500):
    orders = []
    base_date = datetime.now() - timedelta(days=90)

    for i in range(num_orders):
        customer = random.choice(CUSTOMERS)
        created_at = base_date + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Sélectionner entre 1 et 3 articles par commande
        num_items = random.choices([1, 2, 3], weights=[0.65, 0.25, 0.10])[0]
        selected_products = random.sample(PRODUCTS, num_items)
        
        line_items = []
        total_price = 0.0

        for p in selected_products:
            qty = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]
            price = p["base_price"]
            line_items.append({
                "item_id": f"LI-{uuid.uuid4().hex[:6].upper()}",
                "product_id": p["product_id"],
                "sku": p["sku"],
                "title": p["title"],
                "quantity": qty,
                "price": price,
                "unit_cost": p["cost"]
            })
            total_price += qty * price

        order = {
            "order_id": f"ORD-{10000 + i}",
            "order_number": 10000 + i,
            "created_at": created_at.isoformat(),
            "customer": customer,
            "line_items": line_items,
            "financial_status": "paid",
            "total_price": round(total_price, 2),
            "currency": "USD"
        }
        orders.append(order)

    file_path = OUTPUT_DIR / "shopify_orders.json"
    with open(file_path, "w", encoding="utf-8") as f:
        for order in orders:
            f.write(json.dumps(order) + "\n")
    print(f"-> {len(orders)} commandes Shopify générées dans {file_path}")

def generate_marketing_ads(days=90):
    ads_records = []
    base_date = datetime.now() - timedelta(days=days)
    platforms = ["Meta Ads", "Google Ads"]
    campaigns = [
        {"campaign_id": "CMP-META-RETARGET", "name": "Meta Dynamic Retargeting", "channel": "Meta Ads"},
        {"campaign_id": "CMP-META-PROSPECT", "name": "Meta Lookalike Top of Funnel", "channel": "Meta Ads"},
        {"campaign_id": "CMP-GOOG-SEARCH", "name": "Google Brand Search", "channel": "Google Ads"},
        {"campaign_id": "CMP-GOOG-PERFMAX", "name": "Google Performance Max Tech", "channel": "Google Ads"}
    ]

    for d in range(days):
        current_date = (base_date + timedelta(days=d)).strftime("%Y-%m-%d")
        for camp in campaigns:
            spend = round(random.uniform(40.0, 220.0), 2)
            impressions = int(spend * random.uniform(25, 45))
            clicks = int(impressions * random.uniform(0.015, 0.045))
            conversions = int(clicks * random.uniform(0.02, 0.08))

            record = {
                "date": current_date,
                "channel": camp["channel"],
                "campaign_id": camp["campaign_id"],
                "campaign_name": camp["name"],
                "impressions": impressions,
                "clicks": clicks,
                "spend": spend,
                "conversions": conversions
            }
            ads_records.append(record)

    file_path = OUTPUT_DIR / "marketing_ads.json"
    with open(file_path, "w", encoding="utf-8") as f:
        for record in ads_records:
            f.write(json.dumps(record) + "\n")
    print(f"-> {len(ads_records)} lignes Ads générées dans {file_path}")

if __name__ == "__main__":
    generate_shopify_orders()
    generate_marketing_ads()