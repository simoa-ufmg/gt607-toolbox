import pandas as pd
import keplergl
import configparser
import ast
import glob

# + tags=["parameters"]
upstream= ['chl_algo', 'extract_metadata']

global df, kivu, kab_1, sabi, ndci, ndvi, bda_1, bda_2, bda_31, gb1, gr, kepler_map

# config = configparser.ConfigParser()
# config.read_file(open(r'map_config.txt'))
# map_config = config.get('map_config', 'map_config')
# map_config = ast.literal_eval(map_config)

# paths = configparser.ConfigParser()
# paths.read_file(open(r'paths.txt'))
# field = paths.get('paths', 'field')
# field_name = field.split('\\')


def map_builder(metadata, chl_algo):
    global df, kivu, kab_1, sabi, ndci, ndvi, bda_1, bda_2, bda_31, bda_mod , gb1,b3b1 , gr

    metadata = pd.read_csv(metadata)
    




    chl_algo = pd.read_csv(chl_algo)
        



    kivu = pd.concat([metadata, chl_algo['KIVU']], axis=1)
    #kivu.drop(kivu.columns[[5, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]], axis=1, inplace=True)
    print(len(kivu))

    kab_1 = pd.concat([metadata, chl_algo['Kab 1(Rs)']], axis = 1)
    #kab_1.drop(kab_1.columns[[5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]], axis=1, inplace=True)

    sabi = pd.concat([metadata, chl_algo['SABI']], axis = 1)
    #sabi.drop(sabi.columns[[5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21]], axis=1, inplace=True)


    ndci = pd.concat([metadata, chl_algo['NDCI']], axis = 1)
    #ndci.drop(ndci.columns[[5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21]], axis=1, inplace=True)

    ndvi = pd.concat([metadata, chl_algo['NDVI']], axis = 1)
    #ndvi.drop(ndvi.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21]], axis = 1, inplace=True)

    bda_1 = pd.concat([metadata, chl_algo['2BDA_1']], axis = 1)
    #bda_1.drop(bda_1.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21]], axis = 1, inplace=True)

    bda_2 = pd.concat([metadata, chl_algo['2BDA_2']], axis = 1)
    #bda_2.drop(bda_2.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21]], axis = 1, inplace = True)

    bda_31 = pd.concat([metadata, chl_algo['3BDA_1']], axis = 1)
    #bda_31.drop(bda_31.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21]], axis = 1, inplace = True)

    bda_mod = pd.concat([metadata, chl_algo['3BDA_MOD']], axis = 1)
 
    #bda_mod.drop(bda_mod.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 16, 19, 20, 21]], axis = 1, inplace = True)

    b3b1 = pd.concat([metadata, chl_algo['B3B1']], axis = 1)
    #b3b1.drop(b3b1.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21]], axis=1, inplace = True)

    gb1 = pd.concat([metadata, chl_algo['GB1']], axis = 1)
    #gb1.drop(gb1.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21]], axis=1, inplace = True)
    
    gr = pd.concat([metadata, chl_algo['GR']], axis = 1)
    #gr.drop(gr.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]], axis=1, inplace = True)

    
def df_builder():
    global df
    df = pd.DataFrame()
    df = pd.concat([kivu, sabi, ndci, ndvi, bda_1, bda_2, bda_31, bda_mod, b3b1, gb1, gr], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df



def add_data_map(kivu, kivu_name, sabi, sabi_name , ndci, ndci_name , ndvi,ndvi_name, bda_1, bda_1_name, bda_2,bda_2_name , bda_31,bda_31_name, bda_mod,bda_mod_name, b3b1,b3b1_name, gb1,gb1_name, gr, gr_name):
    kepler_map.add_data(data=kivu, name=kivu_name)
    kepler_map.add_data(data= sabi, name= sabi_name)
    kepler_map.add_data(data= ndci, name= ndci_name)
    kepler_map.add_data(data= ndvi, name= ndvi_name)
    kepler_map.add_data(data= bda_1, name= bda_1_name)
    kepler_map.add_data(data= bda_2, name= bda_2_name)
    kepler_map.add_data(data= bda_31, name= bda_31_name)
    kepler_map.add_data(data= bda_mod, name= bda_mod_name)
    kepler_map.add_data(data= b3b1, name= b3b1_name)
    kepler_map.add_data(data= gb1, name= gb1_name)
    kepler_map.add_data(data= gr, name= gr_name)





#metadata = 'data_' + field_name[-1] + '/metadata.csv'
#chl_algo = 'data_' + field_name[-1] + '/chl_algo_reflectance_60.csv'

def fields():
    global kepler_map
    config = configparser.ConfigParser()
    config.read_file(open(r'map_config.txt'))
    map_config = config.get('map_config', 'map_config')
    map_config = ast.literal_eval(map_config)
    
    kepler_map = keplergl.KeplerGl(height=1000, config= map_config)    
    field_data = glob.glob('field_data_*')
    print(field_data)
    df_list = []
    for i in field_data:
        print(i)
        chl_algo = i + '/chl_algo_reflectance_60.csv'
        metadata = i + '/metadata.csv'
        map_builder(metadata, chl_algo)
        data = df_builder()
        df_list.append(data)
        #add_data(kivu,'KIVU_' + i, sabi,'SABI_' + i, ndci,'NDCI_' + i, ndvi,'NDVI_' + i, bda_1,'BDA 1_' + i, bda_2,'BDA 2_' + i, bda_31,'BDA 3 1_' + i, bda_mod,'BDA MOD_' + i, b3b1,'B3B1_' + i, gb1,'GB1_' + i, gr, 'GR_' + i)
    all_data = pd.concat(df_list)
    all_data['DateTime'] = pd.to_datetime(all_data['DateTime'], format = '%Y:%m:%d %H:%M:%S')
    all_data["DateTime"] =  all_data["DateTime"].astype(str)
    #all_data.iloc[-1] = ['0', '0', '0', '2059:06:07 14:22:31', 'IMG_FakeTime', '0','0','0','0','0','0','0','0','0','0']

    #all_data = all_data.dropna()

    add_data_map(all_data,'KIVU', all_data,'SABI' , all_data,'NDCI', all_data,'NDVI', all_data,'2BDA_1', all_data,'2BDA_2', all_data,'3BDA_1', all_data,'3BDA_MOD', all_data,'B3B1', all_data,'GB1', all_data, 'GR')
    kepler_map.save_to_html(file_name = 'map.html')


#kepler_map.save_to_html(file_name = 'data_' + field_name[-1] + '/map.html')


#map_builder(metadata, chl_algo)



# -
