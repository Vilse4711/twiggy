from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from vec3 import Vec3
from module import *
from visitor import ModuleVisitor
import copy
import math

class GLTurtle(ModuleVisitor):
    def __init__(self):
        self.debug = False
        self.drawing = False
        self.dir = Vec3(1.,0.,0.)
        self.up = Vec3(0.,1.,0.)
        self.right = Vec3(0.,0.,1.)
        self.pos = Vec3(0.,0.,0.)
        self.width = 1
        self.color = (0.0,0.5,0.0,1.0)
        self.trail = []
        self.poly = None

    def __str__(self):
        return '%s,%s,%s,%s' % (self.pos,self.dir,self.up,self.right)

    def visit_y(self,module):
        #self.yaw(module.angle)
        pass        

    def visit_r(self,module):
        #self.roll(module.angle)
        pass
    
    def visit_p(self,module):
        #self.pitch(module.angle)
        pass
    
    def visit_c(self,module):
        self.color = module.color

    def visit_w(self,module):
        self.width = module.width
        
    def visit_F(self,module):
        self.forward(module)

    def visit_f(self,module):
        self.skip(module)

    def visit_Q(self,module):
        pass

    def visit_O(self,module):
        self.sphere(module)

    def visit_PB(self,module):
        self.beginPoly(module.getData())
        
    def visit_PE(self,module):
        self.endPoly()

    def visit_t(self,module):
        if self.poly <> None:
            self.poly.turn(module.angle)
        else:
            raise LException("t() module outside a polygon not allowed!")
        
    def visit_LB(self,module):
        return
        self.push()
        
    def visit_RB(self,module):
        return
        self.pop()

    def beginPoly(self,state):
        self.poly = Poly(state)

    def endPoly(self):
        assert len(self.poly.verts) > 2
        pos = self.poly.origin()
        color = self.poly.state.color
        orientation = self.poly.orientation()

        glPushMatrix()
        glTranslatef(pos.x,pos.y,pos.z)
        glMultMatrixf(orientation)
        
        glDisable(GL_CULL_FACE)
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,color)

        glBegin(GL_POLYGON)
        glNormal3f(0,1,0)
        for v in self.poly.verts:
            glVertex3f(v.x,v.y,v.z)
        glEnd()

        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)
        glEnable(GL_CULL_FACE)

        glPopMatrix()
        self.poly = None
        
    def sphere(self,module):
        pos = module.getData().pos
        color = module.getData().color
        
        glPushMatrix()
        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
        glTranslatef(pos.x,pos.y,pos.z)
        glTranslatef(0.,0.5,0.)
        glutSolidSphere(module.radius,16,16)
        glPopMatrix()
        
    def forward(self,module):
        pos = module.getData().pos
        color = module.getData().color
        orientation = module.getData().orientation()
        factor = module.factor
        width = module.getData().width
        
        q0 = gluNewQuadric()
        glPushMatrix()
        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
        glTranslatef(pos.x,pos.y,pos.z)
        glMultMatrixf(orientation)
        glPushMatrix()        
        glScalef(module.length,width,width)
        glRotatef(90,0,1,0)
        gluCylinder(q0,0.5,0.5*factor,1.0,16,4)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(module.length,0,0)
        glRotatef(90,0,1,0)
        gluDisk(q0,0,width/2*factor,16,1)
        glPopMatrix()
        
        glPopMatrix()
        gluDeleteQuadric(q0)

    def skip(self,module):
        # Make sure dir is of unit length
        if self.poly <> None:
            self.poly.move(module.length)

    def yaw(self,angle):
        if self.poly <> None:
            self.poly.turn(angle)
        else:
            self.dir = self.dir.rotate(self.up,angle).roundOff()
            self.right = self.right.rotate(self.up,angle).roundOff()
        return self.dir
    
    def pitch(self,angle):
        if self.poly <> None:
            raise LException("p() not allowed inside a polygon primitive")
        
        self.dir = self.dir.rotate(self.right,angle).roundOff()
        self.up = self.up.rotate(self.right,angle).roundOff()
        return self.dir

    def roll(self,angle):
        if self.poly <> None:
            raise LException("r() not allowed inside a polygon primitive")
        
        self.up = self.up.rotate(self.dir,angle).roundOff()
        self.right = self.right.rotate(self.dir,angle).roundOff()
        return self.dir
    
    def push(self):
        self.trail.append((copy.deepcopy(self.pos),
                           copy.deepcopy(self.dir),
                           copy.deepcopy(self.up),
                           copy.deepcopy(self.right),
                           self.width,
                           copy.deepcopy(self.color)))

    def pop(self):
        self.pos,self.dir,self.up,self.right,self.width,self.color = self.trail.pop()

    # Move turtle to world origo
    def goto(self,pos):
        self.pos = pos
        return pos

    # Align turtle coordinate system with world coordinate system
    def align(self):
        self.dir = Vec3(1.,0.,0.)
        self.up = Vec3(0.,1.,0.)
        self.right = Vec3(0.,0.,1.)
        
    def drawTurtle(self):
        scale = 100
        glDisable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glPushMatrix()
        glTranslatef(self.pos.x,self.pos.y,self.pos.z)
        glScalef(scale,scale,scale)
        glBegin(GL_LINES)
        # Forward is GREEN (Roll-axis)
        glColor3f(0,1,0)
        glVertex3f(0.,0.,0.)
        glVertex3f(self.dir.x,self.dir.y,self.dir.z)
        # Up is Red (Yaw-axis)
        glColor3f(1,0,0)
        glVertex3f(0.,0.,0.)
        glVertex3f(self.up.x,self.up.y,self.up.z)
        # Right is Blue (Pitch-axis)
        glColor3f(0,0,1)
        glVertex3f(0.,0.,0.)
        glVertex3f(self.right.x,self.right.y,self.right.z)
        glEnd()
        glPopMatrix()
        glDisable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

class Poly:
    def __init__(self,state):
        self.state = state
        self.pos = Vec3(0.0,0.0,0.0)
        self.verts = [self.pos]
        self.dir = Vec3(1.0,0.0,0.0)

    def __repr__(self):
        s = "Poly("
        for v in self.verts:
            s = s + "," + repr(v)
        s = s + ")"
        return s
            
    def turn(self,angle):
        self.dir = self.dir.rotate(Vec3.UP,angle)

    def move(self,distance):
        self.pos = self.pos + self.dir.scale(distance)
        self.verts.append(self.pos)

    def origin(self):
        return self.state.pos

    def orientation(self):
        return self.state.orientation()
        
if __name__ == "__main__":

    t = GLTurtle()
    t.roll(45)
    print t.dir
    print t.up
    print t.right
    print t.toLocal()
    
