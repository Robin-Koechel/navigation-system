import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup as bs # parsing the data
from matplotlib import pyplot as plt
from matplotlib import image
import math
from parse_osm_files import osm_parser#

class Building():
    def __init__(self, building_Data, osm_parser):
        self.nodes = osm_parser.get_Building_nodes(building_Data['id'])
        self.city = building_Data['addr:city']
        self.country = building_Data['addr:country']
        self.housenumber = building_Data['addr:housenumber']
        self.postcode = building_Data['addr:postcode']
        self.street = building_Data['addr:street']

    def get_All_Lat_Lon(self):
        return self.nodes

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

    @staticmethod
    def get_DF_For_All_Buildings(allBuildings):

        lst_coordinates = allBuildings[0].get_All_Lat_Lon()
        first = True
        for building in allBuildings:
            if not (first):
                lst_coordinates = np.concatenate((lst_coordinates, building.get_All_Lat_Lon()))
            first = False
        columm_values = ['lat', 'lon']
        df = pd.DataFrame(data=lst_coordinates, columns=columm_values)
        return df




if __name__ == "__main__":

    background_img = plt.imread('img_gerlingen.png')

    p = osm_parser('data_gerlingen.osm')
    BBox = p.get_Lat_Lon_Box()
    all_Buildings = p.get_Building_dicts()
    all_BuildingsObjects = []

    for building in all_Buildings:
        buildingObject = Building(building, p)
        all_BuildingsObjects.append(buildingObject)

    fig, ax = plt.subplots(figsize=(9, 7))
    df = Building.get_DF_For_All_Highays(all_BuildingsObjects)
    print(df)

    ax.scatter(df.lon, df.lat, zorder=1, alpha=0.65, c='r', s=10)

    ax.set_title('Plotting Spatial Data on Riyadh Map')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    print(BBox)
    ax.imshow(background_img, zorder=0, extent=BBox, aspect='equal')
    plt.show()




















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