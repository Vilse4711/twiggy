import sys
from module import *
from lsystem import LSystem
from production import Production
from context import FSC,ASC
from gllsystem import Renderer

class A(Module):
    def __init__(self,length,width):
        self.length = length
        self.width = width

class I(Module):
    def __init__(self,length,factor):
        self.length = length
        self.factor = factor

    def interpret(self,data):
        return F(self.length,self.factor)
    
class P0(Production):
    def context(self):
        return FSC(None,[A],None)

    def produce(self,actuals,data):
        a = actuals.unpack(ASC.SP)
        w1 = a.width*pow(data.q,data.e)
        w2 = a.width*pow(1-data.q,data.e)
        f0 = max(w1,w2)/a.width

        if a.length >= data.m:
            return w(a.width),I(a.length,f0),[y(data.a1),r(data.f1),A(a.length*data.r1,w1)],[y(data.a2),r(data.f2),A(a.length*data.r2,w2)]
        else:
            return EPSILON
        
class Data:
    def __init__(self,r1,r2,a1,a2,f1,f2,w0,q,e,m):
        self.r1 = r1
        self.r2 = r2
        self.a1 = a1
        self.a2 = a2
        self.f1 = f1
        self.f2 = f2
        self.w0 = w0
        self.q = q
        self.e = e
        self.m = m

fig_a = Data(0.75,0.77,35,-35,0,0,30,0.5,0.4,0.0)
fig_b = Data(0.65,0.71,27,-68,0,0,20,0.53,0.50,1.7)
fig_f = Data(0.92,0.37,0,60,180,0,2,0.5,0.0,0.5)
fig_g = Data(0.8,0.8,30,-30,137,137,30,0.5,0.5,0.0)
fig_h = Data(0.95,0.75,5,-30,-90,90,40,0.6,0.45,25.0)
fig_i = Data(0.55,0.95,-5,30,137,137,5,0.4,0.0,5.0)

if __name__ == "__main__":
    # Run stand alone    
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "<Data>"
        quit()
    data = eval(sys.argv[1])
    ls = LSystem(0,data)
    ls.declare(P0())
    ls.setAxiom([A(100,data.w0)])
    ls.setDerivationDepth(10)
    Renderer(ls,None,scale=2.0).render()
