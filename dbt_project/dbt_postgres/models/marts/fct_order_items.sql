select oi.id as Order_items_id
,oi.order_id as Order_id,oi.product_id as Product_id,
o.customer_id as Customer_id,
oi.quantity as Quantity,
oi.unit_price as Unit_price,
(oi.quantity*oi.unit_price) as Total_amount
,d.date_id as Date_id
from {{ref('stg_order_items')}} as oi 
join {{ref('stg_orders')}} as o
on oi.order_id=o.id
join {{ref('dim_date')}} as d
on o.order_date=d.order_date
