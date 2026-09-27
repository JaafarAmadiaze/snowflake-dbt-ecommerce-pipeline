import os
from pathlib import Path
import snowflake.connector
from dotenv import load_dotenv

# Charger les variables d'environnement depuis config/.env
env_path = Path(__file__).resolve().parents[2] / "config" / ".env"
load_dotenv(dotenv_path=env_path)

def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "ECOMMERCE_DWH"),
        schema=os.getenv("SNOWFLAKE_SCHEMA_RAW", "RAW"),
    )

def ingest_data():
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "data_landing"

    orders_file = (data_dir / "shopify_orders.json").as_posix()
    ads_file = (data_dir / "marketing_ads.json").as_posix()

    try:
        print("1. Upload des fichiers JSON vers le stage interne Snowflake (@INTERNAL_RAW_STAGE)...")
        cursor.execute(f"PUT 'file://{orders_file}' @INTERNAL_RAW_STAGE AUTO_COMPRESS=TRUE OVERWRITE=TRUE;")
        cursor.execute(f"PUT 'file://{ads_file}' @INTERNAL_RAW_STAGE AUTO_COMPRESS=TRUE OVERWRITE=TRUE;")
        print("-> Upload terminé avec succès.")

        print("2. Chargement dans les tables RAW (couche Bronze)...")
        
        # Vider les tables temporairement pour éviter les doublons lors des tests
        cursor.execute("TRUNCATE TABLE RAW_SHOPIFY_ORDERS;")
        cursor.execute("TRUNCATE TABLE RAW_MARKETING_ADS;")

        # Copier le JSON brut dans la colonne VARIANT
        cursor.execute("""
            COPY INTO RAW_SHOPIFY_ORDERS (raw_payload)
            FROM (
                SELECT $1 FROM @INTERNAL_RAW_STAGE/shopify_orders.json.gz
            )
            FILE_FORMAT = (TYPE = 'JSON');
        """)
        print("-> RAW_SHOPIFY_ORDERS chargée.")

        cursor.execute("""
            COPY INTO RAW_MARKETING_ADS (raw_payload)
            FROM (
                SELECT $1 FROM @INTERNAL_RAW_STAGE/marketing_ads.json.gz
            )
            FILE_FORMAT = (TYPE = 'JSON');
        """)
        print("-> RAW_MARKETING_ADS chargée.")

        # Vérification rapide du nombre de lignes insérées
        cursor.execute("SELECT COUNT(*) FROM RAW_SHOPIFY_ORDERS;")
        orders_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM RAW_MARKETING_ADS;")
        ads_count = cursor.fetchone()[0]

        print(f"\n[Succès] Lignes en base : {orders_count} commandes, {ads_count} dépenses publicitaires.")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    ingest_data()