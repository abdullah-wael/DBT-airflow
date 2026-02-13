select id as customer_id
, name as Full_name
,trim(email) as Email
,trim(country) as Country
from {{ref('stg_customers')}}