import pandas as pd
import numpy as np
import math
import configparser


paths = configparser.ConfigParser()
paths.read_file(open(r'paths.txt'))
field = paths.get('paths', 'field')
field_name = field.split('\\')



#preparing drone photos

def data_merger(medians, metadata, probe, merge):
    medians = pd.read_csv(medians)
    metadata = pd.read_csv(metadata, parse_dates=['DateTime'], infer_datetime_format= True)
    field_data = pd.concat([metadata, medians], axis=1)
    #field_data = field_data.dropna()
    field_data['DateTime'] = pd.to_datetime(field_data['DateTime'], format = '%Y:%m:%d %H:%M:%S')
    field_data['DateTime'] = field_data['DateTime'].dt.date
    field_data = field_data.rename(columns ={'Latitude':'lat_d', 'Longitude':'long_d'})
    field_data.DateTime = pd.to_datetime(field_data.DateTime)
    print(field_data.DateTime.unique())
    #field_data.long_d = field_data.long_d * -1

    #preparing probe data
    probe = pd.read_excel(probe)
    
    probe['date'] = pd.to_datetime(probe['date'], format = '%Y-%d-%m %H:%M:%S') #Funciona para a pampulha new general table
    
    #probe['date'] = pd.to_datetime(probe['date'], format='%d-%m-%Y') #funciona para tres marias general table


    #probe['date'] = pd.to_datetime(probe['date'], format = '%Y-%d-%m %H:%M:%S', exact=False) # funciona para pamps

    probe = probe.rename(columns={'lat':'lat_p', 'lon':'long_p'})
    probe['id'] = probe.index + 1






    #probe['date'] = pd.to_datetime(probe['date'])
    #probe['date'] = probe['date'].dt.date



    print('-------------------------------------------------------------------------------------------')


    #merging data based on date
    merged_data = pd.merge(left = field_data, left_on = 'DateTime', right = probe, 
                            right_on = 'date') #Dataframes merged on same date

    #function to  calculate distances
    def haversine_meters(lat1, long1, lat2, long2):
        dLat = np.radians(lat2-lat1)
        dLong = np.radians(long2-long1)

        lat1 = np.radians(lat1)
        lat2 = np.radians(lat2)

        a = np.sin(dLat/2) * np.sin(dLat/2) + np.sin(dLong/2) * np.sin(dLong/2) * np.cos(lat1) * np.cos(lat2)
        
        m = 2 * math.atan2(np.sqrt(a), np.sqrt(1-a))
        return m * 6371 * 1000



    # =============================================================================
    # merged_data = merged_data.drop_duplicates(subset=['Image Index'], ignore_index=True)
    # 
    # =============================================================================

    #calculating distance between drone img and probe data
    merged_data['Distance'] = [haversine_meters(long1 = merged_data.long_p[i], lat1 = merged_data.lat_p[i],long2 = merged_data.long_d[i], lat2 = merged_data.lat_d[i]) for i in range(len(merged_data))]
    merged_data['Distance'] = merged_data['Distance'].round(decimals=3)
    merge_mask = merged_data[(merged_data.Distance <= 100)]
    print(merge_mask.Distance)
    #writing info to excel file
    merge_mask.to_csv(merge)

metadata = 'field_data_' + field_name[-1] + '/metadata.csv'
medians_10 = 'field_data_' + field_name[-1] + '/chl_algo_reflectance_10.csv'
medians_20 = 'field_data_' + field_name[-1] + '/chl_algo_reflectance_20.csv'
medians_30 = 'field_data_' + field_name[-1] + '/chl_algo_reflectance_30.csv'
medians_40 = 'field_data_' + field_name[-1] + '/chl_algo_reflectance_40.csv'
medians_50 = 'field_data_' + field_name[-1] + '/chl_algo_reflectance_50.csv'
medians_60 = 'field_data_' + field_name[-1] + '/chl_algo_reflectance_60.csv'
probe = 'field_data_' + field_name[-1] + '/Campo Pampulha Mar-Abr-Mai.xlsx'
data_merger(medians_10, metadata, probe, 'field_data_' + field_name[-1] + '/drone_probe_10.csv')
data_merger(medians_20, metadata, probe, 'field_data_' + field_name[-1] + '/drone_probe_20.csv')
data_merger(medians_30, metadata, probe, 'field_data_' + field_name[-1] + '/drone_probe_30.csv')
data_merger(medians_40, metadata, probe, 'field_data_' + field_name[-1] + '/drone_probe_40.csv')
data_merger(medians_50, metadata, probe, 'field_data_' + field_name[-1] + '/drone_probe_50.csv')
data_merger(medians_60, metadata, probe, 'field_data_' + field_name[-1] + '/drone_probe_60.csv')
