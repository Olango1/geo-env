#Import necessary libraries
import tools
import matplotlib.pyplot as plt
import pandas as pd
import pdb

#Reading the data file
df_isd = tools.read_isd_csv(r"C:/Users/Em/Desktop/phd/Geo-modelling/Data/ISD_Data/41024099999.csv")
plot = df_isd.plot(title="ISD data for Jeddah")
plt.show()

#Convert dew point temperature to relative humidity from tools.py
df_isd['RH'] = tools.dewpoint_to_rh(df_isd['DEW'].values,df_isd['TMP'].values)

#Calculating the Heat Index (HI) from air temperature and relative humidity
df_isd['HI'] = tools.gen_heat_index(df_isd['TMP'].values, df_isd['RH'].values)

#Highest HI in 2023
df_isd.max()

#The day and time when the highest HI was observed
df_isd.idxmax()

# Air temperature and relative humidity were observed at this moment
df_isd.loc[["2023-08-21 10:00:00"]]

#Resample the data to daily weather data from hourly
daily=df_isd.resample('D').mean()
daily
#Plot for HI time series for 2023 daily
plot = daily['HI'].plot(title="Heat Index for Jeddah")
plt.xlabel("Date")
plt.ylabel("Heat Index ◦C")
plt.show()

#Plot for HI time series for 2023
plot = df_isd['HI'].plot(title="ISD data for Jeddah")
plt.xlabel("Date")
plt.ylabel("Heat Index ◦C")
plt.show()

#Applying the temperature increase to all values
df_isd['C_TMP']=df_isd.TMP+3
#Recalculating the HI
df_isd['C_RH'] = tools.dewpoint_to_rh(df_isd['DEW'].values,df_isd['C_TMP'].values)
df_isd['C_HI'] = tools.gen_heat_index(df_isd['C_TMP'].values, df_isd['RH'].values)
#Calculate increasee in HI
HI_inc=df_isd['C_HI'].max()-df_isd['HI'].max()
HI_inc

# pdb.set_trace()
