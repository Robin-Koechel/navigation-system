from Building import Building
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup as bs # parsing the data
from matplotlib import pyplot as plt
from matplotlib import image
import math
from parse_osm_files import osm_parser

class House(Building):
    def __init__(self,building_Data, osm_parser):
        Building.__init__(self,building_Data,osm_parser)
        #self.city = building_Data['addr:city']
        #self.country = building_Data['addr:country']
        #self.housenumber = building_Data['addr:housenumber']
        #self.postcode = building_Data['addr:postcode']
        #self.street = building_Data['addr:street']

    def get_City(self):
        return self.city

    def get_Country(self):
        return self.country

    def get_Housenumber(self):
        return self.housenumber

    def get_Postcode(self):
        return self.postcode

    def get_Street(self):
        return self.street

if __name__ == "__main__":

    background_img = plt.imread('img_gerlingen.png')

    p = osm_parser('data_gerlingen.osm')
    BBox = p.get_Lat_Lon_Box()
    all_Buildings = p.get_Building_dicts()
    all_BuildingsObjects = []

    for building in all_Buildings:
        buildingObject = House(building, p)
        all_BuildingsObjects.append(buildingObject)



    fig, ax = plt.subplots(figsize=(9, 7))
    df = Building.get_DF_For_All_Buildings(all_BuildingsObjects)
    print(df)

    ax.scatter(df.lon, df.lat, zorder=1, alpha=0.65, c='r', s=10)

    ax.set_title('Plotting Spatial Data on Riyadh Map')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    print(BBox)
    ax.imshow(background_img, zorder=0, extent=BBox, aspect='equal')
    plt.show()