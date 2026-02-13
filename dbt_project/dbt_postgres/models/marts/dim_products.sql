select id as product_id
,trim(name) as Product_name
,trim(category) as Product_category
from {{ref('stg_products')}}