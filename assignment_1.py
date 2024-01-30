#Importing required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr

#Acessing dataset
dset = xr.open_dataset(r'C:/Users/Em/Desktop/phd/Geo-modelling/SRTMGL1_NC.003_Data/N21E039.SRTMGL1_NC.nc')
dset
# pdb.set_trace()

#Explore variables
dset.variables

#Access variable containing elevation data
DEM = np.array(dset.variables['SRTMGL1_DEM'])
DEM

# dset.close()
# pdb.set_trace()

#Visualize the elevation data
plt.imshow(DEM)
cbar = plt.colorbar()
cbar.set_label('Elevation (m asl)')
plt.show()

#Save the plotted figure
plt.savefig('C:/Users/Em/Downloads/assignment 1.png', dpi=300)
