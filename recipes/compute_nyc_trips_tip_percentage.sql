SELECT 
    *,
    CASE 
        WHEN total_amount = 0 THEN 0
        ELSE (tip_amount / total_amount) * 100
    END AS tip_percentage
FROM 
    "public"."SQL_nyc_trips_copy"