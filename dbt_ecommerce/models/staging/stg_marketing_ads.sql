with source as (
    select * from {{ source('raw_ecommerce', 'RAW_MARKETING_ADS') }}
),

flattened as (
    select
        raw_payload:date::date as date_day,
        raw_payload:channel::varchar as marketing_channel,
        raw_payload:campaign_id::varchar as campaign_id,
        raw_payload:campaign_name::varchar as campaign_name,
        raw_payload:impressions::number as impressions,
        raw_payload:clicks::number as clicks,
        raw_payload:spend::float as spend,
        raw_payload:conversions::number as conversions,
        ingested_at
    from source
)

select * from flattened