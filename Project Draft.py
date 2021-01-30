import numpy as np
import pandas as pd
from urllib.request import urlretrieve
import matplotlib.pyplot as plt

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

fig1, ax = plt.subplots()
ax.plot(NewCases_df2.index, NewCases_df2["Dublin"], color='b')
ax.plot(NewCases_df2.index, NewCases_df2["National"], color='red')
ax.set_xlabel("Time (Months)")
ax.set_ylabel("New Covid Cases per day")
ax.set_title("New Covid Cases")
plt.show()

fig2, ax = plt.subplots(2,1)
ax[0].plot(NewCases_df2.index, NewCases_df2["Dublin"], color='b')
ax[1].plot(NewCases_df2.index, NewCases_df2["National"], color='red')
ax[1].set_xlabel("Time (Months)")
ax[1].set_ylabel("New Covid Cases per day")
plt.show()

pop_pt = covid_df.pivot_table(index=pd.Grouper(freq='D', key='TimeStamp'), columns='CountyName', values='PopulationProportionCovidCases', aggfunc='sum')
National = pop_pt.sum(axis="columns")
pop_pt["National"] = National
print(pop_pt)
df2=pop_pt.loc[:, ['Dublin', 'National']]
print(df2)
Pop_df=df2.diff()
print(Pop_df)
print(Pop_df.isna().sum())
Pop_df2=Pop_df.fillna(0)
print(Pop_df2)


fig3, ax = plt.subplots()
ax.plot(Pop_df2.index, Pop_df2["Dublin"], color='b')
ax.plot(Pop_df2.index, Pop_df2["National"], color='red')
ax.set_xlabel("Time (Months)")
ax.set_ylabel("New Covid Cases per Proportion of Population per day")
ax.set_title("New Covid Cases per Proportion of Population ")
plt.show()

fig4, ax = plt.subplots(2,1, sharey=True)
ax[0].plot(NewCases_df2.index, NewCases_df2["Dublin"], color='b')
ax[0].plot(NewCases_df2.index, NewCases_df2["National"], color='red'),
ax[1].plot(Pop_df2.index, Pop_df2["Dublin"], color='b')
ax[1].plot(Pop_df2.index, Pop_df2["National"], color='red')
ax[0].set_xlabel("Time (Months)")
ax[0].set_ylabel("New Covid Cases per day")
ax[1].set_ylabel("New Covid Cases per Proportion of Population per day")
plt.show()

Merged_df=NewCases_df2.merge(Pop_df2, on='TimeStamp', how='right')
print(Merged_df)
print(Merged_df.columns)
print(Merged_df[["Dublin_x", "National_x", "Dublin_y", "National_y","Dub_percentage"]].max())
print(Merged_df[["Dublin_x", "National_x", "Dublin_y", "National_y","Dub_percentage"]].min())