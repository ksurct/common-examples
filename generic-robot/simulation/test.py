import pymunk.pygame_util
from pymunk import Vec2d
import pygame
import pymunk


collisionTypes = {
    "wall": 0,
    "sensor": 1,
    "robot": 2
}

class RobotSim():
    def __init__(self, location, length, width, timestep, space):
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

    def rayCast(self):
        pass

    def tick(self):
        self.time += self.timestep
        if (not self.stopped):
            self.rayCast()
        if (not self.stopped and self.endTime <= self.time):
            print("Stopped at ", self.time)
            self.stop()

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
    robot = RobotSim((100,100), 100, 50, 1/FPS, space)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                robot.rotate(90, -45)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                robot.move(100, 50)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                robot.move(100, -50)
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
