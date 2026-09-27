#!/bin/bash
set -e

echo "=== Phase 1: Generating Mock Data ==="
python src/generator/generate_data.py

echo "=== Phase 2: Ingesting into Snowflake (Bronze) ==="
python src/ingestion/upload_to_stage.py

echo "=== Phase 3: Running dbt Transformations & Tests (Silver/Gold) ==="
cd dbt_ecommerce
dbt run --profiles-dir .
dbt test --profiles-dir .

echo "=== Pipeline Completed Successfully! ==="
