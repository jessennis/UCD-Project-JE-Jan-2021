import numpy as np
import pandas as pd
from urllib.request import urlretrieve
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D'
urlretrieve(url, 'covid_county.csv')
covid_df = pd.read_csv('covid_county.csv', index_col = 0)
covid_df.info()
covid_df2=covid_df.loc[:, ['TimeStamp','CountyName','ConfirmedCovidCases']]
covid_pt=covid_df2.pivot_table(values='ConfirmedCovidCases', index='TimeStamp', columns='CountyName')
National=covid_pt.sum(axis="columns")
covid_pt["National"]= National
print(covid_pt)

fig, ax = plt.subplots()
ax.plot(covid_pt.index, covid_pt["Dublin"])
ax.plot(covid_pt.index, covid_pt["National"])
ax.set_xlabel('TimeStamp')
ax.set_ylabel('ConfirmedCovidCases')
plt.show()
