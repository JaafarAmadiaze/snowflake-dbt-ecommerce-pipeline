with ads as (
    select * from {{ ref('stg_marketing_ads') }}
)

select
    date_day,
    marketing_channel,
    campaign_id,
    campaign_name,
    impressions,
    clicks,
    spend as ad_spend,
    conversions,
    case 
        when impressions > 0 then round((clicks::float / impressions) * 100, 2)
        else 0.0 
    end as click_through_rate_pct,
    case 
        when clicks > 0 then round(spend / clicks, 2)
        else 0.0 
    end as cost_per_click,
    case 
        when conversions > 0 then round(spend / conversions, 2)
        else 0.0 
    end as cost_per_acquisition
from ads
