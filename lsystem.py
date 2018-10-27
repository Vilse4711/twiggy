import random
import copy
from types import TupleType,ListType
from lexception import LException
from lmodule import *
from lproduction import LProduction
from lcontext import FSC
from lstring import LString
from lturtle import LTurtle

# Not same as encode as in lcontext
def flatten(modules):
    new = []
    for m in modules:
        if type(m) == ListType:
            new.append(LB())
            new.extend(flatten(m))
            new.append(RB())
        elif type(m) == TupleType:
            new.extend(flatten(m))
        else:
            new.append(m)
    return new

class LSystem:
    def __init__(self,seed,data):
        self._axiom = []
        self._currentDepth = 0
        self._derivationDepth = 0
        self._data = data
        self._lastInterpreted = []
        self._lstring = LString(copy.deepcopy(self._axiom))
        self._productions = []
        self._seed = seed
        self._nextSeed = self._seed
        self._reseed = True
        self._lastInterpreted = None
        self._ignore = LSystem.IGNORE
        self._consider = LSystem.CONSIDER
        
    def reset(self):
        self._reseed = True
        self._currentDepth = 0
        self._lstring = LString(copy.deepcopy(self._axiom))
        self._lastInterpreted = None

    def declare(self,production):
        if not isinstance(production,LProduction):
            raise LException("LSystem.declare(): %s is not an LProduction" % production)
        
        formals = production.context()
        if not formals.encoded():
            formals.encode()
        self._productions.append((formals,production))

    def setDerivationDepth(self,depth):
        self._derivationDepth = depth

    def getDerivationDepth(self):
        return self._derivationDepth
    
    def getCurrentDepth(self):
        return self._currentDepth
    
    def setAxiom(self,axiom):
        self._axiom = copy.deepcopy(flatten(axiom))
        self.reset()

    def getLastInterpreted(self):
        return self._lastInterpreted

    def ignore(self,spec):
        """spec is a list or tuple of LModule classes"""
        self._ignore = tuple(spec)

    def consider(self,spec):
        """spec is a list or tuple of LModule classes"""
        self._consider = tuple(spec)

    def derive(self):
        """Fully derive L-System"""
        for i in range(self._derivationDepth):
            self.produce()
            self.decompose()
            self.interpret()
        
    def produce(self):
        pos = 0
        current = self._lstring
        new = LString([])
        skip = 0
        self._lastInterpreted = None

        if self._reseed:
            self._nextSeed = self._seed
            self._reseed = False
        random.seed(self._nextSeed)
        self._nextSeed = random.randint(0,pow(2,31))
        
        while pos < len(current):
            m = current[pos]
            if m == CUT:
                skip = 1

            if skip == 1 and isinstance(m,RB):
                skip = 0
            elif skip > 0:
                if isinstance(m,LB):
                    skip = skip + 1
                elif isinstance(m,RB):
                    skip = skip - 1
                continue

            found = False
            for formals,production in self._productions:
                actuals = formals.match(current,pos,self._consider,self._ignore)
                if actuals <> None:
                    # We found a matching production and need to apply it
                    found = True
                    p = production.produce(actuals,self._data)
                    if p == None:
                        # Viewed as a bug in the production implementation
                        raise LException("Production %s return NoneType object" % production)
                    else:
                        # We have a proper production
                        if type(p) == TupleType:
                            new.extend(flatten(p))
                        elif type(p) == ListType:
                            new.extend(flatten([p]))
                        elif p == EPSILON:
                            # Empty production so we just toss it
                            pass
                        else:
                            new.append(p)
                    break
            if not found:
                # We found no matching production and need to apply the identity production instead
                new.append(current[pos])    
            pos = pos + 1
        self._lstring = new
        self._currentDepth += 1
        return self._lstring

    def decompose(self):
        self._lastInterpreted = None
        s =_decompose(self._lstring,self._data)
        self._lstring = s
        return self._lstring
            
    def interpret(self):
        if self._lastInterpreted <> None:
            return self._lastInterpreted
        
        self._lastInterpreted = _interpret(self._lstring,self._data,LTurtle())
        return self._lastInterpreted
    
def _decompose(lstring,data):
    new = LString([])
    skip = 0
    for m in lstring:
        if m == CUT and skip == 0:
            skip = 1

        if skip == 1 and isinstance(m,RB):
            skip = 0
        elif skip > 0:
            if isinstance(m,LB):
                skip = skip + 1
            elif isinstance(m,RB):
                skip = skip - 1
            continue
        
        d = m.decompose(data)
        if d == None:
            raise LException("NoneType object returned as a result of %s.decompose()" % m)
        elif type(d) == TupleType:
            new.extend(_decompose(LString(flatten(d)),data))
        elif type(d) == ListType:
            new.extend(_decompose(LString(flatten([d])),data))
        elif d == EPSILON:
            continue
        elif isinstance(d,LModule):
            if d == m:
                # Fixed point
                new.append(d)
            else:
                new.extend(_decompose(LString([d])))
        else:
            raise LException("Unknown object %s returned during %s.decompose()" % (d,m))

    return new

def _interpret(lstring,data,turtle):
    new = LString([])
    for m in lstring:
        d = m.interpret(data)
        if d == None:
            raise LException("NoneType object returned as a result of %s.interpret()" % m)
        elif type(d) == TupleType:
            new.extend(_interpret(LString(flatten(d)),data,turtle))
        elif type(d) == ListType:
            new.extend(_interpret(LString(flatten([d])),data,turtle))
        elif d == EPSILON:
            continue
        elif isinstance(d,PrimitiveLModule):
            d.accept(turtle)
            new.append(d)
        elif isinstance(d,LModule):
            new.extend(_interpret(LString([d]),data,turtle))
        else:
            raise LException("Unknown object %s returned during %s.decompose()" % (d,m))

    return new

LSystem.CONSIDER = tuple()
LSystem.IGNORE = tuple([y,p,r,c,w,MetaModule])


            
