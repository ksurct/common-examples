# Installation:
## Python
- Make sure you have python installed
- - https://www.python.org/downloads/windows/

## Script install
- On windows, run the install.ps1 file by right clicking from file explorer and running with powershell
- On ubuntu, run the install.sh file 

## Manual installation
### Install python build
- Windows: `py -m pip install --upgrade build`
- Ubuntu: `python3 -m pip install --upgrade build`

### Install dependencies
- Pymunk: `py -m pip install pymunk`
- Pygame: `py -m pip install -U pygame --user`

## Install package
- Inside of the robot_sim folder run
- Windows: `py -m build`, Ubuntu: `python3 -m build`
- Windows: `py -m pip install .`, Ubuntu: `pip install .`

# Running
Look at the example.py file provided for how to use
- Try running example.py to make sure it works

## Create Course

The course class creates a course for the robot to navigate through.

> put snapshot image of course

When instantiated, the constructor requires the length of the course in pixels in the x and y direction, as well as the resolution in the x and y direction. The resolution is the pixel width and length of the grid squares. The resolution values cannot exceed the length and width of the window.

```python
course = robot_sim.Course(pixelsX=800,
                          pixelsY=800,
                          courseResolutionX=180,
                          courseResolutionY=180)
```

The createOuterWalls function creates a boundary around the edge of the course window. It takes in a color parameter that determines the color of the boundary.

```python
course.createOuterWalls(c=white)
```

The circle function creates a circular obstacle that takes in an x and y location, as well as the radius and color. The x and y values correspond to the pixel location and the radius is in number of pixels.

```python
course.circle(x=100,y=100,r=20,c=blue)
```

The box function creates a rectangular obstacle that takes in a pair of x and y values corresponding to two of the vertices of the rectangle as well as a color.

```python
course.box(x1=150,y1=10,x2=160,y2=180,c=green)
```

## Robot

## Sensors

## Cameras

## Notes

Color uses the RGBA color model with r, g and b representing the red, green and blue components of the color and the A standing for alpha which represents the opacity of the color. The lower alpha is the more that the color appears transparent.

Pixel location begins at (0,0) in the upper left corner.

> add picture of how pixel location works