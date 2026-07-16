

SELECT *,
        current_timestamp() as processed_at
FROM
`wallmart`.`bronze`.`orders`

WHERE

    updated_timestamp > (SELECT COALESCE(MAX(updated_timestamp), '1200-01-01') FROM `wallmart`.`silver_tech`.`orders_tech`)
