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
        pygame.init()

    def setReferencePoint(self,referencePoint):
        self.referencePoint = referencePoint

    def getReferencePoint(self):
        return self.referencePoint

    def drawHighway(self, highway, radius ,color):
        xyCoordinate = highway.getXYCoordinate(self.zoom, self.width, self.heigth, self.referencePoint)
        latlon = highway.get_All_Lat_Lon()
        font = pygame.font.Font('freesansbold.ttf', 10)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        # create a text surface object,
        # on which text is drawn on it.
        i = 0
        for point in xyCoordinate:
            point[1] = self.heigth-point[1]
            pygame.draw.circle(self.screen, color, point, radius,4)
            text = font.render(str(latlon[i]), True, green, blue)
            self.screen.blit(text,point)
            i = i+1

    def deleteWindow(self):
        self.screen.fill(( 255, 255, 255))

    def refreshWindow(self):
        pygame.display.flip()

    def tick(self):
        self.clock.tick(self.fps)

    def zooming(self, difference):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    self.zoom = self.zoom + difference
                    print("Spieler hat Taste w gedrückt")
                elif event.key == pygame.K_s:
                    self.zoom = self.zoom - difference
                    print("Spieler hat Taste s gedrückt")


    def makeEvents(self,difference):
        spielaktiv = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spielaktiv = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    self.zoom = self.zoom + difference
                    print("Spieler hat Taste w gedrückt")
                elif event.key == pygame.K_s:
                    self.zoom = self.zoom - difference
                    print("Spieler hat Taste s gedrückt")
        return spielaktiv

    def displayImage(self,img):
        # INSIDE OF THE GAME LOOP
        self.screen.blit(img, (0, 0))