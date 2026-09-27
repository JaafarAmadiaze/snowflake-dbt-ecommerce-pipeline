with date_spine as (
    select 
        dateadd(day, seq4(), dateadd(day, -180, current_date())) as date_day
    from table(generator(rowcount => 365))
)

select
    date_day,
    extract(year from date_day) as year,
    extract(quarter from date_day) as quarter,
    extract(month from date_day) as month,
    to_char(date_day, 'MMMM') as month_name,
    extract(day from date_day) as day_of_month,
    to_char(date_day, 'DY') as day_of_week
from date_spine
