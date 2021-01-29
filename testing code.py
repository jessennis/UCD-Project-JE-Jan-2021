import numpy as np
import pandas as pd
from urllib.request import urlretrieve
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D'
urlretrieve(url, 'covid_county.csv')
covid_df = pd.read_csv('covid_county.csv', index_col=0)


covid_df.info()
covid_df['TimeStamp']=pd.to_datetime(covid_df['TimeStamp'])
covid_df = covid_df.loc[:, ['TimeStamp', 'CountyName','ConfirmedCovidCases']]
covid_pt = covid_df.pivot_table(index=pd.Grouper(freq='W', key='TimeStamp'), columns='CountyName', values='ConfirmedCovidCases', aggfunc='sum')
National = covid_pt.sum(axis="columns")
covid_pt["National"] = National
print(covid_pt)

for lab, row in covid_pt.iterrows():
    covid_pt.loc[lab, "TimeStamp"]=len(row["CountyName"])
    print(covid_pt)