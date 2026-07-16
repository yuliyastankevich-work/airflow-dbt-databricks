

SELECT *,
        current_timestamp() as processed_at
FROM
`wallmart`.`bronze`.`customers`

WHERE

    updated_timestamp > (SELECT COALESCE(MAX(updated_timestamp), '1200-01-01') FROM `wallmart`.`silver_tech`.`customers_tech`)
