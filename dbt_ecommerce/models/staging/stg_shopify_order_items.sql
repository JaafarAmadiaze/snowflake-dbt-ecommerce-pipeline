with source as (
    select * from {{ source('raw_ecommerce', 'RAW_SHOPIFY_ORDERS') }}
),

items as (
    select
        raw_payload:order_id::varchar as order_id,
        raw_payload:created_at::timestamp_ntz as order_created_at,
        item.value:item_id::varchar as order_item_id,
        item.value:product_id::varchar as product_id,
        item.value:sku::varchar as sku,
        item.value:title::varchar as product_title,
        item.value:quantity::number as quantity,
        item.value:price::float as unit_price,
        item.value:unit_cost::float as unit_cost,
        (item.value:quantity::number * item.value:price::float) as line_item_subtotal,
        (item.value:quantity::number * item.value:unit_cost::float) as line_item_cost
    from source,
    lateral flatten(input => raw_payload:line_items) item
)

select * from items