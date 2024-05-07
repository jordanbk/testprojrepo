# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/Users/jordanburke/Library/DataScienceStudio/dss_home/tmp/myapp.log')
fh.setLevel(logging.DEBUG)

logger.info('Started')
data = [['tom', 10], ['nick', 15], ['juli', 14]]
 
# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Name', 'Age'])


loggingtest_df = df
logger.info('Finished')


# Write recipe outputs
loggingtest = dataiku.Dataset("loggingtest")
loggingtest.write_with_schema(loggingtest_df)
