import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup as bs # parsing the data
from matplotlib import pyplot as plt
from matplotlib import image
import math
background_img  = plt.imread('img_gerlingen.png')

with open('data_gerlingen.osm', 'r') as f:
    data = f.read()
R = 6378137

bs_data = bs(data, 'xml')

b_bound = bs_data.find('bounds')
b_node = bs_data.find_all('node')

lst_coordinates = []

min_lat = float(b_bound.get('minlat'))
min_lon = float(b_bound.get('minlon'))
max_lat = float(b_bound.get('maxlat'))
max_lon = float(b_bound.get('maxlon'))

for n in b_node:
    lat = float(n.get('lat'))
    lon = float(n.get('lon'))
    lst_coordinates.append([lat, lon])


fig, ax = plt.subplots(figsize = (8,7))
columm_values = ['lat', 'lon']
df = pd.DataFrame(data = lst_coordinates, columns=columm_values)
BBox = (min_lon,  max_lon,
         min_lat, max_lat)
ax.scatter(df.lon, df.lat, zorder=1, alpha= 0.65, c='b', s=10)
ax.set_title('Plotting Spatial Data on Riyadh Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(background_img, zorder=0, extent = BBox, aspect= 'equal')








#plt.imshow(background_img)
plt.show()