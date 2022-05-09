import re
import numpy as np
import numpy
from bs4 import BeautifulSoup as bs # parsing the data

from matplotlib import image
from matplotlib import pyplot as plt
background_img = image.imread('img_gerlingen.png')

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

length = 600
width = 600




data = image.imread('weiß.png')

for c in lst_coordinates:
    x2 = c[0] - min_lat
    y2 = c[1]-min_lon

    plt.plot(x2,y2, marker='v', color="black")


#x = [200, 500]
#y = [300, 100]
#plt.plot(x, y, color="black", linewidth=3)
plt.imshow(data)
plt.show()
