SELECT 
    *,
    (tip_amount::int / total_amount::int) * 100 AS tip_percentage
FROM 
    "public"."SQL_nyc_trips_copy"