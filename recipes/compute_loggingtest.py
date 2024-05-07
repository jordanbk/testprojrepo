# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="/Users/jordanburke/Library/DataScienceStudio/dss_home/loggingtest.log",
                format='%(asctime)s %(message)s',
                filemode='w')

logger.info('Started')
data = [['tom', 10], ['nick', 15], ['juli', 14]]
 
# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Name', 'Age'])


loggingtest_df = df
logger.info('Finished')
if __name__ == '__main__':
    main()

# Write recipe outputs
loggingtest = dataiku.Dataset("loggingtest")
loggingtest.write_with_schema(loggingtest_df)
