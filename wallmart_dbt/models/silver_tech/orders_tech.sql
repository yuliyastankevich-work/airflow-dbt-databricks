{{ config(materialized = 'incremental', unique_key = 'order_id')}}

SELECT *,
        current_timestamp() as processed_at
FROM
{{ source("wallmart_databricks", "orders")}}
WHERE is_active = 'Y'

{% if is_incremental() %}
    AND updated_timestamp > (SELECT COALESCE(MAX(updated_timestamp), '1200-01-01') FROM {{ this }})
{% endif %}