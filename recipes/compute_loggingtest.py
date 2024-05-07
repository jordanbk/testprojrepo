# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from lgg import mylib
import logging
logging.basicConfig(filename='/Users/jordanburke/Library/DataScienceStudio/dss_home/tmp/myapp.log', level=logging.INFO, format='%(asctime)s %(message)s', force=True)
import logging

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/Users/jordanburke/Library/DataScienceStudio/dss_home/tmp/spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('creating an instance of auxiliary_module.Auxiliary')
a = mylib.Auxiliary()
logger.info('created an instance of auxiliary_module.Auxiliary')
logger.info('calling auxiliary_module.Auxiliary.do_something')
a.do_something()
logger.info('finished auxiliary_module.Auxiliary.do_something')
logger.info('calling auxiliary_module.some_function()')
mylib.some_function()
logger.info('done with auxiliary_module.some_function()')

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
