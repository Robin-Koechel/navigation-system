import pygame
from parse_osm_files import osm_parser
from Highway import Highway
from Building import Building
from House import House

class Window():
    def __init__(self, width, heigth, zoomx, zoomY, fps):
        self.width = width
        self.heigth = heigth
        self.screen = pygame.display.set_mode((width, heigth))
        #zoom describes how many lat lon i can get in 100 pixels
        self.zoomX = zoomx
        self.zoomY = zoomY

        self.fps = fps
        self.clock = pygame.time.Clock()
        pygame.init()

    def setReferencePoint(self,referencePoint):
        self.referencePoint = referencePoint

    def getReferencePoint(self):
        return self.referencePoint

    def drawBuilding(self, building, radius, color):
        xyCoordinate = building.getXYCoordinate(self.zoomX, self.zoomY, self.width, self.heigth, self.referencePoint)
        latlon = building.get_All_Lat_Lon()
        #font = pygame.font.Font('freesansbold.ttf', 10)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        # create a text surface object,
        # on which text is drawn on it.
        i = 0
        lastpoint = []
        for point in xyCoordinate:

            point[1] = self.heigth - point[1]
            pygame.draw.circle(self.screen, color, point, radius, 4)
            #text = font.render(str(latlon[i]), True, green, blue)
            #self.screen.blit(text, point)
            #i = i + 1

            if lastpoint != []:
                pygame.draw.line(self.screen, green, lastpoint, point)

            lastpoint = point

    def drawHighway(self, highway, radius ,color):
        xyCoordinate = highway.getXYCoordinate(self.zoomX,self.zoomY, self.width, self.heigth, self.referencePoint)
        latlon = highway.get_All_Lat_Lon()
        font = pygame.font.Font('freesansbold.ttf', 10)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        rot = (255, 0, 0)

        # create a text surface object,
        # on which text is drawn on it.
        i = 0
        lastpoint = []
        for point in xyCoordinate:

            point[1] = self.heigth - point[1]
            pygame.draw.circle(self.screen, color, point, radius, 4)
            text = font.render(str(latlon[i]), True, green, blue)
            self.screen.blit(text, point)
            i = i + 1

            if lastpoint != []:
                pygame.draw.line(self.screen, rot, lastpoint, point)

            lastpoint = point




    def deleteWindow(self):
        self.screen.fill(( 255, 255, 255))

    def refreshWindow(self):
        pygame.display.flip()

    def tick(self):
        self.clock.tick(self.fps)


    def refreshReferencepoint(self):
        mouseButtonPressed = pygame.mouse.get_pressed()
        buttonClicked = False
        for button in mouseButtonPressed:
            if button == True:
                movement = pygame.mouse.get_rel()
                print(movement)
                if not(self.firstTime):
                    changeX = (movement[0] / self.width) * ( self.width/100) * ( self.zoomX)
                    x = self.referencePoint[1]-changeX
                    changeY  = (movement[1] / self.heigth) * ( self.heigth/100) * ( self.zoomY)
                    y =  self.referencePoint[0]+changeY
                    self.referencePoint = (y,x)
                    print(self.referencePoint)

                else:
                    self.firstTime = False
                buttonClicked = True



        if not(buttonClicked):
            self.firstTime = True



    def makeEvents(self,difference):
        spielaktiv = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spielaktiv = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    self.zoomX = self.zoomX + difference
                    self.zoomY = self.zoomY + difference

                    print("Spieler hat Taste w gedrückt")
                elif event.key == pygame.K_s:
                    self.zoomX = self.zoomX - difference
                    self.zoomY = self.zoomY - difference
                    print("Spieler hat Taste s gedrückt")
        return spielaktiv

    def displayImage(self,img):
        # INSIDE OF THE GAME LOOP
        self.screen.blit(img, (0, 0))