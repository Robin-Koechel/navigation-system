import pygame
from parse_osm_files import osm_parser
from Highway import Highway
from Building import Building
from Window import Window
p = osm_parser('data_gerlingen.osm')
BBox = p.get_Lat_Lon_Box()
all_Highways = p.get_highway_dicts()
all_HigwaysObjects = []

for highway in all_Highways:
    highwayObject = Highway(highway, p)
    all_HigwaysObjects.append(highwayObject)

#zoom
amountOfLon = 1250/100
differenceOfLon = BBox[1] - BBox[0]
zoom1 = differenceOfLon/amountOfLon

amountOfLat = 738/100
differenceOfLat = BBox[3] - BBox[2]
zoom2 = differenceOfLat/amountOfLat


spielaktiv = True
w = Window(1250,738,0.0005,60)
w.setReferencePoint((BBox[2],  BBox[0]))
bg = pygame.image.load("img_gerlingen.png")


while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    spielaktiv = w.makeEvents(0.000005)

    # Spiellogik hier integrieren

    # Spielfeld löschen
    w.deleteWindow()

    # Spielfeld/figuren zeichnen

    #w.displayImage(bg)
    for highway in all_HigwaysObjects:
        w.drawHighway(highway, 4, (255, 140, 0))



    # Fenster aktualisieren
    w.refreshWindow()

    # Refresh-Zeiten festlegen
    w.tick()

pygame.quit()

print("hello there")