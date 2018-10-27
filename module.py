from lexception import LException

class BaseModule:
    """Base L-System Module class"""
    def decompose(self,data):
        """Recursively decompose the LModule until a fixed point is reached"""
        return EPSILON
    
    def interpret(self,env):
        """Interpret the LModule into primitive modules"""
        return EPSILON

    def accept(self,v):
        """Support visitor pattern by overriding this method"""
        # Default behavior is to ignore visitors
        print "Warning: attempting to visit an LModule that does not accept visitors!"

    def setData(self,data):
        """Allows for data to be associated with an LModule"""
        self._data = data

    def getData(self):
        """Retrieve data associated with an LModule"""
        return self._data

class MetaModule(BaseModule):
    """Markers"""
CUT = MetaModule() # Denotes throw away the rest of the branch
EPSILON = MetaModule() # Denotes the empty successor
FAIL = MetaModule() # Denotes cond failing in, lc < pred > rc : cond --> succ
   
class PrimitiveModule(BaseModule):
    """Abstract primitive L-System Module class"""
    def decompose(self,data):
        # Default behavior is identity decomposition
        return self

    def interpret(self,data):
        # Default behavior is identity interpretation
        return self
    
    def accept(self,v):
        # PrimitiveLModules has to override this
        raise LException("Abstract method")
        
class Module(BaseModule):
    """Abstract composite L-System Module class from which all non primitive modules should be derived from"""
    def decompose(self,data):
        # Default behavior is identity
        return self
    
    def interpret(self,env):
        # Default behavior is to disappear
        return EPSILON
    
# Set roll
class r(PrimitiveModule):
    """Specifies a rotation around the forward-axis, i.e. Roll"""
    
    def __init__(self,angle):
        self.angle = angle

    def __repr__(self):
        return "r(%s)" % (self.angle)

    def accept(self,v):
        v.visit_r(self)

# Set yaw
class y(PrimitiveModule):
    """Specifies a rotation around the up-axis, i.e. Yaw"""
    
    def __init__(self,angle):
        self.angle = angle

    def __repr__(self):
        return "y(%s)" % (self.angle)

    def accept(self,v):
        v.visit_y(self)

# Set pitch
class p(PrimitiveModule):
    """Specifies a rotation around the right-axis, i.e. Pitch"""
        
    def __init__(self,angle):
        self.angle = angle

    def __repr__(self):
        return "p(%s)" % (self.angle)

    def accept(self,v):
        v.visit_p(self)

# Level $-operator
class l(PrimitiveModule):
    """Levels the turtle"""

    def __init__(self):
        pass

    def __repr__(self):
        return "l()"

    def accept(self, v):
        v.visit_l(self)


# Set width
class w(PrimitiveModule):
    """Specifies width"""
    
    def __init__(self,width):
        self.width = width

    def __repr__(self):
        return "w(%s)" % (self.width)

    def accept(self,v):
        v.visit_w(self)


# Set color
class c(PrimitiveModule):
    """Specifies color"""
    
    def __init__(self,color):
        self.color = color

    def __repr__(self):
        return "c(%s,%s,%s)" % self.color

    def accept(self,v):
        v.visit_c(self)

class F(PrimitiveModule):
    """Specifies continuous growth of length"""
    
    def __init__(self,length,*args):
        self.state = None
        self.length = length
        if len(args) > 0:
            self.factor = args[0]
        else:
            self.factor = 1.0

    def __repr__(self):
        return "F(%s,%s)" % (self.length,self.factor)
    
    def accept(self,v):
        v.visit_F(self)

class f(PrimitiveModule):
    """Specifies a jump of length. Records vertex if in polygon"""
    
    def __init__(self,length):
        self.state = None
        self.length = length

    def __repr__(self):
        return "f(%s)" % (self.length)
    
    def accept(self,v):
        v.visit_f(self)

class O(PrimitiveModule):
    """Specifies a sphere"""

    def __init__(self,radius):
        self.state = None
        self.radius = radius

    def __repr__(self):
        return "O(%s)" % (self.radius)
    
    def accept(self,v):
        v.visit_O(self)

class Q(PrimitiveModule):
    """Query module"""
    def __init__(self):
        self.pos = None
        self.dir = None
        self.up = None
        self.right = None

    def __repr__(self):
        return "Q(%s,%s,%s,%s)" % (self.pos,self.dir,self.up,self.right)
    
    def accept(self,v):
        v.visit_Q(self)

class t(PrimitiveModule):
    """Turning inside a polygon"""
    def __init__(self,angle):
        self.angle = angle

    def __repr__(self):
        return "t(%s)" % (self.angle)

    def accept(self,v):
        v.visit_t(self)
        
class PB(PrimitiveModule):
    def __init__(self):
        self.state = None

    def __repr__(self):
        return "PB()"

    def accept(self,v):
        v.visit_PB(self)

class PE(PrimitiveModule):
    def __repr__(self):
        return "PE()"

    def accept(self,v):
        v.visit_PE(self)
            
class LB(PrimitiveModule):
    def __repr__(self):
        return "LB()"

    def accept(self,v):
        v.visit_LB(self)
        
class RB(PrimitiveModule):
    def __repr__(self):
        return "RB()"

    def accept(self,v):
        v.visit_RB(self)
    
if __name__ == "__main__":
    pass

    

