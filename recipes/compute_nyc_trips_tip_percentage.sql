SELECT 
    *,
    CASE 
        WHEN total_amount::float = 0 THEN 0
        ELSE (tip_amount::float / total_amount::float) * 100
    END AS tip_percentage
FROM 
    "public"."SQL_nyc_trips_copy"