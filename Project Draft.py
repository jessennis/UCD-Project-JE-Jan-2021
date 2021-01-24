import numpy as np

import pandas as pd

from urllib.request import urlretrieve

import matplotlib.pyplot as plt

url = 'https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D'
urlretrieve(url, 'covid_county.csv')
covid_df = pd.read_csv('covid_county.csv', index_col = 0)
covid_df.info()

covid_df2=covid_df.loc[:, ['TimeStamp','CountyName','ConfirmedCovidCases']]
covid_df3=covid_df2[covid_df2["CountyName"] == "Dublin"]
covid_df3.set_index('TimeStamp')
print(covid_df3)




