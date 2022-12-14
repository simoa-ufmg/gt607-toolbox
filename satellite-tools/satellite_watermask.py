import cv2
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import rasterio.features
import rasterio.mask
import configparser
import glob, os

paths = configparser.ConfigParser()
paths.read_file(open(r'config.txt'))
mask = paths.get('paths', 'mask')
img_list = paths.get('paths', 'img_list')




img = rasterio.open(mask).read(1)
img = img.astype(float)
img = img / 2 ** 16
img_normalized = (img - img.min()) / (img.max() - img.min())
img_normalized = 1 - img_normalized
img_normalized = img_normalized ** 8
img_normalized = np.round(img_normalized)
img_normalized_uint8 = img_normalized.astype('uint8')


nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img_normalized_uint8, connectivity=8)
sizes = stats[1:, -1]; nb_components = nb_components - 1

min_size = 250

img2 = np.zeros((output.shape))
for i in range(0, nb_components):
    if sizes[i] >= min_size:
        img2[output == i + 1] = 255

matriz = np.zeros([img2.shape[0], img2.shape[1], 3])
matriz[:,:,0] = img2 
matriz[:,:,1] = img2
matriz[:,:,2] = img2
matriz = matriz.astype('uint8')

r,g,b = cv2.split(matriz)
img_bgr = cv2.merge([b,g,r])
kernel = np.ones((5,5), np.uint8)  
img_dilate = cv2.dilate(img_bgr, kernel, iterations=1)  

img_dilate_1C = cv2.cvtColor(img_dilate, cv2.COLOR_BGR2GRAY)
np.unique(img_dilate_1C)
img_dilate_1C = img_dilate_1C.astype(float)
mask_1C_dilate = img_dilate_1C.copy()
mask_1C_dilate[img_dilate_1C == 0.0] = 'nan'

img_list = glob.glob(os.path.join(img_list , '*.tif'))
masked_imgs = []
names = []
    
def apply_mask():
    for image in img_list:
        namer = image.split('\\')
        split_namer = namer[-1].split('_')
        name = 'masked_' + split_namer[-1]
        final_name = image.replace(split_namer[-1], name)
        final_name = final_name.split('\\')
        final_name = final_name[-1]
        final_name = final_name[:-4]
        band = rasterio.open(image).read(1)
        if band.shape != mask_1C_dilate.shape:
            band  = cv2.imread(image, -1)
            img_half = cv2.resize(band, (0, 0), fx=0.5, fy=0.5)
            mask_band = np.where(np.isnan(mask_1C_dilate), np.nan, img_half)
        else:
            mask_band = np.where(np.isnan(mask_1C_dilate), np.nan, band)
        masked_imgs.append(mask_band)
        names.append(final_name)
apply_mask()

fig = plt.figure(figsize=(40, 10))
columns = 5
rows = 2

ax = []
j = 0
for i in range(columns*rows):
    ax.append( fig.add_subplot(rows, columns, i+1) )
    ax[-1].set_title(names[j][-3:])  # set title
    plt.imshow(masked_imgs[j])
    plt.colorbar()
    j +=1

plt.show()
