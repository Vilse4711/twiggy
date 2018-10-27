import copy
from vec3 import Vec3
from lcs import LCS
from module import *
from visitor import ModuleVisitor
from lexception import LException

class LTurtleState:
    def __init__(self):
        self.ori = LCS()
        self.pos = Vec3(0.,0.,0.)
        self.width = 1
        self.color = (0.0,0.5,0.0)

    def __str__(self):
        return str(self.pos) + " " + str(self.ori[0]) + " " + str(self.ori[1]) + " " + str(self.ori[2]) 
        
    def yaw(self,angle):
        self.ori.rotY(angle)

    def pitch(self,angle):
        self.ori.rotZ(-angle)

    def roll(self,angle):
        self.ori.rotX(angle)

    def level(self):
        V = Vec3(0, 1, 0)
        H = self.getDir()
        L = self.getRight()

        # This is fishy ... all
        U = V.cross(H)
        L = H.cross(U)

        self.setUp(U)
        self.setRight(L)

    def move(self,length):
        x,y,z = self.ori[0]
        self.pos.x = self.pos.x  + x*length
        self.pos.y = self.pos.y  + y*length
        self.pos.z = self.pos.z  + z*length

    def getPos(self):
        return self.pos

    def getDir(self):
        return self.ori.rowAsVec3(0)

    def setDir(self, v):
        self.ori.mat[0] = v.toList()

    def getUp(self):
        return self.ori.rowAsVec3(1)

    def setUp(self, v):
        self.ori.mat[1] = v.toList()

    def getRight(self):
        return self.ori.rowAsVec3(2)

    def setRight(self, v):
        self.ori.mat[2] = v.toList()

    def orientation(self):
        return self.ori.orientation()

    def copy(self):
        cc = LTurtleState()
        cc.pos = Vec3(self.pos.x,self.pos.y,self.pos.z)
        cc.width = self.width
        cc.color = self.color
        cc.ori = self.ori.copy()
        return cc
        
class Turtle(ModuleVisitor):
    def __init__(self):
        self.state = LTurtleState()
        self.inPoly = False
        self.trail = []

    ## Visitor methods
    def visit_y(self,module):
        self.yaw(module)
        
    def visit_r(self,module):
        self.roll(module)
        
    def visit_p(self,module):
        self.pitch(module)

    def visit_l(self, module):
        self.level(module)

    def visit_c(self,module):
        self.setColor(module)
        
    def visit_w(self,module):
        self.setWidth(module)
        
    def visit_F(self,module):
        self.forward(module)
            
    def visit_f(self,module):
        self.skip(module)

    def visit_O(self,module):
        self.saveStateInModule(module)

    def visit_Q(self,module):
        module.pos = self.state.getPos()
        module.dir = self.state.getDir()
        module.up = self.state.getUp()
        module.right = self.state.getRight()
        
    def visit_t(self,module):
        if not self.inPoly:
            print "Warning: t() outside of polygon!"
    
    def visit_PB(self,module):
        self.inPoly = True
        self.saveStateInModule(module)
        
    def visit_PE(self,module):
        self.inPoly = False

    def visit_LB(self,module):
        self.push()
        
    def visit_RB(self,module):
        self.pop()

    ## Additional methods
    def saveStateInModule(self,module):
        module.setData(self.state.copy())

    def restoreStateFromModule(module):
        self.state = module.getData()
        
    def push(self):
        self.trail.append(self.state.copy())
        
    def pop(self):
        self.state = self.trail.pop()

    def setData(self,module,data):
        module.setData(data)

    def forward(self,module):
        if self.inPoly:
            raise LException("F() not allowed inside a polygon")        
        # Order is important: Need start position in module but end position for subsequent calculations
        self.saveStateInModule(module)
        self.state.move(module.length)

    def skip(self,module):
        # Order is important: Need start position in module but end position for subsequent calculations
        if not self.inPoly:
            self.saveStateInModule(module)
            self.state.move(module.length)

    def yaw(self,module):
        if self.inPoly:
            raise LException("y() not allowed inside a polygon")
        self.state.yaw(module.angle)

    def roll(self,module):
        if self.inPoly:
            raise LException("r() not allowed inside a polygon")
        self.state.roll(module.angle)

    def pitch(self,module):
        if self.inPoly:
            raise LException("p() not allowed inside a polygon")
        self.state.pitch(module.angle)

    def level(self, module):
        if self.inPoly:
            raise LException("p() not allowed inside a polygon")
        self.state.level()

    def setColor(self,module):
        self.state.color = module.color

    def setWidth(self,module):
        self.state.width = module.width

if __name__ == "__main__":

    turtle = Turtle()
    f0 = F(100)
    f1 = F(100)
    f2 = F(100)
    p1 = p(45)
    turtle.visit_F(f0)
    turtle.visit_LB(LB())
    turtle.visit_p(p1)
    turtle.visit_F(f1)
    turtle.visit_RB(RB())
    turtle.visit_F(f2)
    print f0.getData()    
    print f1.getData()    
    print f2.getData()    
