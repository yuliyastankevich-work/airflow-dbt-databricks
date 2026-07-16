{{ config(materialized = 'incremental', unique_key = 'store_id')}}

SELECT *,
        current_timestamp() as processed_at
FROM
{{ source("wallmart_databricks", "stores")}}

WHERE
{% if is_incremental() %}
    updated_timestamp > (SELECT COALESCE(MAX(updated_timestamp), '1200-01-01') FROM {{ this }})
{% endif %}