# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
us_tornado_dataset_1950_2021_prepared = dataiku.Dataset("us_tornado_dataset_1950_2021_prepared")
us_tornado_dataset_1950_2021_prepared_df = us_tornado_dataset_1950_2021_prepared.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

us_tornado_test_df = us_tornado_dataset_1950_2021_prepared_df # For this sample code, simply copy input to output


# Write recipe outputs
us_tornado_test = dataiku.Dataset("us_tornado_test")
us_tornado_test.write_with_schema(us_tornado_test_df)
