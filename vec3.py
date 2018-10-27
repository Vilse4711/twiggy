import math

class Vec3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '(%s,%s,%s)' % (self.x, self.y, self.z)

    def __repr__(self):
        return 'Vec3(%s,%s,%s)' % (self.x, self.y, self.z)

    def __add__(self,other):
        return Vec3(self.x + other.x,
                    self.y + other.y,
                    self.z + other.z)

    def __sub__(self,other):
        return Vec3(self.x - other.x,
                    self.y - other.y,
                    self.z - other.z)

    def dot(self,other):
        other.mustBeVector()
        return self.x*other.x + self.y*other.y + self.z*other.z

    def __mul__(self,other):
        return self.dot(other)
    
    def cross(self,other):
        other.mustBeVector()
        return Vec3(self.y*other.z - self.z*other.y,
                    self.z*other.x - self.x*other.z,
                    self.x*other.y - self.y*other.x)

    def __pow__(self,other):
        return self.cross(other)
    
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def scale(self,factor):
        return Vec3(self.x*factor, self.y*factor, self.z*factor)

    def normalize(self):
        return self.scale(1.0/self.length())

    def __eq__(self,other):
        return abs(self.x-other.x)<Vec3.EPSILON and abs(self.y-other.y)<Vec3.EPSILON and abs(self.z-other.z)<Vec3.EPSILON

    def angle(self,other):
        try:
            a = math.degrees(math.acos(self*other))
        except:
            print self,other,self*other
            raise
        return a

    def rotate(self,vector,angle):
        if abs(vector.length() - 1) > Vec3.EPSILON:
            v = vector.normalize()
        else:
            v = vector
            
        x0,y0,z0 = v.x,v.y,v.z
        a = math.radians(angle)
        sina, cosa = math.sin(a),math.cos(a)
        x = self.x*(1+(1-cosa)*(x0*x0-1)) + self.y*(-z0*sina+(1-cosa)*x0*y0) + self.z*(y0*sina+(1-cosa)*x0*z0)
        y = self.x*(z0*sina+(1-cosa)*x0*y0) + self.y*(1+(1-cosa)*(y0*y0-1)) + self.z*(-x0*sina+(1-cosa)*y0*z0)
        z = self.x*(-y0*sina+(1-cosa)*x0*z0) + self.y*(x0*sina+(1-cosa)*y0*z0) + self.z*(1+(1-cosa)*(z0*z0-1))

        return Vec3(x,y,z)

    def colinear(self,other):
        return (1 - abs(self * other / (self.length()*other.length()))) < Vec3.EPSILON
    
    def mustBeVector(self):
        return self

    def isPoint(self):
        return False

    def isVector(self):
        return True
    
    def roundOff(self):
        return Vec3(round(self.x,Vec3.PRECISION), round(self.y,Vec3.PRECISION), round(self.z,Vec3.PRECISION))

    def toList(self):
        return [self.x,self.y,self.z]
    
Vec3.PRECISION = 5
Vec3.EPSILON = 0.000001
Vec3.ZERO = Vec3(0,0,0)
Vec3.UP = Vec3(0,1,0)
Vec3.RIGHT = Vec3(1,0,0)
Vec3.OUT = Vec3(0,0,1)

assert Vec3.RIGHT ** Vec3.UP == Vec3.OUT
assert Vec3.RIGHT.rotate(Vec3.OUT,90) == Vec3.UP
assert Vec3.RIGHT.rotate(Vec3.OUT.scale(2.0),90) == Vec3.UP

    
