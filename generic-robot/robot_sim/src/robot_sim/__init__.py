import random
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
        cameras=None,
        startingAngle=0,
        positionError=0,
        angleError=0,
        moveError=0,
        rotationError=0,
        sensorError=0,
        debugPrints=False
        ):
        self.initialAngle = 0
        self.initialPosition = 0,0
        self.debugPrints=debugPrints
        self.isRunningArc = False
        self.positionError = positionError
        self.angleError = angleError
        self.moveError = moveError
        self.rotationError = rotationError
        self.sensorError = sensorError
        self.length = length
        self.width = width
        self.arcSpeed = 0
        self.cameras = cameras
        self.sensors = sensors
        self.algorithm = algorithm
        self.time = 0
        self.timestep = 0
        self.robotBody = pymunk.Body(1, float("inf"))
        self.robotBody.position = location
        self.robotBody.angle = radians(startingAngle)
        self.robotShape = pymunk.Poly(self.robotBody, [(0,0),(self.width,0),(self.width,self.length),(0,self.length)])
        self.robotShape.sensor = False
        self.defaultVeloFunc = lambda body, gravity, damping, dt: None
        self.robotShape.color = (255, 100, 100, 100)
        self.robotShape.density = 0.5
        self.endTime = 0
        self.stopped = True
        self.suppressUnknownMethodWarning = False
        self.initPosition()

    def _log(self, msg):
        if (self.debugPrints):
            print("robot_sim", msg)

    # allow for generic function calls on robot
    def __getattr__(self, name):
        def method(*args):
            if (not self.suppressUnknownMethodWarning):
                print("Call to unkown method:", name)
        return method

    def _setCourse(self, course):
        self.course = course
    
    def _initPhysics(self, space):
        space.add(self.robotBody, self.robotShape)

    def _setTimestep(self, step):
        self.timestep = step

    def initAngle(self):
        self.initialAngle = self._getAngle()
        self._log("Init angle (%f)" % self.initialAngle)

    def initPosition(self):
        self.initialPosition = self._getRelativePosition(self.width/2, self.length/2)
        self._log("Init posistion {}".format(self.initialPosition))

    def _tick(self, events):
        self.time += self.timestep
        if (self.isRunningArc):
            self._constantMove(self.arcSpeed)
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
            (self.robotBody.position[0] + sin(-self.robotBody.angle - angle)*h),
            (self.robotBody.position[1] + cos(-self.robotBody.angle - angle)*h)
        )

    def _getAngle(self):
        return (self.robotBody.angle * 180 / pi) + (random.uniform(-self.angleError, self.angleError))

    # Public:
    def getAngle(self):
        angle = self._getAngle() - self.initialAngle
        while (angle > 360):
            angle -= 360
        while (angle < -360):
            angle += 360
        if (angle > 180):
            angle -= 360
        if (angle < -180):
            angle += 360
        return (angle) + (random.uniform(-self.angleError, self.angleError))

    def _convertToRelativeCoord(self, pos):
        return (
            cos(radians(self.initialAngle)) * pos[0] + sin(radians(self.initialAngle)) * pos[1],
            sin(radians(self.initialAngle)) * pos[0] - cos(radians(self.initialAngle)) * pos[1]
        )

    def getPosition(self):
        val = self._getRelativePosition(self.width/2, self.length/2)
        val = self._convertToRelativeCoord(val)
        offset = self._convertToRelativeCoord(self.initialPosition)
        return  (
            ((val[0] - offset[0]) / self.course.pixelsPerMeter) + (random.uniform(-self.positionError, self.positionError)),
            ((val[1] - offset[1]) / self.course.pixelsPerMeter) + (random.uniform(-self.positionError, self.positionError))
        )

    def getSensorData(self):
        ret = {}
        for sensor in self.sensors.keys():
            self.sensors[sensor].update(self, -self.robotBody.angle+pi/2, self.course)
            data = self.sensors[sensor].getData()
            ret[sensor] = data if data == -1 else data + (random.uniform(-self.sensorError, self.sensorError))
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
        self._log("Constant move mps:%f" % speed)
        self.stop()
        self.endTime = -1
        self._constantMove(speed)

    def constantRotate(self, speed):
        self._log("Constant rotate dps:%f" % speed)
        self.stop()
        self.endTime = -1
        self._constantRotate(speed)

    def move(self, speed, distance):
        self._log("Move mps:%f, meters:%f" % (speed, distance))
        self.stop()
        self._move(speed, distance)

    def addError(self, cur, error):
        if (cur < 0 and cur + error > 0):
            return 0
        if (cur > 0 and cur + error < 0):
            return 0
        return cur + error

    def _constantMove(self, speed):
        error = (random.uniform(-self.moveError, self.moveError))
        if (speed == 0):
            error = 0
        speed = self.addError(speed, error)
        speed = self.course.pixelsPerMeter * -speed
        self.robotBody.velocity = (speed * Vec2d(0, 1)).rotated(self.robotBody.angle)
        self.stopped = False

    def _constantRotate(self, speed):
        error = (random.uniform(-self.rotationError, self.rotationError))
        if (speed == 0):
            error = 0
        speed = self.addError(speed, error)

        # convert to rad
        radiansPerSecond = speed * (pi / 180)
        self.robotBody.angular_velocity = radiansPerSecond
        self.stopped = False

    def _move(self, speed, distance):
        error = (random.uniform(-self.moveError, self.moveError))
        if (speed == 0):
            return
        speed = self.addError(speed, error)

        speed = speed * self.course.pixelsPerMeter
        distance = distance * self.course.pixelsPerMeter
        self.robotBody.velocity = (-speed * Vec2d(0, 1)).rotated(self.robotBody.angle)
        self.endTime = distance / abs(speed) + self.time - self.timestep
        self.stopped = False

    def rotate(self, speed, degrees):
        self._log("Rotate dps:%f, degrees:%f" % (speed, degrees))
        self.stop()
        self._rotate(speed, degrees)

    def _rotate(self, speed, degrees):
        error = (random.uniform(-self.moveError, self.moveError))
        if (speed == 0):
            return
        # convert to rad
        degrees = degrees * (pi / 180)
        speed = self.addError(speed, error)
        radiansPerSecond = speed * (pi / 180)
        self.robotBody.angular_velocity = radiansPerSecond
        self.endTime = abs(degrees / radiansPerSecond) + self.time - self.timestep
        self.stopped = False

    def constantArcMove(self, speed, radius):
        # Gravity at center of circle = v^2 / r
        # angular velocity = (360 / circumference) * v
        self.constantRotate(speed*360/(2*pi*radius))
        self._constantMove(speed)
        self.isRunningArc = True
        self.arcSpeed = speed

    def arcMove(self, speed, radius, distance):
        # Gravity at center of circle = v^2 / r
        # angular velocity = (360 / circumference) * v
        self.constantArcMove(speed, radius)
        self.endTime = distance / abs(speed) + self.time - self.timestep

    def stop(self):
        self.robotBody.angular_velocity = 0
        self.robotBody.velocity = 0,0
        self.stopped = True
        self.isRunningArc = False
        self.robotBody.velocity_func = self.defaultVeloFunc

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
        (distance, color) = course.rayCast(position[0], position[1], angle+self.angle, self.debug, self.d)
        if (distance > self.d or distance == None):
            self.data = -1
            return
        self.data = distance / course.pixelsPerMeter

    def getData(self):
        return self.data

class Camera():
    def __init__(self,x,y,angle,fieldOfView,splitCount,resolution,maxDistance=None,debug=False):
        self.colorMap = {}
        self.debug = debug
        self.maxDistance = maxDistance
        self.x = x
        self.y = y
        self.fieldOfView = fieldOfView
        self.splitCount = splitCount
        self.resolution = resolution
        self.angle = -angle*pi/180
        self.data = []
        for i in range(self.splitCount):
            self.data.append([])

    def registerColor(self, color, name):
        self.colorMap[color] = name

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
        size = 0
        for i in range(0, self.resolution):
            override = None
            if (i >= nextSplit):
                # Add the last color
                oldColor = None
                if (color != None):
                    c = color
                    if (color in self.colorMap):
                        c = self.colorMap[color]
                    self.data[curSplit].append({"size": size, "color": c})
                size = 0
                curSplit = curSplit + 1
                nextSplit += numRaysInSplit
                override = (255,0,255,255)
            size = size + 1
            (distance, color) = course.rayCast(
                position[0], position[1], angle + self.angle + radians(value), self.debug, override, self.maxDistance)

            # When we encounter a new color we record the result to the split
            if (color != oldColor and oldColor != None):
                c = oldColor
                if (oldColor in self.colorMap):
                    c = self.colorMap[oldColor]
                self.data[curSplit].append({"size": size, "color": c})
                size = 0
            oldColor = color
            value -= increment
            if (color == None):
                size = 0
        if (color != None):
            c = color
            if (color in self.colorMap):
                c = self.colorMap[color]
            self.data[curSplit].append({"size": size, "color": c})

    def getData(self):
        return self.data


class Course():
    def __init__(self, pixelsX, pixelsY, courseResolutionX, courseResolutionY, pixelsPerMeter=1):
        self.pixelsPerMeter = pixelsPerMeter
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
    
    def circle(self, x, y, r, c, px=False):
        if (px):
            x = x * (self.xLength / self.pixelsX)
            y = y * (self.yLength / self.pixelsY)
            r = r * (self.xLength / self.pixelsX)
        for i in range(0,720,1):
            self._set(round(cos(radians(i/2))*r + x), round(sin(radians(i/2))*r + y), c, False)

    def _set(self, x,y,c,px):
        if (px):
            self.setPx(x,y,c)
        else:
            self.set(x,y,c)

    def line(self, x1,y1,x2,y2, c, px=False):
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
                self._set(x,y,c,px)
        else:
            if (y1 > y2):
                temp = y1
                y1 = y2
                y2 = temp
            # vertical
            slope = (x2 - x1) / (y2 - y1)
            for y in range(y1,y2):
                x = round(slope * (y - y1) + x1)
                self._set(x,y,c,px)

    # Stolen from C:
    # https://github.com/3DSage/OpenGL-Raycaster_v1/blob/master/3DSage_Raycaster_v1.c
    #
    def rayCast(self, xStart,yStart, angle, dbg=False, overrideColor=None, maxDistance=None):
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
            if (maxDistance != None and disV > maxDistance):
                disV = None
                colorV = None
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
        if (maxDistance != None and distance > maxDistance):
            distance = None
            color = None
        elif (self.display != None and dbg):
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

    def setPx(self,x,y, color):
        self.set(x * (self.xLength  / self.pixelsX), y * (self.yLength  / self.pixelsY), color)

    def createOuterWalls(self, c):
        self.line(0,0,0,self.yLength, c)
        self.line(self.xLength - 1,0,self.xLength - 1,self.yLength, c)
        self.line(0,0,self.xLength,0, c)
        self.line(0,self.yLength - 1,self.xLength,self.yLength - 1, c)

    def box(self, x1,y1,x2,y2, c, px=False):
        self.line(x1,y1,x1,y2, c, px)
        self.line(x2,y1,x2,y2, c, px)
        self.line(x1,y1,x2,y1, c, px)
        self.line(x1,y2,x2,y2, c, px)

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
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        display.fill(pygame.Color("black"))
        space.debug_draw(drawOpt)
        pygame.draw.circle(display, (0,255,255), robot._getRelativePosition(robot.width/2,robot.length), 4)
        robot._tick(events)
        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)
