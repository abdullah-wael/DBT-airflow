select id
from {{ref('stg_orders')}} where
 total_amount < 0
