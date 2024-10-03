SELECT 
    *,
    CASE 
        WHEN total_amount::float = 0 THEN 0
        ELSE ROUND((tip_amount::float / total_amount::float) * 100, 2)
    END AS tip_percentage
FROM 
    "public"."SQL_nyc_trips_copy"