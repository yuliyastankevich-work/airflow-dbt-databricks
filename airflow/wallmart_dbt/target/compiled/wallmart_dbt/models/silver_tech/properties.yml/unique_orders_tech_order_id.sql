
    
    

select
    order_id as unique_field,
    count(*) as n_records

from `wallmart`.`silver_tech`.`orders_tech`
where order_id is not null
group by order_id
having count(*) > 1


