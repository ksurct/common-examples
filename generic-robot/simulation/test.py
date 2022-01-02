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
    yLength = 8
    xLength = 8
    course = [
        1,1,1,1,1,1,1,1,
        1,0,1,0,0,0,0,1,
        1,0,0,0,0,0,0,1,
        1,0,1,1,0,0,0,1,
        1,0,0,0,0,0,0,1,
        1,1,0,1,0,0,0,1,
        1,0,0,1,1,1,0,1,
        1,1,1,1,1,1,1,1,
    ]
    def createBlock(self,x,y,sizeX,sizeY,space):
        points = [(0,0), (0, sizeY), (sizeX, sizeY), (sizeX, 0)]
        body = pymunk.Body(1, body_type=pymunk.Body.STATIC)
        body.position = (x,y)
        shape = pymunk.Poly(body, points)
        space.add(body, shape)
    def __init__(self, pixelsX, pixelsY):
        self.yLength = Course.yLength
        self.xLength = Course.xLength
        # y ^
        # x <->
        self.course = Course.course

        # Size of the boxes
        self.pxSizeX = pixelsX / self.xLength
        self.pxSizeY = pixelsY / self.yLength

    @staticmethod
    def get(x,y):
        if (x >= Course.xLength or x < 0):
            return 0
        elif (y >= Course.yLength or y < 0):
            return 0
        return Course.course[x + Course.xLength * y]

    def createCourse(self, space):
        for x in range(self.xLength):
            for y in range(self.yLength):
                if (self.get(x,y) == 1):
                    self.createBlock(x*self.pxSizeX,y*self.pxSizeY,self.pxSizeX*0.95,self.pxSizeY*0.95,space)

class RobotSim():
    def __init__(self, location, length, width, timestep, space, display, course):
        self.course = course
        self.display = display
        self.location = location
        self.length = length
        self.width = width
        self.time = 0
        self.timestep = timestep
        self.robotBody = pymunk.Body(1, float("inf"))
        self.robotBody.position = location
        self.robotShape = pymunk.Poly(self.robotBody, [(0,0),(self.width,0),(self.width,self.length),(0,self.length)])
        self.robotShape.sensor = False
        self.robotShape.color = (255, 50, 50, 255)
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

# Stolen from C:
# https://github.com/3DSage/OpenGL-Raycaster_v1/blob/master/3DSage_Raycaster_v1.c
#

    def rayCast(self, xStart,yStart, angle):
        xIter,yIter,xOffset,yOffset,disV,distance = 0,0,0,0,0,0
        color = 0
        colorV = 0
        disV = 100000
        loopX = Course.xLength
        # --- Verticle lines ----
        Tan = tan(angle)
        if (cos(angle)> 0.001):
            xIter=((xStart // self.course.pxSizeX) * self.course.pxSizeX)+self.course.pxSizeX + 0.0001
            yIter=(xStart-xIter)*Tan+yStart
            xOffset= self.course.pxSizeX
            yOffset=-xOffset*Tan
        elif(cos(angle)<-0.001):
            xIter=((xStart//self.course.pxSizeX)*self.course.pxSizeX) - 0.0001
            yIter=(xStart-xIter)*Tan+yStart
            xOffset=-self.course.pxSizeX
            yOffset=-xOffset*Tan
        else:
            xIter=xStart; yIter=yStart
            loopX = 0
        for i in range(loopX):
            mx=int((xIter)//self.course.pxSizeX)
            my=int((yIter)//self.course.pxSizeY)
            if(mx >= 0 and my >= 0 and Course.get(mx,my) != 0):
                disV=cos(angle)*(xIter-xStart)-sin(angle)*(yIter-yStart)
                colorV = Course.get(mx,my)
                break
            else:
                #pygame.draw.circle(self.display, (0,0,255), (xIter,yIter), 3)
                xIter+=xOffset; yIter+=yOffset
        vx = xIter
        vy = yIter

        # --- Horizontal lines ----
        if (Tan == 0):
            Tan = 0.00000001
        Tan = 1/Tan
        if (sin(angle)> 0.001):
            yIter=((yStart//self.course.pxSizeY)*self.course.pxSizeY) - 0.0001
            xIter=(yStart-yIter)*Tan+xStart
            yOffset= -self.course.pxSizeY
            xOffset=-yOffset*Tan
        elif(sin(angle)<-0.001):
            yIter=((yStart // self.course.pxSizeY) * self.course.pxSizeY)+self.course.pxSizeY + 0.0001
            xIter=(yStart-yIter)*Tan+xStart
            yOffset=self.course.pxSizeY
            xOffset=-yOffset*Tan
        else:
            xIter=xStart; yIter=yStart
            return (disV, colorV)
        for i in range(Course.yLength):
            mx=int((xIter)//self.course.pxSizeX)
            my=int((yIter)//self.course.pxSizeY)
            if(mx >= 0 and my >= 0 and Course.get(mx,my) != 0):
                distance=cos(angle)*(xIter-xStart)-sin(angle)*(yIter-yStart)
                color = Course.get(mx,my)
                break
            else:
                #pygame.draw.circle(self.display, (255,0,0), (xIter,yIter), 3)
                xIter+=xOffset; yIter+=yOffset
        xIter; yIter
        if (distance > disV or distance == 0):
            distance = disV
            color = colorV
            xIter = vx
            yIter = vy
        # Draw line from px py to rx ry
        pygame.draw.line(self.display, (0, 255, 0), (xStart, yStart), (xIter, yIter), 1)
        return (distance, color)

    def tick(self):
        self.time += self.timestep
        for i in range(0, 360):
            (distance, color) = self.rayCast(self.robotBody.position[0], self.robotBody.position[1],radians(i) + -self.robotBody.angle + pi/2)
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
    course = Course(pxX, pxY)
    FPS = 50
    course.createCourse(space)
    robot = RobotSim((100,100), 100, 50, 1/FPS, space, display, course)

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
