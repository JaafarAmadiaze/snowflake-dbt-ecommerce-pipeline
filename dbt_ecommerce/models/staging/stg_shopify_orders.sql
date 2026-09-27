with source as (
    select * from {{ source('raw_ecommerce', 'RAW_SHOPIFY_ORDERS') }}
),

flattened as (
    select
        raw_payload:order_id::varchar as order_id,
        raw_payload:order_number::number as order_number,
        raw_payload:created_at::timestamp_ntz as created_at,
        raw_payload:customer.customer_id::varchar as customer_id,
        raw_payload:financial_status::varchar as financial_status,
        raw_payload:total_price::float as total_amount,
        raw_payload:currency::varchar as currency,
        ingested_at
    from source
)

select * from flattened