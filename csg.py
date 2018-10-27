from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from vec3 import Vec3

g_alpha = 0.5

class CSG:
    def inside(self,point):
        return False

    def draw(self,complement):
        pass
    def _preDraw(self,complement):
        if not complement:
            glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,(0,1,0,1.0))
            glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,(0,1,0,1.0))
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendColor(0.3,0.5,0.3,1)
            glBlendFunc(GL_SRC_ALPHA, GL_CONSTANT_COLOR)
        else:
            glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,(1,0,0,1.0))
            glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,(1,0,0,1.0))            
        glPushMatrix()

    def _postDraw(self,complement):
        if not complement:
            glEnable(GL_DEPTH_TEST)
            glDisable(GL_BLEND)
        glPopMatrix()
        
    
class Cube(CSG):
    def __init__(self):
        self.min = Vec3(-0.5,-0.5,-0.5)
        self.max = Vec3(0.5,0.5,0.5)

    def inside(self,point):
        bx = point.x > self.min.x and point.x < self.max.x
        by = point.y > self.min.y and point.y < self.max.y
        bz = point.z > self.min.z and point.z < self.max.z
        return bx and by and bz

    def draw(self,complement):
        self._preDraw(complement)
        glutSolidCube(1.0)
        self._postDraw(complement)
        
class Sphere(CSG):
    def __init__(self):
        self.radius = 0.5

    def inside(self,point):
        return point.length() < self.radius

    def draw(self,complement):
        self._preDraw(complement)
        glutSolidSphere(self.radius,16,16)
        self._postDraw(complement)

def Cylinder(CSG):
    def __init__(self):
        self.radius = 0.5

    def inside(self,point):
        r = self.radius
        dy = point.y > -r and point.y < r
        dxz = math.sqrt(point.x*point.x + point.z*point.z) < r*r
        return dy and dxz
    
    def draw(self,complement):
        self._preDraw(complement)
        q = gluNewQuadric()
        glTranslatef(0,-0.5,0)
        glRotatef(-90,1,0,0)
        glutSolidCylinder(q,0.5,0.5,16,4)
        gluDeleteQuadric(q)
        self._postDraw(complement)

class Halfplane(CSG):
    def __init__(self,normal,d):
        self.normal = normal
        self.d = d

    def inside(self,point):
        # Point is considered inside if it is below the plane
        p = point
        n = self.normal
        return p.x*n.x + p.y*n.y + p.z*n.z - self.d < 0
        
    def draw(self,complement):
        pass

class Union(CSG):
    def __init__(self,csg0,csg1):
        self.csg0 = csg0
        self.csg1 = csg1

    def inside(self,point):
        return self.csg0.inside(point) or self.csg1.inside(point)

    def draw(self,complement):
        self.csg0.draw(complement)
        self.csg1.draw(complement)

class Intersection(CSG):
    def __init__(self,csg0,csg1):
        self.csg0 = csg0
        self.csg1 = csg1

    def inside(self,point):
        return self.csg0.inside(point) and self.csg1.inside(point)

    def draw(self,complement):
        self.csg0.draw(complement)
        self.csg1.draw(complement)

class Difference(CSG):
    def __init__(self,csg0,csg1):
        self.csg0 = csg0
        self.csg1 = csg1

    def inside(self,point):
        return self.csg0.inside(point) and not self.csg1.inside(point)

    def draw(self,complement):
        self.csg0.draw(complement)
        self.csg1.draw(complement)

class Complement(CSG):
    def __init__(self,csg):
        self.csg = csg

    def inside(self,point):
        return not self.csg.inside(point)

    def draw(self,complement):
        # Once you complement you can't go back
        self.csg.draw(True)
    
class Rotation(CSG):
    def __init__(self,csg,angle,axis):
        self.csg = csg
        self.angle = angle
        self.axis = axis

    def reverse(self,point):
        return point.rotate(self.axis,-self.angle)

    def inside(self,point):
        return self.csg.inside(self.reverse(point))

    def draw(self,complement):
        glPushMatrix()
        glRotatef(self.angle,self.axis.x,self.axis.y,self.axis.z)
        self.csg.draw(complement)
        glPopMatrix()
        
class Translation(CSG):
    def __init__(self,csg,vector):
        self.csg = csg
        self.vector = vector
        
    def reverse(self,point):
        return point - self.vector

    def inside(self,point):
        return self.csg.inside(self.reverse(point))

    def draw(self,complement):
        glPushMatrix()
        glTranslatef(self.vector.x,self.vector.y,self.vector.z)
        self.csg.draw(complement)
        glPopMatrix()
        
class Scaling(CSG):
    def __init__(self,csg,vector):
        self.csg = csg
        self.vector = vector
        self.ivector = Vec3(1.0/vector.x,1.0/vector.y,1.0/vector.z)
        
    def reverse(self,point):
        iv = self.ivector
        v = Vec3(point.x*iv.x,point.y*iv.y,point.z*iv.z)
        return Vec3(point.x*iv.x,point.y*iv.y,point.z*iv.z)

    def inside(self,point):
        return self.csg.inside(self.reverse(point))

    def draw(self,complement):
        glPushMatrix()
        glScalef(self.vector.x,self.vector.y,self.vector.z)
        self.csg.draw(complement)
        glPopMatrix()
        
if __name__ == "__main__":
    c0 = Cube()  
    c1 = Scaling(c0,Vec3(300,300,300))
    print c1.inside(Vec3(100,100,100))
    
