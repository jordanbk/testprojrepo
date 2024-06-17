# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
XML = dataiku.Folder("16soUqEn")
XML_info = XML.get_info()


with XML.get_download_stream("books.xml") as f:
    data = pd.read_xml(f)

books_df = data


# Write recipe outputs
books = dataiku.Dataset("books")
books.write_with_schema(books_df)
