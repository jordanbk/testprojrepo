# -*- coding: utf-8 -*-
import dataiku
from dataiku import spark as dkuspark
from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

# Read recipe inputs
test_geo = dataiku.Dataset("test_geo")
test_geo_df = dkuspark.get_dataframe(sqlContext, test_geo)

# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a SparkSQL dataframe
test_geo_spark_df = test_geo_df # For this sample code, simply copy input to output

# Write recipe outputs
test_geo_spark = dataiku.Dataset("test_geo_spark")
dkuspark.write_with_schema(test_geo_spark, test_geo_spark_df)
