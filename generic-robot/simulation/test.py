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
# int r,mx,my,mp,dof,side; float vx,vy,rx,ry,ra,xo,yo,disV,disH; 
# 
# ra=FixAng(pa+30);                                                              //ray set back 30 degrees
# 
# for(r=0;r<60;r++)
# {
#  //---Vertical--- 
#  dof=0; side=0; disV=100000;
#  float Tan=tan(degToRad(ra));
#       if(cos(degToRad(ra))> 0.001){ rx=(((int)px>>6)<<6)+64;      ry=(px-rx)*Tan+py; xo= 64; yo=-xo*Tan;}//looking left
#  else if(cos(degToRad(ra))<-0.001){ rx=(((int)px>>6)<<6) -0.0001; ry=(px-rx)*Tan+py; xo=-64; yo=-xo*Tan;}//looking right
#  else { rx=px; ry=py; dof=8;}                                                  //looking up or down. no hit  
#
#  while(dof<8) 
#  { 
#   mx=(int)(rx)>>6; my=(int)(ry)>>6; mp=my*mapX+mx;                     
#   if(mp>0 && mp<mapX*mapY && map[mp]==1){ dof=8; disV=cos(degToRad(ra))*(rx-px)-sin(degToRad(ra))*(ry-py);}//hit         
#   else{ rx+=xo; ry+=yo; dof+=1;}                                               //check next horizontal
#  } 
#  vx=rx; vy=ry;
#

    def rayCast(self):
        r, mx, my, mp, dof = 0,0,0,0,0,
        vx,vy,rx,ry,ra,xo,yo,disV,disH = 0,0,0,0,0,0,0,0,0
        cube = self.course.xLength * self.course.yLength
        px = self.robotBody.position[0]
        py = self.robotBody.position[1]
        pa = self.robotBody.angle
        ra = -self.robotBody.angle + pi / 2
        print("angle = ", ra * 180 / pi)
        dof=0; disV = 100000
        Tan = tan(ra)
        if (cos(ra)> 0.001):
            rx=((px // Course.xLength) * Course.xLength)+Course.xLength
            ry=(px-rx)*Tan+py; xo= self.course.pxSizeX; yo=-xo*Tan
        elif(cos(ra)<-0.001):
            rx=((px//Course.xLength)*Course.xLength) - 0.0001
            ry=(px-rx)*Tan+py; xo=-self.course.pxSizeX; yo=-xo*Tan
        else:
            rx=px; ry=py; dof=8
        while(dof<8):
            mx=int((rx)//self.course.pxSizeX)
            my=int((ry)//self.course.pxSizeY)
            if(mx > 0 and my > 0 and Course.get(mx,my) == 1): #Course.get(mx,my)==1
                dof=8; disV=cos(ra)*(rx-px)-sin(ra)*(ry-py)
                break
            else:
                rx+=xo; ry+=yo; dof+=1
        vx=rx; vy=ry
        # Draw line from px py to rx ry
        pygame.draw.line(self.display, (0, 255, 0), (px, py), (rx, ry), 1)

    def tick(self):
        self.time += self.timestep
        self.rayCast()
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
