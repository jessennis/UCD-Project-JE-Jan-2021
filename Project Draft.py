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
covid_pt = covid_df.pivot_table(index=pd.Grouper(freq='D', key='TimeStamp'), columns='CountyName', values='ConfirmedCovidCases', aggfunc='sum')
National = covid_pt.sum(axis="columns")
covid_pt["National"] = National
print(covid_pt)

df=covid_pt.loc[:, ['Dublin', 'National']]
print(df)
NewCases_df=df.diff()
print(NewCases_df)

fig, ax = plt.subplots()
ax.plot(NewCases_df.index, NewCases_df["Dublin"])
ax.plot(NewCases_df.index, NewCases_df["National"])
ax.set_xlabel('TimeStamp')
ax.set_ylabel('ConfirmedCovidCases')
ax.set_title("New Covid Cases")
plt.show()



