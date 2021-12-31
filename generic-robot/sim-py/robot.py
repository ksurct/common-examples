import pygame
import pymunk
import sys
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


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

def createRobot(space, location):
    robotBody = pymunk.Body(1, float("inf"))
    robotShape = pymunk.Poly(robotBody, [(0,0),(10,0),(10,10),(0,10)])
    robotShape.sensor = False
    robotShape.color = (255, 50, 50, 255)
    robotShape.collision_type = 1
    robotShape.density = 0.5

    robotBody.position = location
    robotBody.velocity = 10,50
    space.add(robotBody, robotShape)
    return robotBody
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
    robot = createRobot(space, (400,400))
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                robot.velocity = (-100+robot.velocity[0], robot.velocity[1])
                robot.angular_velocity -= 10
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                robot.velocity = robot.velocity[0], -100+robot.velocity[1]
                robot.angular_velocity += 10
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                robot.velocity = robot.velocity[0], 100+robot.velocity[1]
                robot.angular_velocity -= 10
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                robot.velocity = 100+robot.velocity[0], robot.velocity[1]
                robot.angular_velocity += 10

        #pygame.display.update()
        display.fill(pygame.Color("black"))
        space.debug_draw(draw_options)
        
        display.blit(
            font.render("fps: " + str(clock.get_fps()), True, pygame.Color("white")),
            (0, 0),
        )
        
        pygame.display.flip()
        clock.tick(FPS)
        space.step(1/FPS)

if __name__ == "__main__":
    sys.exit(run())
