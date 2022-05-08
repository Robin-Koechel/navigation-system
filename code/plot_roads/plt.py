from bs4 import BeautifulSoup as bs # parsing the data
from matplotlib import pyplot as plt
from matplotlib import image
import math

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


min_x = R * math.cos(min_lat) * math.cos(min_lon)
min_y = R * math.cos(min_lat) * math.sin(min_lon)
min_z = R * math.sin(min_lat)


for c in lst_coordinates:
    x = R * math.cos(c[0]) * math.cos(c[1])
    y = R * math.cos(c[0]) * math.sin(c[1])
    z = R * math.sin(c[0])
    print(x, y, z)

    x = x - min_x
    y = y - min_y
    z = z - min_z

    #plt.plot(x/1250, y/738, 'ro')

plt.imshow(background_img)
plt.show()