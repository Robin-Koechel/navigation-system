import pygame
from parse_osm_files import osm_parser
from Highway import Highway
from Building import Building


class Window():
    def __init__(self, width, heigth, zoom, fps):
        self.width = width
        self.heigth = heigth
        self.screen = pygame.display.set_mode((width, heigth))
        #zoom describes how many lat lon i can get in 100 pixels
        self.zoom = zoom
        self.fps = fps
        self.clock = pygame.time.Clock()

    def setReferencePoint(self,referencePoint):
        self.referencePoint = referencePoint

    def getReferencePoint(self):
        return self.referencePoint

    def drawHighway(self, highway, radius ,color):
        xyCoordinate = highway.getXYCoordinate(self.zoom, self.width, self.heigth, self.referencePoint)
        for point in xyCoordinate:
            pygame.draw.circle(self.screen, color, point, radius,4)

    def deleteWindow(self):
        self.screen.fill(( 255, 255, 255))

    def refreshWindow(self):
        pygame.display.flip()

    def tick(self):
        self.clock.tick(self.fps)


    def getDeleteEvent(self):
        spielaktiv = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spielaktiv = False
        return spielaktiv

    def displayImage(self,img):
        # INSIDE OF THE GAME LOOP
        self.screen.blit(img, (0, 0))