import robot_sim

# Target FPS
FPS = 60

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events):
    # 'events' from pygame
    # 'time' time since start of program in seconds
    sensorData = robot.getSensorData()
    cameraData = robot.getCameraData()

    # in degrees
    angle = robot.getAngle()

    # Probable x,y coordinates
    position = robot.getPosition()

    for sensor in sensorData:
        # Do something
        pass

    for camera in cameraData:
        # Do something
        pass

    flip = False

    # Since this is called every 'tick' this is how to check
    # to see if the robot is still moving
    if (robot.isNotMoving()):
        if (flip):
            robot.move(distance=10, # in pixels
                    speed=10)    # pixels per second
        else:
            robot.rotate(degrees=90, # degrees
                         speed=45)   # degrees per second
        flip = not flip

# Pixels is the resolution on screen
# Course resolution is the grid count used to draw a course
course = robot_sim.Course(pixelsX=1000,
                          pixelsY=1000,
                          courseResolutionX=300,
                          courseResolutionY=300)


# -- Draw course --
#                       color
course.createOuterWalls(c=(255, 255, 255, 255))

#             x   y    r   color
course.circle(x=100,y=100,r=20,c=(0,0,255,255))
course.circle(x=200,y=100,r=20,c=(0,0,255,255))
course.circle(x=200,y=200,r=20,c=(0,0,255,255))
course.circle(x=100,y=200,r=20,c=(0,0,255,255))


# Sensors:
#                 | 0°
#                 |
#            __________
#     -90°  |          |
#    -------S <- (x,y) |
#    |--d---|          |
#           |          |
#           |  Robot   |
#           |          |
#           |          |
#      (0,0)x----------
#
sensors = [
    robot_sim.Sensor(name="TL",x=0,y=10,d=30,angle=-90),
    robot_sim.Sensor(name="BL",x=0,y=0,d=30,angle=-90),
    robot_sim.Sensor(name="BR",x=10,y=0,d=30,angle=90),
    robot_sim.Sensor(name="TR",x=10,y=10,d=30,angle=90)
]

# Cameras:
#                 | 0°
#                 |
#            ___________
#           |           |
#           | \       / |
#           |  \     /  |
#           |   \   /   |
#           |    \ϴ/ <---- fieldOfView
#           |     C     |
#           |   (x,y)   |
#      (0,0)x-----------
#
cameras = [
    robot_sim.Camera(name="main",
                     x=5,
                     y=5,
                     angle=0,
                     fieldOfView=45,
                     splitCount=2, # How many splits are in the camera when showing object colors
                     resolution=20 # How many rays are in the field of view
                     )
]

# Location is pixel placement in display
# Length and width are in pixels
robot = robot_sim.RobotSim(location=(100,100),
                           length=100,
                           width=50,
                           algorithm=algorithm,
                           sensors=sensors,
                           cameras=cameras)

robot_sim.run(course, robot, FPS)
