select unit_price
from {{ref('stg_order_items')}}
where unit_price < 0