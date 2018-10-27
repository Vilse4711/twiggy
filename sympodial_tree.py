import sys
from module import *
from lsystem import LSystem
from production import Production
from context import FSC, ASC
from gllsystem import Renderer


#
# Sympodial trees - p. 59 in The Algorithmic Beauty of Plants
#

class A(Module):
    def __init__(self, length, width):
        self.length = length
        self.width = width

class B(Module):
    def __init__(self, length, width):
        self.length = length
        self.width = width

class P1(Production):
    def context(self):
        return FSC(None, [A], None)

    def produce(self, actuals, data):
        a = actuals.unpack(ASC.SP)

        return w(a.width),F(a.length), [y(data.a1), B(a.length*data.r1, a.width*data.wr)], r(180), [y(data.a2), B(a.length*data.r2,a.width*data.wr)]

class P2(Production):
    def context(self):
        return FSC(None, [B], None)

    def produce(self, actuals, data):
        a = actuals.unpack(ASC.SP)

        # Need to get support for the $ operator (page 57)
        return w(a.width), F(a.length), [p(data.a1), l(), B(a.length * data.r1, a.width * data.wr)], [p(-data.a2), l(), B(a.length * data.r2, a.width * data.wr)]


class Data:
    def __init__(self, r1, r2, a1, a2, wr):
        self.r1 = r1
        self.r2 = r2
        self.a1 = a1
        self.a2 = a2
        self.wr = wr


fig_a = Data(0.9, 0.7, 5, 65, 0.707)
fig_b = Data(0.9, 0.7, 10, 60, 0.707)
fig_c = Data(0.9, 0.8, 20, 50, 0.707)
fig_d = Data(0.9, 0.8, 35, 35, 0.707)

if __name__ == "__main__":
    # Run stand alone
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "<Data>"
        quit()
    data = eval(sys.argv[1])
    ls = LSystem(0, data)
    ls.declare(P1())
    ls.declare(P2())
    ls.setAxiom([A(100, 10)])
    ls.setDerivationDepth(10)
    Renderer(ls, None, scale=2.0).render()
