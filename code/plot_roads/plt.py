from bs4 import BeautifulSoup as bs # parsing the data
from matplotlib import pyplot as plt
from matplotlib import image
import math
import numpy as np

background_img = image.imread('img_gerlingen.png')

with open('data_gerlingen.osm', 'r') as f:
    data = f.read()
R = 6378137

bs_data = bs(data, 'xml')

b_bound = bs_data.find('bounds')
b_node = bs_data.find_all('node')

lst_coordinates = []

for n in b_node:
    lat = float(n.get('lat'))
    lon = float(n.get('lon'))
    lst_coordinates.append([lat, lon])


x_data=[]
y_data=[]
z_data=[]
for c in lst_coordinates:
    x = R * math.cos(c[0]) * math.sin(c[1])
    y = R * math.sin(c[0]) * math.sin(c[1])
    z = R * math.cos(c[0])

    x_data.append(x)
    y_data.append(y)
    z_data.append(z)


def plot_3d_sphere():
    ax = plt.axes(projection='3d')
    #ax.set_aspect("auto")

    # generates the values of every line
    lat, lon = np.mgrid[0:2 * np.pi:15j, 0:np.pi:15j] # https://numpy.org/doc/stable/reference/generated/numpy.mgrid.html

    # convert lan & lon to x, y,z
    x = np.cos(lat) * np.sin(lon) * R
    y = np.sin(lat) * np.sin(lon) * R
    z = np.cos(lon) * R

    #ax.plot_surface(x, y, z, cmap='plasma')
    ax.plot_wireframe(x, y, z, color='k')
    ax.scatter3D(x_data, y_data, z_data, color="r")

plot_3d_sphere()

plt.show()