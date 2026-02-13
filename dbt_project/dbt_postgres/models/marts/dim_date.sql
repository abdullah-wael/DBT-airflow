select
    row_number() over (order by order_date) as date_id,
    order_date,
    extract(day from order_date) as day,
    extract(month from order_date) as month,
    extract(quarter from order_date) as quarter,
    extract(year from order_date) as year
from (
    select distinct order_date
    from {{ ref('stg_orders') }}
) t
