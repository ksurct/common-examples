import pymunk.pygame_util
from pymunk import Vec2d
import pygame
import pymunk



class Course():
    def createBlock(self,x,y,sizeX,sizeY,space):
        points = [(0,0), (0, sizeY), (sizeX, sizeY), (sizeX, 0)]
        body = pymunk.Body(1, body_type=pymunk.Body.STATIC)
        body.position = (x,y)
        shape = pymunk.Poly(body, points)
        space.add(body, shape)

    def __init__(self, pixelsX, pixelsY):
        self.yLength = 10
        self.xLength = 10
        # y ^
        # x <->
        self.course = [
            1,1,1,1,1,1,1,1,1,1,
            1,0,1,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,1,
            1,0,1,1,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,1,
            1,1,0,1,0,0,0,0,0,1,
            1,0,0,1,1,1,1,1,1,1,
            1,1,0,1,0,0,0,0,0,1,
            1,0,0,1,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,1,
        ]

        # Size of the boxes
        self.pxSizeX = pixelsX / self.xLength
        self.pxSizeY = pixelsY / self.yLength

    def get(self,x,y):
        return self.course[x + self.xLength * y]

    def createCourse(self, space):
        for x in range(self.xLength):
            for y in range(self.yLength):
                if (self.get(x,y) == 1):
                    self.createBlock(x*self.pxSizeX,y*self.pxSizeY,self.pxSizeX*0.95,self.pxSizeY*0.95,space)

def run():
    pygame.init()
    pxX = 800
    pxY = 800
    display = pygame.display.set_mode((pxX, pxY))
    drawOpt = pymunk.pygame_util.DrawOptions(display)
    clock = pygame.time.Clock()
    space = pymunk.Space()
    course = Course(pxX, pxY)
    FPS = 50
    course.createCourse(space)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # DO stuff


        # pygame.display.update()
        ### Draw space
        space.debug_draw(drawOpt)

        ### All done, lets flip the display
        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

run()
