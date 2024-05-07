# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from lgg import mylib
import logging
logging.basicConfig(filename='/Users/jordanburke/Library/DataScienceStudio/dss_home/tmp/myapp.log', level=logging.INFO, format='%(asctime)s %(message)s', force=True)
logger = logging.getLogger(__name__)

logger.info("Hello world")

logger.info('Started')
mylib.do_something()

logger.info('Started')
data = [['tom', 10], ['nick', 15], ['juli', 14]]
 
# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Name', 'Age'])


loggingtest_df = df
logger.info('Finished')


# Write recipe outputs
loggingtest = dataiku.Dataset("loggingtest")
loggingtest.write_with_schema(loggingtest_df)
