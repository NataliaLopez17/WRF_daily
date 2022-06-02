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
datasets_CESM_1985 = []
datasets_CESM_2040 = []


def classify_netcdf_files():
    """
    This function takes all of the NETCDF files in the directory and generates
    two lists, one for the CESM-1985 model and one for the CESM-2040 model.
    """
    # This line reads the data from the netcdf list and puts each file in a list according to the year and model
    for i in netcdf_list:
        if i.find('CESM') != -1 and i.find('1985') != -1:
            datasets_CESM_1985.append(i)
        elif i.find('CESM') != -1 and i.find('2040') != -1:
            datasets_CESM_2040.append(i)


def cesm_2040():
    """
    This function takes all of the files in the datasets_CESM_2040 list and turns the data
    into csv files, which are then stored in the path variable.
    """
    path = r'NETCDF Files csv/CESM-2040-2060/'

    for i in datasets_CESM_2040:
        my_list = i.split('\\')[-1]
        name = my_list.split('_')[0]
        # print(name)
        netcdf_ds = xr.open_dataset(i)
        netcdf_df = netcdf_ds.to_dataframe()
        netcdf_df = netcdf_df.reset_index()
        netcdf_df = netcdf_df.drop(
            columns=['bnds', 'south_north', 'west_east', 'Time_bnds'])
        # print(netcdf_df)
        netcdf_df.to_csv(os.path.join(path, name+'.csv'))


def cesm_1985():
    """
    This function takes all of the files in the datasets_CESM_1985 list and turns the data
    into csv files, which are then stored in the path variable.
    """
    path = r'NETCDF Files csv/CESM-1985-2005/'
    for i in datasets_CESM_1985:
        my_list = i.split('\\')[-1]
        name = my_list.split('_')[0]
        # print(name)
        netcdf_ds = xr.open_dataset(i)
        netcdf_df = netcdf_ds.to_dataframe()
        netcdf_df = netcdf_df.reset_index()
        netcdf_df = netcdf_df.drop(
            columns=['bnds', 'south_north', 'west_east', 'Time_bnds'])
        # print(netcdf_df)
        netcdf_df.to_csv(os.path.join(path, name+'.csv'))


def read_cesm_csvs_2040():
    """
    This function reads the csv files and slices the data daily.
    The sliced data is turned into a csv file and stored into separate folders based
    on the parameter name.
    All of the parameter folders are stored into the folder CESM-2040-2060-daily.
    """
    first_date = datetime.datetime(2040, 1, 1)
    end_date = datetime.datetime(2060, 12, 31)
    days = pd.date_range(start=first_date, end=end_date, freq='D')

    CESM_2040_csvs = glob.glob(
        'NETCDF Files csv/CESM-2040-2060/*.csv', recursive=True)
    source_folder = r'NETCDF Files csv/CESM-2040-2060/CESM-2040-2060-daily/'

    for i in CESM_2040_csvs:
        for d in days:
            file_name = i.split('\\')[-1]
            parameter = file_name.split('.')[0]
            df = pd.read_csv(i)
            df = df.drop(columns=['Unnamed: 0'])
            df = df.reset_index()
            df = df.drop(columns=['index'])
            df['Time'] = df['Time'].astype('datetime64[ns]')
            df = df.loc[df['Time'] == d]
            # dt_object = dt_object.strftime('%Y-%m-%d')
            df.to_csv(os.path.join(source_folder, parameter, 'f{d}.csv'))
            
                       
def read_cesm_csvs_1985():
    """
    This function reads the csv files and slices the data daily.
    The sliced data is turned into a csv file and stored into separate folders based
    on the parameter name.
    All of the parameter folders are stored into the folder CESM-1985-2005-daily. 
    """
    first_date = datetime.datetime(1985, 1, 1)
    end_date = datetime.datetime(2005, 12, 31)
    days = pd.date_range(start=first_date, end=end_date, freq='D')

    CESM_1985_csvs = glob.glob(
        'NETCDF Files csv/CESM-1985-2005/*.csv', recursive=True)
    source_folder = r'NETCDF Files csv/CESM-1985-2005/CESM-1985-2005-daily/'

    for i in CESM_1985_csvs:
        for d in days:
            file_name = i.split('\\')[-1]
            parameter = file_name.split('.')[0]
            df = pd.read_csv(i)
            df = df.drop(columns=['Unnamed: 0'])
            df = df.reset_index()
            df = df.drop(columns=['index'])
            df['Time'] = df['Time'].astype('datetime64[ns]')
            df = df.loc[df['Time'] == d]
            # dt_object = dt_object.strftime('%Y-%m-%d')
            df.to_csv(os.path.join(source_folder, parameter, 'f{d}.csv'))


if __name__ == "__main__":
    # Identify the current year desired.
    year = int(sys.argv[1])
    classify_netcdf_files()
    if year == 2040:
        cesm_2040()
        read_cesm_csvs_2040()
    else:
        cesm_1985()
        read_cesm_csvs_1985()
