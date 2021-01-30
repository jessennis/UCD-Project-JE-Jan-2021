import numpy as np
import pandas as pd
from urllib.request import urlretrieve
import matplotlib.pyplot as plt
import seaborn as sns
import jinja2

url = 'https://opendata-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D'
urlretrieve(url, 'covid_county.csv')
covid_df = pd.read_csv('covid_county.csv', index_col=0)
print(covid_df.head())
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
NewCases_df["Dub_percentage"]=NewCases_df['Dublin']/NewCases_df['National']
print(NewCases_df)

print(NewCases_df.isna().sum())
NewCases_df2=NewCases_df.fillna(0)
print(NewCases_df2)

NewCases_df2['Dub_percentage'] = pd.Series(["{0:.2f}%".format(val * 100) for val in NewCases_df2['Dub_percentage']], index = NewCases_df2.index)
print(NewCases_df2)


fig, ax = plt.subplots()
ax.plot(NewCases_df2.index, NewCases_df2["Dublin"],
        NewCases_df2.index, NewCases_df2["National"])
ax.set_xlabel("Time (Months)")
ax.set_ylabel("New Covid Cases per day")
ax.set_title("New Covid Cases")
ax.legend()
plt.show()




