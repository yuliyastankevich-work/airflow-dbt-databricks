-- back compat for old kwarg name
  
  
  
  
  
  
      
          
          
      
  

    merge
    into
        `wallmart`.`silver_tech`.`orders_tech` as DBT_INTERNAL_DEST
    using
        `orders_tech__dbt_tmp` as DBT_INTERNAL_SOURCE
    on
        
              DBT_INTERNAL_SOURCE.`order_id` <=> DBT_INTERNAL_DEST.`order_id`
          
    when matched
        then update set
            *
    when not matched
        then insert
            *
