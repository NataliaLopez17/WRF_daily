"""
To run the script, in the terminal write: python {script-name.py} {year desired (1985 or 2040)}
"""
import sys
import datetime
import glob
import os
import pandas as pd
import xarray as xr


# This line reads all the files in the directory and puts them in a list
netcdf_list = glob.glob('NETCDF Files/*.nc', recursive=True)

# This line initializes empty lists to store the data according to the years and models
datasets_CNRM_1985 = []
datasets_CNRM_2040 = []


def classify_netcdf_files():
    """
    This function takes all of the NETCDF files in the directory and generates
    two lists, one for the CNRM-1985 model and one for the CNRM-2040 model.
    """
    for i in netcdf_list:
        # print(netcdf_ds)
        if i.find('CNRM') != -1 and i.find('1985') != -1:
            datasets_CNRM_1985.append(i)
        elif i.find('CNRM') != -1 and i.find('2040') != -1:
            datasets_CNRM_2040.append(i)


def cnrm_1985():
    """
    This function takes all of the files in the datasets_CNRM_1985 list and creates daily csv files.
    The files are stored in separate folders according to the parameter name.
    Everything is stored in the parent path NETCDF Files csv/CNRM-1985-2005/.
    """
    # dates to use in the loop
    first_date = datetime.datetime(1985, 1, 1)
    end_date = datetime.datetime(2005, 12, 31)
    days = xr.cftime_range(start=first_date, end=end_date, freq='D')

    # path to store the files
    source_folder = r'NETCDF Files csv/CNRM-1985-2005/'

    # loops over the list containing the different files from the CNRM model with the 1985 data
    for i in datasets_CNRM_1985:
        for d in days:
            my_list = i.split('\\')[-1]
            name = my_list.split('_')[0]
            # print(name)

            netcdf_ds = xr.open_dataset(i)
            netcdf_ds = netcdf_ds.sel(Time=slice(first_date, end_date))
            netcdf_df = netcdf_ds.to_dataframe()
            netcdf_df = netcdf_df.reset_index()
            netcdf_df = netcdf_df.drop(
                columns=['bnds', 'south_north', 'west_east', 'Time_bnds'])
            netcdf_df = netcdf_df.loc[netcdf_df['Time'] == d]
            dt_object = d.to_pydatetime()
            dt_object = dt_object.strftime('%Y-%m-%d')
            # print(dt_object)

            # This line creates the folders for each parameter inside the source_folder path
            netcdf_df.to_csv(os.path.join(source_folder, name,
                                          '{dt_object}.csv'.format(dt_object=dt_object)))


def cnrm_2040():
    """
    This function takes all of the files in the datasets_CNRM_2040 list and creates daily csv files.
    The files are stored in separate folders according to the parameter name.
    Everything is stored in the parent path NETCDF Files csv/CNRM-2040-2060/.
    """
    first_date = datetime.datetime(2041, 1, 1)
    end_date = datetime.datetime(2060, 12, 31)
    days = pd.date_range(start=first_date, end=end_date, freq='D')

    source_folder = r'NETCDF Files csv/CNRM-2040-2060/'

    for i in datasets_CNRM_2040:
        for d in days:
            my_list = i.split('\\')[-1]
            name = my_list.split('_')[0]
            # print(name)

            netcdf_ds = xr.open_dataset(i)
            netcdf_ds = netcdf_ds.sel(Time=slice(first_date, end_date))
            netcdf_df = netcdf_ds.to_dataframe()
            netcdf_df = netcdf_df.reset_index()
            netcdf_df = netcdf_df.drop(
                columns=['bnds', 'south_north', 'west_east', 'Time_bnds'])
            netcdf_df = netcdf_df.loc[netcdf_df['Time'] == d]
            # print(netcdf_df)
            dt_object = d.to_pydatetime()
            dt_object = dt_object.strftime('%Y-%m-%d')
            # print(dt_object)

            # This line creates the folders for each parameter inside the source_folder path
            netcdf_df.to_csv(os.path.join(source_folder, name,
                                          '{dt_object}.csv'.format(dt_object=dt_object)))


if __name__ == "__main__":
    # Identify the current year desired.
    year = int(sys.argv[1])
    classify_netcdf_files()
    if year == 2040:
        cnrm_2040()
    else:
        cnrm_1985()
