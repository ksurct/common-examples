import pymunk.pygame_util
from pymunk import Vec2d
import pygame
import pymunk
from math import *

class RobotSim():
    def __init__(self,
        location,
        length,
        width,
        algorithm=None,
        sensors=None,
        cameras=None
        ):
        self.length = length
        self.width = width
        self.cameras = cameras
        self.sensors = sensors
        self.algorithm = algorithm
        self.time = 0
        self.timestep = 0
        self.robotBody = pymunk.Body(1, float("inf"))
        self.robotBody.position = location
        self.robotShape = pymunk.Poly(self.robotBody, [(0,0),(self.width,0),(self.width,self.length),(0,self.length)])
        self.robotShape.sensor = False
        self.robotShape.color = (255, 100, 100, 100)
        self.robotShape.density = 0.5
        self.endTime = 0
        self.stopped = True

    def _setCourse(self, course):
        self.course = course
    
    def _initPhysics(self, space):
        space.add(self.robotBody, self.robotShape)

    def _setTimestep(self, step):
        self.timestep = step

    def _tick(self, events):
        self.time += self.timestep
        self.algorithm(self, self.time, events)
        if (not self.stopped and self.endTime <= self.time and self.endTime != -1):
            self.stop()

    def _getRelativePosition(self, x,y):
        y = self.length - y
        h = sqrt((x)**2 + (y)**2)
        angle = -pi/2
        if (x != 0):
            angle = angle * abs(x)/x
        if (y != 0):
            angle = -atan(x/y)
        return (
            self.robotBody.position[0] + sin(-self.robotBody.angle - angle)*h,
            self.robotBody.position[1] + cos(-self.robotBody.angle - angle)*h
        )

    # Public:
    def getAngle(self):
        return self.robotBody.angle * 180 / pi

    def getPosition(self):
        return self._getRelativePosition(self.width/2, self.length/2)

    def getSensorData(self):
        ret = {}
        for sensor in self.sensors.keys():
            self.sensors[sensor].update(self, -self.robotBody.angle+pi/2, self.course)
            ret[sensor] = self.sensors[sensor].getData()
        return ret

    def getCameraData(self):
        ret = {}
        for camera in self.cameras.keys():
            self.cameras[camera].update(self, -self.robotBody.angle+pi/2, self.course)
            ret[camera] = self.cameras[camera].getData()
        return ret

    def isNotMoving(self):
        return self.stopped
    
    def constantMove(self, speed):
        self.stop()
        self.robotBody.velocity = (-speed * Vec2d(0, 1)).rotated(self.robotBody.angle)
        self.endTime = -1
        self.stopped = False

    def constantRotate(self, speed):
        self.stop()
        # convert to rad
        radiansPerSecond = speed * (pi / 180)
        self.robotBody.angular_velocity = radiansPerSecond
        self.endTime = -1
        self.stopped = False

    def move(self, speed, distance):
        self.stop()
        if (speed == 0):
            return
        self.robotBody.velocity = (-speed * Vec2d(0, 1)).rotated(self.robotBody.angle)
        self.endTime = distance / abs(speed) + self.time - self.timestep
        self.stopped = False

    def rotate(self, speed, degrees):
        self.stop()
        if (speed == 0):
            return
        # convert to rad
        degrees = degrees * (pi / 180)
        radiansPerSecond = speed * (pi / 180)
        self.robotBody.angular_velocity = radiansPerSecond
        self.endTime = abs(degrees / radiansPerSecond) + self.time - self.timestep
        self.stopped = False

    def stop(self):
        self.robotBody.angular_velocity = 0
        self.robotBody.velocity = 0,0
        self.stopped = True

class Sensor():
    def __init__(self, x, y, d, angle, debug=False):
        self.x = x
        self.debug = debug
        self.y = y
        self .d = d
        self.angle = -angle*pi/180
        self.data = -1

    def update(self, robot, angle, course):
        position = robot._getRelativePosition(self.x,self.y)
        (distance, color) = course.rayCast(position[0], position[1], angle+self.angle, self.debug)
        if (distance > self.d):
            distance = -1
        self.data = distance

    def getData(self):
        return self.data

class Camera():
    def __init__(self,x,y,angle,fieldOfView,splitCount,resolution,debug=False):
        self.debug = debug
        self.x = x
        self.y = y
        self.fieldOfView = fieldOfView
        self.splitCount = splitCount
        self.resolution = resolution
        self.angle = -angle*pi/180
        self.data = []
        for i in range(self.splitCount):
            self.data.append([])

    def update(self, robot, angle, course):
        position = robot._getRelativePosition(self.x,self.y)
        for i in range(self.splitCount):
            self.data[i] = []
        curSplit = 0
        increment = self.fieldOfView/self.resolution
        numRaysInSplit = self.resolution / self.splitCount
        start = self.fieldOfView/2
        nextSplit = numRaysInSplit
        oldColor = None
        value = start
        color = None
        for i in range(0, self.resolution):
            override = None
            if (i >= nextSplit):
                # Add the last color
                oldColor = None
                self.data[curSplit].append(color)
                curSplit = curSplit + 1
                nextSplit += numRaysInSplit
                override = (255,0,255,255)

            (distance, color) = course.rayCast(position[0], position[1], angle + self.angle + radians(value), self.debug, override)

            # When we encounter a new color we record the result to the split
            if (color != oldColor and oldColor != None):
                self.data[curSplit].append(oldColor)
            oldColor = color
            value -= increment
        self.data[curSplit].append(color)

    def getData(self):
        return self.data


class Course():
    def __init__(self, pixelsX, pixelsY, courseResolutionX, courseResolutionY):
        self.display = None
        self.yLength = courseResolutionY
        self.xLength = courseResolutionX
        self.course = [0]*(self.xLength*self.yLength)
        self.pixelsX = pixelsX
        self.pixelsY = pixelsY
        # Size of the boxes
        self.pxSizeX = pixelsX / self.xLength
        self.pxSizeY = pixelsY / self.yLength

    def _setDisplay(self, display):
        self.display = display

    def createBlock(self,x,y,sizeX,sizeY,space, c):
        points = [(0,0), (0, sizeY), (sizeX, sizeY), (sizeX, 0)]
        body = pymunk.Body(1, body_type=pymunk.Body.STATIC)
        body.position = (x,y)
        shape = pymunk.Poly(body, points)
        shape.color = c
        space.add(body, shape)

    def setCourse(self, course):
        self.course = course
    
    def circle(self, x, y, r, c):
        for i in range(0,720,1):
            self.set(round(cos(radians(i/2))*r + x), round(sin(radians(i/2))*r + y), c)

    def line(self, x1,y1,x2,y2, c):
        slope = 1000 
        if x2 != x1:
            if (x1 > x2):
                temp = x1
                x1 = x2
                x2 = temp
            slope = (y2 - y1) / (x2 - x1)
        if (slope < 1):
            # Draw over horizontal
            for x in range(x1,x2):
                y = slope * (x - x1) + y1
                self.set(x,y,c)
        else:
            if (y1 > y2):
                temp = y1
                y1 = y2
                y2 = temp
            # vertical
            slope = (x2 - x1) / (y2 - y1)
            for y in range(y1,y2):
                x = round(slope * (y - y1) + x1)
                self.set(x,y,c)

    # Stolen from C:
    # https://github.com/3DSage/OpenGL-Raycaster_v1/blob/master/3DSage_Raycaster_v1.c
    #
    def rayCast(self, xStart,yStart, angle, dbg=False, overrideColor=None):
        xIter,yIter,xOffset,yOffset,disV,distance = 0,0,0,0,0,0
        color = 0
        colorV = 0
        disV = 100000
        loopX = self.xLength
        # --- Vertical lines ----
        Tan = tan(angle)
        if (cos(angle)>=0):
            xIter=((xStart // self.pxSizeX) * self.pxSizeX)+self.pxSizeX + 0.0001
            yIter=(xStart-xIter)*Tan+yStart
            xOffset= self.pxSizeX
            yOffset=-xOffset*Tan
        elif(cos(angle)<0):
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
        if (sin(angle)>= 0):
            yIter=((yStart//self.pxSizeY)*self.pxSizeY) - 0.0001
            xIter=(yStart-yIter)*Tan+xStart
            yOffset= -self.pxSizeY
            xOffset=-yOffset*Tan
        elif(sin(angle)<0):
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
        if (self.display != None and dbg):
            pygame.draw.line(self.display,
            color if overrideColor == None else overrideColor,
            (xStart, yStart), (xIter, yIter), 1)
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

    def createOuterWalls(self, c):
        self.line(0,0,0,self.yLength, c)
        self.line(self.xLength - 1,0,self.xLength - 1,self.yLength, c)
        self.line(0,0,self.xLength,0, c)
        self.line(0,self.yLength - 1,self.xLength,self.yLength - 1, c)

    def box(self, x1,y1,x2,y2, c):
        self.line(x1,y1,x1,y2, c)
        self.line(x2,y1,x2,y2, c)
        self.line(x1,y1,x2,y1, c)
        self.line(x1,y2,x2,y2, c)

    def _createCourse(self, space):
        for x in range(self.xLength):
            for y in range(self.yLength):
                get = self.get(x,y)
                if (get != 0):
                    self.createBlock(x*self.pxSizeX,y*self.pxSizeY,self.pxSizeX*0.95,self.pxSizeY*0.95,space, get)

def run(course, robot, FPS):
    pygame.init()
    display = pygame.display.set_mode((course.pixelsX, course.pixelsY))
    drawOpt = pymunk.pygame_util.DrawOptions(display)
    clock = pygame.time.Clock()
    space = pymunk.Space()
    robot._setCourse(course)
    robot._initPhysics(space)
    robot._setTimestep(1/FPS)
    course._setDisplay(display)
    course._createCourse(space)

    while True:
        events = pygame.event.get()        # DO stuff

        # show the front

        display.fill(pygame.Color("black"))
        space.debug_draw(drawOpt)
        pygame.draw.circle(display, (0,255,255), robot._getRelativePosition(robot.width/2,robot.length), 4)
        robot._tick(events)
        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)
