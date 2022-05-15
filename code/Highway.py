import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup as bs # parsing the data
from matplotlib import pyplot as plt
from matplotlib import image
import math
from parse_osm_files import osm_parser

class Highway():

    def __init__(self, highway_Data, osm_parser):
        self.nodes = osm_parser.get_highway_nodes(highway_Data['id'])
        self.lit = highway_Data['lit']
        self.maxspeed = highway_Data['maxspeed']
        self.name = highway_Data['name']
        self.surface = highway_Data['surface']

    def get_All_Lat_Lon(self):

        return self.nodes

    def get_Lit(self):
        return self.lit

    def get_Maxspeed(self):
        return self.maxspeed

    def get_Name(self):
        return self.name

    def get_Surface(self):
        return self.surface

    def getXYCoordinate(self, zoomX,zoomY, width, heigth, referencePoint):
        lst_coordinates = []

        for point in self.nodes:
           # is the point in the window
           isThePointDrawable = True
           differenceLon = point[1] - referencePoint[1]
           differenceLat = point[0] - referencePoint[0]

           if differenceLat < 0 or differenceLon < 0:
               isThePointDrawable = False
           amountOfLon = width / 100 * zoomX
           amountOfLat = heigth / 100 * zoomY

           if amountOfLat < differenceLat or amountOfLon < differenceLon:
               isThePointDrawable = False

           if isThePointDrawable:
               # get x
               xRatio = differenceLon / amountOfLon
               xCoordinate = xRatio * width

               # get y
               yRatio = differenceLat / amountOfLat
               yCoordinate = yRatio * heigth
               lst_coordinates.append([xCoordinate, yCoordinate])





        return lst_coordinates


    @staticmethod
    def get_DF_For_All_Highays(allHighways):

        lst_coordinates = allHighways[0].get_All_Lat_Lon()
        first = True
        for highway in allHighways:
            if not(first):
                lst_coordinates = np.concatenate((lst_coordinates, highway.get_All_Lat_Lon()))
            first = False
        columm_values = ['lat', 'lon']
        df = pd.DataFrame(data=lst_coordinates, columns=columm_values)
        return df




if __name__ == "__main__":

    background_img = plt.imread('img_gerlingen.png')

    p = osm_parser('data_gerlingen.osm')
    BBox = p.get_Lat_Lon_Box()
    all_Highways = p.get_highway_dicts()
    all_HigwaysObjects = []

    for highway in all_Highways:
        highwayObject = Highway(highway, p)
        all_HigwaysObjects.append(highwayObject)

    fig, ax = plt.subplots(figsize=(9, 7))
    df = Highway.get_DF_For_All_Highays(all_HigwaysObjects)
    print(df)

    ax.scatter(df.lon, df.lat, zorder=1, alpha=0.65, c='r', s=10)

    ax.set_title('Plotting Spatial Data on Riyadh Map')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    print(BBox)
    ax.imshow(background_img, zorder=0, extent=BBox, aspect='equal')
    plt.show()

