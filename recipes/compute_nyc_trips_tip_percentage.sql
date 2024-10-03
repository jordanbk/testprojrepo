SELECT 
    *,
    (tip_amount / total_amount) * 100 AS tip_percentage
FROM 
    "public"."SQL_nyc_trips_copy"