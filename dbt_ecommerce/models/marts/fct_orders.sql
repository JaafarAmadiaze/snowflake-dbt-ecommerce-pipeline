with orders as (
    select * from {{ ref('stg_shopify_orders') }}
),

item_metrics as (
    select
        order_id,
        count(order_item_id) as total_items_count,
        sum(quantity) as total_units_sold,
        sum(line_item_cost) as total_order_cost
    from {{ ref('stg_shopify_order_items') }}
    group by order_id
)

select
    o.order_id,
    o.order_number,
    to_date(o.created_at) as order_date,
    o.created_at as order_timestamp,
    o.customer_id,
    o.financial_status,
    coalesce(i.total_items_count, 0) as total_items_count,
    coalesce(i.total_units_sold, 0) as total_units_sold,
    o.total_amount as gross_revenue,
    coalesce(i.total_order_cost, 0.0) as cost_of_goods_sold,
    round(o.total_amount - coalesce(i.total_order_cost, 0.0), 2) as gross_profit,
    case 
        when o.total_amount > 0 
        then round((o.total_amount - coalesce(i.total_order_cost, 0.0)) / o.total_amount, 4)
        else 0.0 
    end as gross_margin_percentage
from orders o
left join item_metrics i on o.order_id = i.order_id
