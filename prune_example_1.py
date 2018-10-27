from vec3 import Vec3
import sys
import random
from csg import *
from module import *
from context import FSC,ASC
from production import LProduction
from gllsystem import Renderer
from lsystem import LSystem

bb1 =  Translation(Scaling(Sphere(),Vec3(300,300,300)),Vec3(150,0,0))
bb2 =  Translation(Scaling(Sphere(),Vec3(200,200,200)),Vec3(150,0,0))
bb3 =  Translation(Scaling(Cube(),Vec3(100,100,100)),Vec3(150,0,0))
bb4 =  Translation(Scaling(Cube(),Vec3(200,100,100)),Vec3(200,0,0))
bb5 =  Translation(Scaling(Sphere(),Vec3(100,200,200)),Vec3(150,0,0))
bb6 =  Translation(Scaling(Sphere(),Vec3(200,100,100)),Vec3(100,0,0))

bb9 = Complement(Translation(Scaling(Cube(),Vec3(200,100,100)),Vec3(100,-75,0)))
house_0 =  Complement(Scaling(Cube(),Vec3(250,100,100)))
house_1 = Translation(house_0,Vec3(125,0,-100))
house_2 = Translation(house_0,Vec3(125,0,100))
village_1 = Intersection(house_1,house_2)
village_2 = Intersection(Intersection(house_1,house_2),bb2)

class A(CompositeLModule):
    def __init__(self,k,l,w):
        self.k = k
        self.l = l
        self.w = w
        
    def __repr__(self):
        return "A(%s,%s,%s)" % (self.k,self.l,self.w)
            
    def interpret(self,data):
        return f(-self.l/2),L0(self.l)

class B(CompositeLModule):
    def __init__(self,m,n,l,w):
        self.m = m
        self.n = n
        self.l = l
        self.w = w
        
    def __repr__(self):
        return "B(%s,%s)" % (self.m,self.n)

##    def interpret(self,data):
##        return [p(45),w(1),F(data.ls/2),c((1,0,0)),W()]
##        return [p(45),w(1),F(data.ls/2),W()]
##        return [p(45),w(1),F(data.ls/2),L1(data.ls)]

class I(CompositeLModule):
    def __init__(self,length,factor):
        self.length = length
        self.factor = factor
        
    def interpret(self,data):
        return c((128/255.0,128/255.0,64/255.0)),F(self.length,self.factor)
    
class T(CompositeLModule):
    def __repr__(self):
        return "T()"

class S(CompositeLModule):
    def __repr__(self):
        return "S()"

##    def interpret(self,data):
##        return [c((1,1,0)),O(5)]
    
class W(CompositeLModule):
    def __repr__(self):
        return "W()"

    def interpret(self,data):
        # Polygons are drawn in the x/z-plane so we are constrained to yaw-rotations
        return [c((0,1,0)),PB(),t(-60),f(data.ls),t(60),f(data.ls),t(60),f(data.ls),t(60),f(data.ls),t(60),f(data.ls),t(60),PE()]

class L0(CompositeLModule):
    def __init__(self,length):
        self.length = length

    def __repr__(self):
        return "L0(%s)" % (self.length)

    def interpret(self,data):
        _l = self.length
        return f(_l/2),LB(),p(45),f(data.ls),W(),RB(),r(90),LB(),p(45),f(data.ls),W(),RB(),f(_l/2),r(90),LB(),p(45),f(data.ls),W(),RB(),r(90),LB(),p(45),f(data.ls),W(),RB()

class L1(CompositeLModule):
    def __init__(self,length):
        self.length = length

    def __repr__(self):
        return "L0(%s)" % (self.length)

    def interpret(self,data):
        _l = self.length
        return [p(45),L0(_l/2),RB(),r(90),LB(),p(45),L0(_l/2),RB(),r(90),f(_l/2),r(90),LB(),p(45),L0(_l/2),RB(),r(90),LB(),p(45),L0(_l/2)]

class P0(LProduction):
    def context(self):
        return FSC(None,[A],[Q])

    def produce(self,actuals,data):
        a = actuals.unpack(ASC.SP)
        q = actuals.unpack(ASC.RC)

        if a.l > data.min:
            choise = self.select(a.k)
            prune = self.prune(q,a.l,data.csg)
            if not prune and choise == 1:
                return w(a.w),r(data.gamma),[y(data.alpha),I(a.l,data.dw),A(a.k+1,a.l*data.dl,a.w*data.dw),Q()],y(-data.beta),I(a.l,data.dw),A(a.k+1,a.l*data.dl,a.w*data.dw)
            elif not prune and choise == 2:
                return w(a.w),r(data.gamma),B(a.k+1,a.k+1,a.l*data.dl,a.w*data.dw),y(-data.beta),I(a.l,data.dw),A(a.k+1,a.l*data.dl,a.w*data.dw)
            elif prune:
                return T(),CUT
        return a

    def prune(self,q,l,csg):
        if q.pos != None and csg != None:
            if not csg.inside(q.pos):
                return True
        return False
        
    def select(self,k):
        if k != 0 and random.random() <= max(0.0,(2.0*k+1)/(k*k)):
            return 1
        else:
            return 2

class P1(LProduction):
    def context(self):
        return FSC(None,[I],[T])

    def produce(self,actuals,data):
        return S()
        
class P2(LProduction):
    def context(self):
        return FSC(None,[I],[S])

    def produce(self,actuals,data):
        f = actuals.unpack(ASC.SP)
        print "Propagate"
        return S(),I(f.length,f.factor)

class P3(LProduction):
    def __init__(self):
        P4.i = 0
        
    def context(self):
        return FSC(None,[B],[S])

    def produce(self,actuals,data):
        b = actuals.unpack(ASC.SP)
        
        k = data.a*b.m+data.b*b.n+data.c
        P4.i += 1
        print "Wake up:", P4.i
        return [y(data.alpha),I(b.l,data.dw),A(k,b.l*data.dl,b.w*data.dw),Q()]

class P4(LProduction):
    def context(self):
        return FSC(None,[B],[I])

    def produce(self,actuals,data):
        b = actuals.unpack(ASC.SP)
        return B(b.m+1,b.n+1,b.l,b.w)        

class P5(LProduction):
    def context(self):
        return FSC(None,[S],None)

    def produce(self,actuals,data):
        return EPSILON
    
# Not in the rule set in the article "Synthetic Topiary"
class P6(LProduction):
    def context(self):
        return FSC(None,[T],None)

    def produce(self,actuals,data):
        return EPSILON

class Data:
    def __init__(self,alpha,beta,gamma,dl,dw,bs,m,ls,csg):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.dl = dl
        self.dw = dw
        self.budSize = bs
        self.min = m
        self.ls = ls
        self.a = 0
        self.b = 0
        self.c = 1
        self.csg = csg

data0 = Data(32.0,20.0,90.0,0.85,0.9,1.1,2.0,3,village_1)
data1 = Data(32.0,20.0,90.0,0.95,0.9,1.1,2.0,3,village_1)
data2 = Data(32.0,20.0,90.0,0.95,0.9,1.1,2.0,3,village_2)
data3 = Data(32.0,20.0,90.0,0.95,0.9,1.1,2.0,3,None)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: python %s <axiom> <data> <depth> <seed>" % sys.argv[0]
        print "Example: \"[w(10),F(100,0.5),A(1,25,5),Q()]\" data0 5 92333"
        quit()

    # Axiom on form: "[A(),Q()]"
    data = eval(sys.argv[2])
    maxDepth = int(sys.argv[3])
    axiom = eval(sys.argv[1])
    seed = int(sys.argv[4])
    ls = LSystem(seed,data)
    ls.setAxiom(axiom)
    ls.setDerivationDepth(maxDepth)
    ls.declare(P0())
    ls.declare(P1())
    ls.declare(P2())
    ls.declare(P3())
    ls.declare(P4())
    ls.declare(P5())
    ls.declare(P6())

    Renderer(ls,data.csg,'drawCSG',scale=2.0).render()


