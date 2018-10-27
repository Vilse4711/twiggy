from lmodule import *
from lsystem import LSystem
from gllsystem import Renderer
from lcontext import FSC,ASC
from lproduction import LProduction
import random
import sys

def ypr(angle):
    return y(angle),p(angle),r(angle)

def leaf(time,dw,size):
    return [p(75),f(dw*time/2),L0(size)],[p(-75),f(dw*time/2),L0(size)]

def spiral(l,dw,la,ra):
    return p(la),F(l,dw),p(-la),r(ra)

class A(CompositeLModule):
    def __init__(self,time,dl,dw):
        self.t = time
        self.dl = dl
        self.dw = dw
        
    def __repr__(self):
        return "A(%s,%s,%s)" % (self.t,self.dl,self.dw)

    def interpret(self,data):
        return I(self.t,self.dl,self.dw)

    def decompose(self,data):
        k = random.randint(0,4)
        if self.t >= data.gp and k < 3:
            roll = random.choice([0,180])
            return I(self.t,self.dl,self.dw),[r(roll),y(65),B(1)],[r(roll),p(75),A(self.t-data.gp,0.5*self.dl,0.5*self.dw)],A(self.t-data.gp,self.dl,self.dw)
        elif self.t >= data.gp:
            return I(self.t,self.dl,self.dw),A(self.t-data.gp,self.dl,self.dw)
        else:
            return self

class I(CompositeLModule):
    def __init__(self,time,dl,dw):
        self.t = time
        self.dl = dl
        self.dw = dw

    def __repr__(self):
        return "I(%s,%s,%s)" % (self.t,self.dl,self.dw)

    def interpret(self,data):
        w0 = float(self.dw*max(1.0,(self.t+data.gp)))
        wN = float(self.dw*self.t)
        l0 = self.dl*min(data.gp,self.t)
        s0 = 5.0/data.gp*min(data.gp,self.t)
##        return w(w0),p(30),F(l0,wN/w0),leaf(self.t,self.dw,s0),p(-30),r(50)
        return w(w0),spiral(l0,wN/w0,30,50),leaf(self.t,self.dw,s0)

class B(CompositeLModule):
    def __init__(self,time):
        self.t = time

    def __repr__(self):
        return "B(%s)" % self.time

    def interpret(self,data):
        d = 90
        o = -65
        t = self.t
        gr = B.growthRate
        gp = B.growthPeriod
        s = B.size/gp*min(t,gp)
##        pc = (255.0/255.0,207.0/255.0,233.0/255.0)
        pc = (0.75,0.5,1)
        bc = (1,0.5,1)
        gc = (0,1,0)
        return c(gc),w(s/10),F(4*s),c(pc),[r(0),[p(o),L0(2*s)],r(d),[p(o),L0(2*s)],r(d),[p(o),L0(2*s)],r(d),[p(o),L0(2*s)]],f(s/2.0),c(bc),O(s/2.0)
B.growthRate = 1.1
B.growthPeriod = 10
B.size = 3.0

class L0(CompositeLModule):
    def __init__(self,size):
        self.size = size

    def __repr__(self):
        return "L0"

    def interpret(self,env):
        size = self.size
        # Polygons are drawn in the x/z-plane so we are constrained to yaw-rotations
        return PB(),t(-60),f(size),t(60),f(size),t(60),f(size),t(60),f(size),t(60),f(size),t(60),PE()

class P0(LProduction):
    def context(self):
        return FSC(None,[A],None)

    def produce(self,actuals,data):
        a = actuals.unpack(ASC.SP)
        return A(a.t+data.dt,a.dl,a.dw)        

class P1(LProduction):
    def context(self):
        return FSC(None,[I],None)

    def produce(self,actuals,data):
        i = actuals.unpack(ASC.SP)
        return I(i.t+data.dt,i.dl,i.dw)        

class P2(LProduction):
    def context(self):
        return FSC(None,[B],None)

    def produce(self,actuals,data):
        b = actuals.unpack(ASC.SP)
        return B(b.t+data.dt)        
    
class Data:
    def __init__(self,gp,dl,dw,dt):
        self.gp = gp
        self.dl = dl
        self.dw = dw
        self.dt = dt

data0 = Data(10,5,0.1,1)

ls = LSystem(int(sys.argv[1]),data0)
ls.declare(P0())
ls.declare(P1())
ls.declare(P2())
ls.setAxiom([A(1,data0.dl,data0.dw)])
ls.setDerivationDepth(100)
Renderer(ls,None,scale=2.75).render()
