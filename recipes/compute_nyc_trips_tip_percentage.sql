SELECT 
    *,
    (tip_amount::float / total_amount::float) * 100 AS tip_percentage
FROM 
    "public"."SQL_nyc_trips_copy"