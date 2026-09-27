with source as (
    select * from {{ source('raw_ecommerce', 'RAW_SHOPIFY_ORDERS') }}
),

raw_customers as (
    select distinct
        raw_payload:customer.customer_id::varchar as customer_id,
        raw_payload:customer.first_name::varchar as first_name,
        raw_payload:customer.last_name::varchar as last_name,
        raw_payload:customer.email::varchar as email,
        raw_payload:customer.city::varchar as city,
        raw_payload:customer.country::varchar as country
    from source
),

order_summary as (
    select
        customer_id,
        count(distinct order_id) as lifetime_orders,
        sum(total_amount) as lifetime_spend,
        min(created_at) as first_order_at,
        max(created_at) as most_recent_order_at
    from {{ ref('stg_shopify_orders') }}
    group by customer_id
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.city,
    c.country,
    coalesce(s.lifetime_orders, 0) as lifetime_orders,
    coalesce(s.lifetime_spend, 0.0) as lifetime_spend,
    s.first_order_at,
    s.most_recent_order_at
from raw_customers c
left join order_summary s on c.customer_id = s.customer_id
