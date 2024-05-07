# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import myapp from logging
import logging

logger = logging.getLogger(__name__)

def do_something():
    logger.info('Doing something')

logger.info('Started')
data = [['tom', 10], ['nick', 15], ['juli', 14]]
 
# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Name', 'Age'])


loggingtest_df = df
logger.info('Finished')


# Write recipe outputs
loggingtest = dataiku.Dataset("loggingtest")
loggingtest.write_with_schema(loggingtest_df)
