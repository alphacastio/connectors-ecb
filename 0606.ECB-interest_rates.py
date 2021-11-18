#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
import datetime
import urllib
import time
from urllib.request import urlopen
import requests  

from alphacast import Alphacast
from dotenv import dotenv_values
API_KEY = dotenv_values(".env").get("API_KEY")
alphacast = Alphacast(API_KEY)

# In[ ]:


url = "https://sdw.ecb.europa.eu/browseTable.do?org.apache.struts.taglib.html.TOKEN=cf1e76ee4dc40c69de84145bf7d51c0b&df=true&MAX_DOWNLOAD_SERIES=500&DATASET=0&org.apache.struts.taglib.html.TOKEN=f3a664acac9c45eaefba7848eb62a16e&legendRef=reference&node=9691107&SERIES_MAX_NUM=50&SERIES_KEY=143.FM.B.U2.EUR.4F.KR.DFR.LEV&SERIES_KEY=143.FM.B.U2.EUR.4F.KR.MLFR.LEV&SERIES_KEY=143.FM.D.U2.EUR.4F.KR.MRR_FR.LEV&activeTab=FM&start=01-08-2008&end=&submitOptions.x=0&submitOptions.y=0&trans=N&q=&type="
df = pd.read_html(requests.get(url).text)[9]


# In[ ]:


df = df.iloc[2:,:]
df.columns = ["Date", "ECB Deposit facility", "ECB Marginal lending facility", "ECB Main refinancing operations - fixed rate tenders"]


# In[ ]:


df.index = pd.to_datetime(df["Date"])
del df["Date"]
df = df.sort_index()
df = df.fillna(method='ffill')


# In[ ]:


df["country"] = "Euro Area"

alphacast.datasets.dataset(606).upload_data_from_df(df, 
    deleteMissingFromDB = True, onConflictUpdateDB = True, uploadIndex=True)

# In[ ]:




