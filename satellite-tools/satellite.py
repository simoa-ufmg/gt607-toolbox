import numpy as np
import cv2
import os
import glob
import pandas as pd
from itertools import product
import affine
from affine import Affine
import pyproj
from pyproj import Transformer
import matplotlib.pyplot as plt
import rasterio
import rasterio.features
import keplergl
import ast
import configparser

paths = configparser.ConfigParser()
paths.read_file(open(r'config.txt'))
sat_img = paths.get('paths', 'sat')
img_list = glob.glob(os.path.join(sat_img, '*.tif'))

img = rasterio.open(img_list[0])
img_left = img.bounds[0]
img_bottom = img.bounds[1]
img_right = img.bounds[2]
img_top = img.bounds[-1]

pixel_transform = affine.Affine(
    -20,
    0,
    img_top,
    0,
    20,
    img_left
)

transformer = Transformer.from_crs(32723, 4326,  always_xy=True)

df_list = []
coords_list = []
cart_list = []


def points():
    for img in img_list:
        im = cv2.imread(img, -1)
        height = range(im.shape[0])
        width = range(im.shape[1])
        im = im.flatten()
        df = pd.DataFrame(im)
        df.columns = ['value']
        df_list.append(df)

        coords = np.array(list(product(height, width)))

        coords_df = pd.DataFrame(coords, columns=['Y', 'X'])

        yy, xx = pixel_transform * (coords_df['Y'], coords_df['X'])

        xx_latlng, yy_latlng = transformer.transform(xx, yy)

        xx_latlng = pd.Series(xx_latlng)
        yy_latlng = pd.Series(yy_latlng)

        xx_yy = pd.concat([xx_latlng, yy_latlng], axis=1)

        xx_yy.columns = ['Longitude', 'Latitude']

        name = img.split('\\')
        name = name[-1]
        name = name.replace('.tif', '')

        xx_yy.name = name
        df.name = name

        cart_list.append(coords_df)

        coords_list.append(xx_yy)


points()

minimal = df_list[0]['value'].min()
path_namer = sat_img
df_namer = glob.glob(os.path.join(path_namer, '*.tif'))

points = []

if os.path.isdir("sat_data"):
    print('Diretório sat_data já existe')
else:
    print('Diretório sat_data criado')
    os.mkdir("sat_data")

for d in df_list:
    print(d.name)
    merge = pd.concat([d, coords_list[0]], axis=1)
    merge_mask = merge[(merge['value'] > minimal)]
    img_band = df_namer[0].replace(path_namer, '')
    img_band = img_band.replace('_20m_Mask_NDWI.tif', '')
    img_band = img_band.replace('\\', '')
    merge_mask.name = img_band
    print(merge_mask.name)
    df_namer.pop(0)
    coords_list.pop(0)
    points.append(merge_mask)

for j in points:
    j.to_csv('sat_data/{}.csv'.format(j.name), index=False)
