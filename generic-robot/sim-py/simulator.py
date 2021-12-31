import pygame
import pymunk
import sys
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


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
        self.robotBodies = []
        for i in range(2):
            self.robotBodies.append(pymunk.Body(1, float("inf")))
            if (i == 0):
                self.robotBodies[i].position = location
            else:
                self.robotBodies[i].position = (location[0] + self.width / 2, location[1] + self.length / 2)

        self.robotShape = pymunk.Poly(self.robotBodies[0], [(0,0),(self.width,0),(self.width,self.length),(0,self.length)])
        self.robotSensor = pymunk.Segment(self.robotBodies[1], (0, self.length/2), (0, self.length/2 + 1000), 1)
        self.robotSensor.sensor = True
        self.robotSensor.collision_type = collisionTypes["sensor"]
        self.robotSensor.color = (150, 150, 255, 255)
        self.robotShape.sensor = False
        self.robotShape.color = (255, 50, 50, 255)
        self.robotShape.collision_type = collisionTypes["robot"]
        self.robotShape.density = 0.5
        self.endTime = 0
        space.add(self.robotBodies[0], self.robotShape)
        space.add(self.robotBodies[1], self.robotSensor)
        self.stopped = True

    # meters per second
    def move(self, meters, speed):
        self.stop()
        for body in self.robotBodies:
            body.velocity = (speed * Vec2d(0, 1)).rotated(body.angle)
        self.endTime = meters / abs(speed) + self.time
        print("Starting at ", self.time, " ending at ", self.endTime)
        self.stopped = False

    def rotate(self, degrees, degreesPerSecond):
        self.stop()
        # convert to rad
        degrees = degrees * (3.1415 / 180)
        degreesPerSecond = degreesPerSecond * (3.1415 / 180)
        for body in self.robotBodies:
            body.angular_velocity = degreesPerSecond
        self.endTime = degrees / abs(degreesPerSecond) + self.time
        print("Starting at ", self.time, " ending at ", self.endTime)
        self.stopped = False

    def stop(self):
        for body in self.robotBodies:
            body.angular_velocity = 0
            body.velocity = 0,0
        self.stopped = True

    def tick(self):
        self.time += self.timestep
        if (not self.stopped and self.endTime <= self.time):
            print("Stopped at ", self.time)
            self.stop()


class Wall():
    def __init__(self, p1, p2, width):
        self.p1 = p1
        self.p2 = p2
        self.width = width

def createWalls(space, walls):
        # walls - the left-top-right walls
    
    static: list[pymunk.Shape] = []

    for wall in walls:
        static.append(pymunk.Segment(space.static_body, wall.p1, wall.p2, wall.width))

    for s in static:
        s.friction = 1.0
        s.group = 1

    space.add(*static)

def run():
    pygame.init()
    display = pygame.display.set_mode((800,800))
    clock = pygame.time.Clock()
    FPS = 120
    space = pymunk.Space()
    draw_options = pymunk.pygame_util.DrawOptions(display)
    font = pygame.font.SysFont("Arial", 16)

    createWalls(space, [
        Wall((800,800), (800,0), 10),
        Wall((800,800), (0,800), 10),
        Wall((0,0), (800,0), 10),
        Wall((0,0), (0,800), 10),
    ])

    robot = RobotSim((100,100), 100, 50, 1/FPS, space)

    def callback(arbiter, space, data):
        print("Called!", data, arbiter)
        return True

    h = space.add_collision_handler(collisionTypes["sensor"], collisionTypes["wall"])
    h.begin = callback
    h.separate = callback

    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                robot.rotate(90, -45)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                robot.move(100, 50)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                robot.move(100, -50)
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                robot.rotate(90, 45)

        #pygame.display.update()
        display.fill(pygame.Color("black"))
        space.debug_draw(draw_options)

        display.blit(
            font.render("fps: " + str(clock.get_fps()), True, pygame.Color("white")),
            (15, 15),
        )
        robot.tick()
        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

if __name__ == "__main__":
    sys.exit(run())
