import robot_sim
import random
import pygame

# Target FPS
FPS = 60
flip = False
white = (255,255,255,255)
blue = (0,0,255,255)
green = (0,255,0,255)
red = (255,0,0,255)
mod = 0
# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events=None):
    global white
    global blue
    global flip
    global green
    global red
    global mod
    robot.suppressUnknownMethodWarning = True
    # 'events' from pygame
    # 'time' time since start of program in seconds
    robot.test()
    sensorData = robot.getSensorData()
    cameraData = robot.getCameraData()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            robot.rotate(-90, 45)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            robot.move(100, 30)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            robot.move(-100, 30)
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            robot.rotate(90, 45)
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            robot.stop()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            robot.initPosition() 
            robot.initAngle() 
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            angle = robot.getAngle()
            position = robot.getPosition()
            print("------------------")
            print("Angle =", robot.getAngle())
            print("Position =", robot.getPosition())
        print("Front: ", robot.getSensorData()["Front"])
        print("Front2: ", robot.getSensorData()["Front2"])

    # in degrees

    # for cameraName in cameraData.keys():
    #     camera = cameraData[cameraName]
    #     # Do something
    #     # for split in camera:
    #     #     print("[", end="")
    #     #     for object in split:
    #     #         print(object, end="")
    #     #     print("]")
    # if (sensorData['Front'] < 100 and sensorData['Front'] != -1):
    #     while (mod == 0):
    #         mod = random.randrange(-1,2)
    #     robot.rotate(700 * mod, 35)
    # elif (robot.isNotMoving()):
    #     mod = 0
    #     robot.constantMove(20)

# Pixels is the resolution on screen
# Course resolution is the grid count used to draw a course
course = robot_sim.Course(pixelsX=800,
                          pixelsY=800,
                          courseResolutionX=180,
                          courseResolutionY=180,
                          pixelsPerMeter=5)


# -- Draw course --
course.createOuterWalls(c=white)

course.circle(x=200,y=200,r=40,c=blue, px=True)

course.box(x1=150,y1=10,x2=160,y2=180,c=green, px=False)



# Sensors:
#                 | 0??
#                 |
#            __________
#     -90??  |          |
#    -------S <- (x,y) |
#    |--d---|          |
#           |          |
#           |  Robot   |
#           |          |
#           |          |
#      (0,0)x----------
#
sensors = {
    "TL": robot_sim.Sensor(x=0,y=50,d=300,angle=-90,debug=False),
    "BL": robot_sim.Sensor(x=0,y=0,d=300,angle=-90,debug=False),
    "BR": robot_sim.Sensor(x=25,y=0,d=300,angle=90,debug=False),
    "TR": robot_sim.Sensor(x=25,y=50,d=300,angle=90,debug=False),
    "Front": robot_sim.Sensor(x=12.5,y=50,d=300,angle=0,debug=True,coneAngle=10),
    "Front2": robot_sim.Sensor(x=12.5,y=50,d=300,angle=0,debug=True)
}

# Cameras:
#                 | 0??
#                 |
#            ___________
#           |           |
#           | \       / |
#           |  \     /  |
#           |   \   /   |
#           |    \??/ <---- fieldOfView
#           |     C     |
#           |   (x,y)   |
#      (0,0)x-----------
#
cameras = {
    'main': robot_sim.Camera(x=12.5,
                   y=25,
                   angle=0,
                   fieldOfView=90,
                   splitCount=3, # How many splits are in the camera when showing object colors
                   resolution=40, # How many rays are in the field of view
                   debug=True,
                   maxDistance=300 # in pixels
                   )
}

cameras["main"].registerColor(blue, "Blue")
cameras["main"].registerColor(green, "Green")
cameras["main"].registerColor(red, "Red")
cameras["main"].registerColor(white, "White")

# Location is pixel placement in display
# Length and width are in pixels
robot = robot_sim.RobotSim(location=(20,40),
                           length=50,
                           width=25,
                           algorithm=algorithm,
                           sensors=sensors,
                           cameras=cameras,
                           startingAngle=-90,
                           sensorError=0,
                           positionError=0,
                           moveError=0,
                           rotationError=0,
                           angleError=0,
                           debugPrints=True)

robot_sim.run(course, robot, FPS)
