with order_items as (
    select * from {{ ref('stg_shopify_order_items') }}
)

select distinct
    product_id,
    sku,
    product_title,
    unit_cost as standard_cost,
    unit_price as current_price
from order_items
