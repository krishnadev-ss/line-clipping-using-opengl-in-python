import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

INSIDE = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000

# Defining x_max, y_max and x_min, y_min for rectangle
# Since diagonal points are enough to define a rectangle
x_max = 200
y_max = 200
x_min = 100
y_min = 100


# Function to compute region code for a point(x, y)
def computeCode(x, y):
    code = INSIDE
    if x < x_min:
        code |= LEFT
    if x > x_max:
        code |= RIGHT
    if y < y_min:
        code |= BOTTOM
    if y > y_max:
        code |= TOP
    return code


def plot_line(x1, y1, x2, y2,color):
    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
    glFlush()

def draw_boundaries(x1, y1, x2, y2 ):
    glColor3f(1,0,0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1, y1)
    glVertex2f(x1, y2)
    glVertex2f(x2, y2)
    glVertex2f(x2, y1)
    glEnd()
    glFlush()


def cohenSutherlandClip(x1_b, y1_b, x2_b, y2_b, p1, p2):
    x1 = p1[0]
    x2 = p2[0]

    y1 = p1[1]
    y2 = p2[1]

    draw_boundaries(x1_b, y1_b, x2_b, y2_b)
    #plot_line(x1, y1, x2, y2, [0,1,0])

    code1 = computeCode(x1, y1)
    code2 = computeCode(x2, y2)


    accept = False

    while True:

        if code1 == 0 and code2 == 0:
            accept = True
            break

        elif (code1 & code2) != 0:
            break

        else:

            # Line Needs clipping
            x = 1.0
            y = 1.0
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            # using formulas y = y1 + slope * (x - x1),
            # x = x1 + (1 / slope) * (y - y1)
            if code_out & TOP:

                # point is above the clip rectangle
                x = x1 + ((x2 - x1) / (y2 - y1)) * (y_max - y1)
                y = y_max


            elif code_out & BOTTOM:

                # point is below the clip rectangle
                x = x1 + ((x2 - x1) / (y2 - y1)) * (y_min - y1)
                y = y_min

            elif code_out & RIGHT:

                # point is to the right of the clip rectangle
                y = y1 + ((y2 - y1) / (x2 - x1)) * (x_max - x1)
                x = x_max

            elif code_out & LEFT:

                # point is to the left of the clip rectangle
                y = y1 + ((y2 - y1) / (x2 - x1)) * (x_min - x1)
                x = x_min

            # Now intersection point x, y is found
            # We replace point outside clipping rectangle
            # by intersection point
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = computeCode(x1, y1)

            else:
                x2 = x
                y2 = y
                code2 = computeCode(x2, y2)

    if accept:
        plot_line(x1, y1, x2, y2,[1,1,1])

    else:
        print("Line rejected")


window_size = 800


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, window_size, window_size, 0)


def main():
    print("Enter clipping boundaries :")
    # x1 = int(input("Enter x1: "))
    # y1 = int(input("Enter y1: "))
    # x2 = int(input("Enter x2: "))
    # y2 = int(input("Enter y2: "))
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(window_size, window_size)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("cohenSutherlandClip")
    glutDisplayFunc(lambda: cohenSutherlandClip(x_min, y_min, x_max,
y_max,[30,0], [500, 500]))
    glutIdleFunc(lambda: cohenSutherlandClip(x_min, y_min, x_max,
y_max, [30,0], [500, 500]))
    init()
    glutMainLoop()


main()
