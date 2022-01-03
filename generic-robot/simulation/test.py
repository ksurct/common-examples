import pymunk.pygame_util
from pymunk import Vec2d
import pygame
import pymunk
from math import *


collisionTypes = {
    "wall": 0,
    "sensor": 1,
    "robot": 2
}

class Course():
    def createBlock(self,x,y,sizeX,sizeY,space, color):
        points = [(0,0), (0, sizeY), (sizeX, sizeY), (sizeX, 0)]
        body = pymunk.Body(1, body_type=pymunk.Body.STATIC)
        body.position = (x,y)
        shape = pymunk.Poly(body, points)
        shape.color = color
        space.add(body, shape)
    def __init__(self, pixelsX, pixelsY, xLength, yLength, display = None):
        self.display = display
        self.yLength = yLength
        self.xLength = xLength
        self.course = [0]*(xLength*yLength)
        # Size of the boxes
        self.pxSizeX = pixelsX / self.xLength
        self.pxSizeY = pixelsY / self.yLength

    def setCourse(self, course):
        self.course = course
    
    def circle(self, x, y, radius, color):
        for i in range(0,360):
            self.set(cos(radians(i))*radius + x, sin(radians(i))*radius + y, color)

    def line(self, x1,y1,x2,y2, color):
        slope = 1000 
        if x2 != x1:
            slope = (y2 - y1) / (x2 - x1)
        if (slope < 1):
            # Draw over horizontal
            # mx + b
            # y = slope * (x - x1) + y1
            for x in range(x1,x2):
                y = slope * (x - x1) + y1
                self.set(x,y,color)
        else:
            # Verticle
            slope = (x2 - x1) / (y2 - y1)
            for y in range(y1,y2):
                x = slope * (y - y1) + x1
                self.set(x,y,color)

    # Stolen from C:
    # https://github.com/3DSage/OpenGL-Raycaster_v1/blob/master/3DSage_Raycaster_v1.c
    #
    def rayCast(self, xStart,yStart, angle):
        xIter,yIter,xOffset,yOffset,disV,distance = 0,0,0,0,0,0
        color = 0
        colorV = 0
        disV = 100000
        loopX = self.xLength
        # --- Verticle lines ----
        Tan = tan(angle)
        if (cos(angle)> 0.001):
            xIter=((xStart // self.pxSizeX) * self.pxSizeX)+self.pxSizeX + 0.0001
            yIter=(xStart-xIter)*Tan+yStart
            xOffset= self.pxSizeX
            yOffset=-xOffset*Tan
        elif(cos(angle)<-0.001):
            xIter=((xStart//self.pxSizeX)*self.pxSizeX) - 0.0001
            yIter=(xStart-xIter)*Tan+yStart
            xOffset=-self.pxSizeX
            yOffset=-xOffset*Tan
        else:
            xIter=xStart; yIter=yStart
            loopX = 0
        for i in range(loopX):
            mx=int((xIter)//self.pxSizeX)
            my=int((yIter)//self.pxSizeY)
            if(mx >= 0 and my >= 0 and self.get(mx,my) != 0):
                disV=cos(angle)*(xIter-xStart)-sin(angle)*(yIter-yStart)
                colorV = self.get(mx,my)
                break
            else:
                xIter+=xOffset; yIter+=yOffset
        vx = xIter
        vy = yIter

        # --- Horizontal lines ----
        if (Tan == 0):
            Tan = 0.00000001
        Tan = 1/Tan
        if (sin(angle)> 0.001):
            yIter=((yStart//self.pxSizeY)*self.pxSizeY) - 0.0001
            xIter=(yStart-yIter)*Tan+xStart
            yOffset= -self.pxSizeY
            xOffset=-yOffset*Tan
        elif(sin(angle)<-0.001):
            yIter=((yStart // self.pxSizeY) * self.pxSizeY)+self.pxSizeY + 0.0001
            xIter=(yStart-yIter)*Tan+xStart
            yOffset=self.pxSizeY
            xOffset=-yOffset*Tan
        else:
            xIter=xStart; yIter=yStart
            return (disV, colorV)
        for i in range(self.yLength):
            mx=int((xIter)//self.pxSizeX)
            my=int((yIter)//self.pxSizeY)
            if(mx >= 0 and my >= 0 and self.get(mx,my) != 0):
                distance=cos(angle)*(xIter-xStart)-sin(angle)*(yIter-yStart)
                color = self.get(mx,my)
                break
            else:
                xIter+=xOffset; yIter+=yOffset
        xIter; yIter
        if (distance > disV or distance == 0):
            distance = disV
            color = colorV
            xIter = vx
            yIter = vy
        # Draw line from px py to rx ry
        if (self.display != None):
            pygame.draw.line(self.display, color, (xStart, yStart), (xIter, yIter), 1)
        return (distance, color)

    def get(self,x,y):
        if (x >= self.xLength or x < 0):
            return 0
        elif (y >= self.yLength or y < 0):
            return 0
        return self.course[int(x + self.xLength * y)]

    def set(self,x,y, color):
        if (x >= self.xLength or x < 0):
            return
        elif (y >= self.yLength or y < 0):
            return
        self.course[int(x + self.xLength * y)] = color

    def createOuterWalls(self, color):
        self.line(0,0,0,self.yLength, color)
        self.line(self.xLength - 1,0,self.xLength - 1,self.yLength, color)
        self.line(0,0,self.xLength,0, color)
        self.line(0,self.yLength - 1,self.xLength,self.yLength - 1, color)

    def createCourse(self, space):
        for x in range(self.xLength):
            for y in range(self.yLength):
                get = self.get(x,y)
                if (get != 0):
                    self.createBlock(x*self.pxSizeX,y*self.pxSizeY,self.pxSizeX*0.95,self.pxSizeY*0.95,space, get)

class RobotSim():
    def __init__(self, location, length, width, timestep, space, course):
        self.course = course
        self.location = location
        self.length = length
        self.width = width
        self.time = 0
        self.timestep = timestep
        self.robotBody = pymunk.Body(1, float("inf"))
        self.robotBody.position = location
        self.robotShape = pymunk.Poly(self.robotBody, [(0,0),(self.width,0),(self.width,self.length),(0,self.length)])
        self.robotShape.sensor = False
        self.robotShape.color = (100, 100, 100, 255)
        self.robotShape.collision_type = collisionTypes["robot"]
        self.robotShape.density = 0.5
        self.endTime = 0
        space.add(self.robotBody, self.robotShape)
        self.stopped = True

    # meters per second
    def move(self, meters, speed):
        self.stop()
        self.robotBody.velocity = (speed * Vec2d(0, 1)).rotated(self.robotBody.angle)
        self.endTime = meters / abs(speed) + self.time
        print("Starting at ", self.time, " ending at ", self.endTime)
        self.stopped = False

    def rotate(self, degrees, degreesPerSecond):
        self.stop()
        # convert to rad
        degrees = degrees * (3.1415 / 180)
        degreesPerSecond = degreesPerSecond * (3.1415 / 180)
        self.robotBody.angular_velocity = degreesPerSecond
        self.endTime = degrees / abs(degreesPerSecond) + self.time
        print("Starting at ", self.time, " ending at ", self.endTime)
        self.stopped = False

    def stop(self):
        self.robotBody.angular_velocity = 0
        self.robotBody.velocity = 0,0
        self.stopped = True

    def tick(self):
        self.time += self.timestep
        for i in range(-20, 20):
            self.course.rayCast(self.robotBody.position[0], self.robotBody.position[1],radians(i) + -self.robotBody.angle + pi/2)
        if (not self.stopped and self.endTime <= self.time):
            print("Stopped at ", self.time)
            self.stop()

def run():
    pygame.init()
    pxX = 800
    pxY = 800
    display = pygame.display.set_mode((pxX, pxY))
    drawOpt = pymunk.pygame_util.DrawOptions(display)
    clock = pygame.time.Clock()
    space = pymunk.Space()
    course = Course(pxX, pxY, 20, 20, display)
    course.createOuterWalls((255, 255, 255, 255))
    course.circle(10,10, 3, (0,0,255,255))
    FPS = 50
    course.createCourse(space)
    robot = RobotSim((100,100), 100, 50, 1/FPS, space, course)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                robot.rotate(90, -45)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                robot.move(100, -50)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                robot.move(100, 50)
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                robot.rotate(90, 45)
        # DO stuff


        # pygame.display.update()
        ### Draw space
        display.fill(pygame.Color("black"))
        space.debug_draw(drawOpt)

        ### All done, lets flip the display
        robot.tick()
        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

run()
