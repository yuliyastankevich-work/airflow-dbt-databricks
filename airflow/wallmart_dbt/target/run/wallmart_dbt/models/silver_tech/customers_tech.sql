-- back compat for old kwarg name
  
  
  
  
  
  
      
          
          
      
  

    merge
    into
        `wallmart`.`silver_tech`.`customers_tech` as DBT_INTERNAL_DEST
    using
        `customers_tech__dbt_tmp` as DBT_INTERNAL_SOURCE
    on
        
              DBT_INTERNAL_SOURCE.`customer_id` <=> DBT_INTERNAL_DEST.`customer_id`
          
    when matched
        then update set
            *
    when not matched
        then insert
            *
