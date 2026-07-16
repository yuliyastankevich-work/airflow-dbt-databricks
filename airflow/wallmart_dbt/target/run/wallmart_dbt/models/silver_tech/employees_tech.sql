-- back compat for old kwarg name
  
  
  
  
  
  
      
          
          
      
  

    merge
    into
        `wallmart`.`silver_tech`.`employees_tech` as DBT_INTERNAL_DEST
    using
        `employees_tech__dbt_tmp` as DBT_INTERNAL_SOURCE
    on
        
              DBT_INTERNAL_SOURCE.`employee_id` <=> DBT_INTERNAL_DEST.`employee_id`
          
    when matched
        then update set
            *
    when not matched
        then insert
            *
