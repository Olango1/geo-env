# %%
#Load data and libraries
import numpy as np
import pandas as pd
import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt
dset = xr.open_dataset(r"C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Data/ERA5_Data/download.nc")

# %%
#Extracting the data
t2m = np.array(dset.variables['t2m'])
tp = np.array(dset.variables['tp'])
latitude = np.array(dset.variables['latitude'])
longitude = np.array(dset.variables['longitude'])
time_dt = np.array(dset.variables['time'])

# %%
#Convert temperature to Celsius and precipitation to mm/h
t2m = t2m - 273.15
tp = tp * 1000

# %%
#Computing mean across the second dimension
if t2m.ndim == 4:
    t2m = np.nanmean(t2m, axis=1)
    tp = np.nanmean(tp, axis=1)
    tp

# %%
#Defining location of wadi within the data
df_era5 = pd.DataFrame(index=time_dt)
df_era5['t2m'] = t2m[:,3,2]
df_era5['tp'] = tp[:,3,2]
df_era5

# %%
#Plot time series of temperature and precipitation on same axes
plt.figure(figsize=(10, 6))
df_era5.plot()
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Time Series Plot')
plt.legend()

plt.savefig('Time_Series_Plot.png')
plt.show()

# %%
#Resample data to annual values and find the mean precipitation
annual_precip = df_era5['tp'].resample('A').mean()
mean_annual_precip = np.nanmean(annual_precip)
mean_annual_precip

# %%
#Deriving the maximum, minimum, and mean daily temperatures from the dataset
tmin = df_era5['t2m'].resample('D').min().values
tmax = df_era5['t2m'].resample('D').max().values
tmean = df_era5['t2m'].resample('D').mean().values
lat = 21.25
doy = df_era5['t2m'].resample('D').mean().index.dayofyear

# %%
#Computing PE
import tools
pe = tools.hargreaves_samani_1982(tmin, tmax, tmean, lat, doy)
pe

# %%
#Plotting PE time series

ts_index = np.array(df_era5['t2m'].resample('D').mean().index)
plt.figure(figsize=(10, 6), tight_layout=True)
plt.plot(ts_index, pe, label='Potential Evaporation')
plt.xlabel('Date')
plt.ylabel('PE [mm day−1]')
plt.title('Potential Evaporation Time Series')
plt.grid(True)

# %%
# Calculating mean annual PE in mm y−1
mean_annual_pe = np.nanmean(pe)
mean_annual_pe

# %%
# Calculating mean volume of water evaporated in m3 y−1 over 1.6 km2 of wadi area
wadi_area = 1.6e6
mean_volume_evaporated = (mean_annual_pe/1000) * wadi_area
mean_volume_evaporated