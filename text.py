from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from vec3 import Vec3
from ctypes import *

def beginText():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0,1600,0,1000)
    glMatrixMode(GL_MODELVIEW)

def endText():
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def drawString(pos,string):
    currentFont = GLUT_STROKE_ROMAN
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(pos.x,pos.y,pos.z)
    glScalef(0.1,0.1,1)

    glMaterialfv(GL_FRONT,GL_DIFFUSE,(1,1,0,1))
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN,c_int(ord(c)))

    #glutStrokeWidth()???

    glPopMatrix()

