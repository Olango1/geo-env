#Importing required packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


#Opening the dataset from the different periods
dset = xr.open_dataset('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_195001-201412.nc', decode_times=True)
dset_1900 = xr.open_dataset('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc')
dset_2100_s1 = xr.open_dataset('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp119_r1i1p1f1_gr1_201501-210012.nc')
dset_2100_s2 = xr.open_dataset('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp245_r1i1p1f1_gr1_201501-210012.nc')
dset_2100_s3 = xr.open_dataset('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp585_r1i1p1f1_gr1_201501-210012.nc')
dset

#Printing variable names
dset.variables.keys()

###################################################################
# #Printing the variables within the dataset and their properties in a dataframe
# # Creating an empty DataFrame to store variable names and properties
# variable_info_df = pd.DataFrame(columns=['Variable_Name', 'Shape', 'Dimensions', 'Attributes'])

# # Looping through all variables in the dataset
# for variable_name in dset.variables:
#     variable = dset[variable_name]
    
#     # Get variable properties
#     shape = variable.shape
#     dimensions = variable.dims
#     attributes = variable.attrs
    
#     # Appending information to the DataFrame
#     variable_info_df = pd.concat([variable_info_df, pd.DataFrame({
#         'Variable_Name': [variable_name],
#         'Shape': [shape],
#         'Dimensions': [dimensions],
#         'Attributes': [attributes]
#     })], ignore_index=True)


# variable_info_df.reset_index(drop=True, inplace=True)

# variable_info_df

##############################################################
#Accessing the air temperature variable
dset['tas']

#Dimensions of the air temperature variable
dset['tas'].shape

#Data type of the air temperature variable
dset['tas'].dtype

############################################################
#Calculating the mean air temperature map for 1850–1900
data_1900=np.mean(dset_1900['tas'].sel(time=slice('18500101', '19001231')), axis=0)
# dset_1900

############################################################
#Calculating the mean air temperature map for 2071–2100 for the three scenarios
data_2100_s1=np.mean(dset_2100_s1['tas'].sel(time=slice('20710101', '21001231')), axis=0)
data_2100_s2=np.mean(dset_2100_s2['tas'].sel(time=slice('20710101', '21001231')), axis=0)
data_2100_s3=np.mean(dset_2100_s3['tas'].sel(time=slice('20710101', '21001231')), axis=0)

##############################################################
# Compute and visualize the temperature differences between 2071–2100 and 1850–1900
array_2100_s1 = np.array(data_2100_s1.data)
array_2100_s2 = np.array(data_2100_s2.data)
array_2100_s3 = np.array(data_2100_s3.data)
array_1900=np.array(data_1900.data)

#Computing difference for the two periods
arr_diff_s1=array_2100_s1-array_1900
arr_diff_s2=array_2100_s2-array_1900
arr_diff_s3=array_2100_s3-array_1900
# arr_diff_s1

#############################################################
#Create dataframe to obtain the coordinates for plotting from the temperature data
df_1900 = data_1900.to_dataframe()
df1 = df_1900.reset_index()
df1

############################################################
#Plotting mean temperature 1850-1900
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# Scatter plot of temperature data
scatter = ax.scatter(df1['lon'], df1['lat'], c=df1['tas'], cmap='viridis', s=100, transform=ccrs.PlateCarree())

# Add coastlines and gridlines for reference
ax.coastlines(linewidth=0.4)
# Add gridlines and labels
gl = ax.gridlines(draw_labels=True, linestyle='--', color='black', linewidth=0.3)
# gl.xlines = False
# gl.ylines = False
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', pad=0.1)
cbar.set_label('Temperature (K)')

# Add title
plt.title('Mean Air Temperature Map(1850-1900)')
# Show the save and plot
plt.savefig('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Results/Mean Air Temperature Map(1850-1900).png', dpi=300)
plt.show()

###############################################
# Create separate figures for each scenario
fig, axes = plt.subplots(3, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
axes = axes.flatten()

scenarios = ['Scenario 1', 'Scenario 2', 'Scenario 3']

for ax, scenario, temperature_array in zip(axes, scenarios, [array_2100_s1, array_2100_s2, array_2100_s3]):
    # Scatter plot of temperature data
    scatter = ax.scatter(df1['lon'], df1['lat'], c=temperature_array, cmap='viridis', s=100, label=scenario, transform=ccrs.PlateCarree())

    # Add coastlines and gridlines for reference
    ax.coastlines(linewidth=0.4)

    # Add gridlines and labels
    gl = ax.gridlines(draw_labels=True, linestyle='--', color='black', linewidth=0.3)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # Add colorbar for each subplot
    cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', pad=0.1, label='Temperature (K)')

    # Add legend
    # ax.legend()

    # Add title
    ax.set_title(f'Mean Air Temperature Map - {scenario}')

# Adjust layout for better spacing
plt.tight_layout()

# Show the save and plot
plt.savefig('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Results/Mean Air Temperature Map(2071-2100)', dpi=300)
plt.show()

###########################################
# Create separate figures for each scenario
fig, axes = plt.subplots(3, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
axes = axes.flatten()

scenarios = ['Scenario 1', 'Scenario 2', 'Scenario 3']

for ax, scenario, temperature_array in zip(axes, scenarios, [arr_diff_s1, arr_diff_s2, arr_diff_s3]):
    # Scatter plot of temperature data
    scatter = ax.scatter(df1['lon'], df1['lat'], c=temperature_array, cmap='inferno', s=100, label=scenario, transform=ccrs.PlateCarree())

    # Add coastlines and gridlines for reference
    ax.coastlines(linewidth=0.4)

    # Add gridlines and labels
    gl = ax.gridlines(draw_labels=True, linestyle='--', color='black', linewidth=0.3)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # Add colorbar for each subplot
    cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', pad=0.1, label='Temperature (K)')

    # Add legend
    # ax.legend()

    # Add title
    ax.set_title(f'Temperature Difference - {scenario}')

    # Add axis labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

# Adjust layout for better spacing
plt.tight_layout()



# Show the save and plot
plt.savefig('C:/Users/Em/OneDrive - University of Twente/Desktop/phd/Geo-modelling/Results/Temperature difference', dpi=300)
plt.show()