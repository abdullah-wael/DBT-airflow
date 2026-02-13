    select price 
    from {{ref('stg_products')}}
    where price<0