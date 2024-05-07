# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu



import logging

logging.basicConfig(filename="guided_repair_dataiku_python_library.log",
                format='%(asctime)s %(message)s',
                filemode='w')

loggingtest_df = ... # Compute a Pandas dataframe to write into loggingtest


# Write recipe outputs
loggingtest = dataiku.Dataset("loggingtest")
loggingtest.write_with_schema(loggingtest_df)
