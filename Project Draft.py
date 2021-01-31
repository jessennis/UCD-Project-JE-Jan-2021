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


fc=plt.subplots

fig0, ax = fc()
ax.plot(covid_pt.index, covid_pt["Dublin"], color='b', label='Dublin')
ax.plot(covid_pt.index, covid_pt["National"], color='r', label ='National')
ax.set_xlabel("Time (Months)")
ax.set_ylabel("Confirmed Covid Cases")
ax.legend(loc="upper center")
ax.set_title("Confirmed Covid Cases")
plt.show()
fig0.savefig("Confirmed Covid Cases")

df=covid_pt.loc[:, ['Dublin', 'National']]
print(df)
NewCases_df=df.diff()
print(NewCases_df)
print(NewCases_df.isna().sum())
NewCases_df2=NewCases_df.fillna(0)


fig1, ax = fc()
ax.plot(NewCases_df2.index, NewCases_df2["Dublin"], color='b',label='Dublin')
ax.plot(NewCases_df2.index, NewCases_df2["National"], color='r',label='National')
ax.set_xlabel("Time (Months)")
ax.set_ylabel("New Covid Cases per day")
ax.set_title("New Covid Cases")
ax.legend(loc="upper center")
plt.show()
fig1.savefig("New Covid Cases")


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

population_pt = covid_df.pivot_table(columns='CountyName', values='PopulationCensus16')
National = population_pt.sum(axis="columns")
population_pt["National"] = National
print(population_pt)
df2=population_pt.loc[:, ['Dublin', 'National']]
print(df2)


fig2, ax = fc()
fig2.suptitle('Proportion of COVID Cases per Population')
ax.plot(Pop_df2.index, Pop_df2["National"], color='r', label='National')
ax.set_xlabel("Time (Months)")
ax.set_ylabel("National - Proportion of COVID Cases per Population per day")
ax.legend(loc="upper center")
ax2= ax.twinx()
ax2.plot(Pop_df2.index, Pop_df2["Dublin"], color='b', label='Dublin')
ax2.set_xlabel("Time (Months)")
ax2.set_ylabel("Dublin- Proportion of COVID Cases per Population per day")
ax2.legend(loc="upper left")
plt.show()
fig2.savefig("Proportion of COVID Cases per Population")

fig3, ax = fc(2, sharex=True)
fig3.suptitle('New COVID Cases vs Proportion of New COVID Cases per Population')
ax[0].plot(NewCases_df2.index, NewCases_df2["National"], color='r',label='National'),
ax[0].plot(NewCases_df2.index, NewCases_df2["Dublin"], color='b', label='Dublin')
ax[1].plot(Pop_df2.index, Pop_df2["Dublin"], color='b', label='Dublin')
ax[1].plot(Pop_df2.index, Pop_df2["National"], color='r', label='National')
ax[1].set_xlabel("Time (Months)")
ax[0].set_ylabel("New Covid Cases")
ax[1].set_ylabel("Proportion per Population")
ax[0].legend(loc="upper center")
plt.show()

fig3.savefig("New COVID Cases vs Proportion of New COVID Cases per Population")