from vec3 import *
import math
import time

class LCS:
    def __init__(self):
        self.mat = [[1.0,0.0,0.0],
                    [0.0,1.0,0.0],
                    [0.0,0.0,1.0]]

    def copy(self):
        mat = LCS()
        mat[0][0] = self.mat[0][0]
        mat[0][1] = self.mat[0][1]
        mat[0][2] = self.mat[0][2]
        mat[1][0] = self.mat[1][0]
        mat[1][1] = self.mat[1][1]
        mat[1][2] = self.mat[1][2]
        mat[2][0] = self.mat[2][0]
        mat[2][1] = self.mat[2][1]
        mat[2][2] = self.mat[2][2]
        return mat
                
    def rowAsVec3(self,i):
        return Vec3(self.mat[i][0],self.mat[i][1],self.mat[i][2])

    def __getitem__(self,i):
        return self.mat[i]
    
    def rotX(self,angle):
        a = math.radians(angle)
        cosa = math.cos(a)
        sina = math.sin(a)
        mmm = [[self.mat[0][0],self.mat[0][1],self.mat[0][2]],
               [           0.0,           0.0,           0.0],
               [           0.0,           0.0,           0.0]]

        mmm[1][0] = cosa*self.mat[1][0]-sina*self.mat[2][0]
        mmm[1][1] = cosa*self.mat[1][1]-sina*self.mat[2][1]
        mmm[1][2] = cosa*self.mat[1][2]-sina*self.mat[2][2]
        
        mmm[2][0] = sina*self.mat[1][0]+cosa*self.mat[2][0]
        mmm[2][1] = sina*self.mat[1][1]+cosa*self.mat[2][1]
        mmm[2][2] = sina*self.mat[1][2]+cosa*self.mat[2][2]

        self.mat = mmm
        
    def rotY(self,angle):
        a = math.radians(angle)
        cosa = math.cos(a)
        sina = math.sin(a)
        mmm = [[           0.0,           0.0,           0.0],
               [self.mat[1][0],self.mat[1][1],self.mat[1][2]],
               [           0.0,           0.0,           0.0]]

        mmm[0][0] = cosa*self.mat[0][0]+sina*self.mat[2][0]
        mmm[0][1] = cosa*self.mat[0][1]+sina*self.mat[2][1]
        mmm[0][2] = cosa*self.mat[0][2]+sina*self.mat[2][2]
        
        mmm[2][0] = -sina*self.mat[0][0]+cosa*self.mat[2][0]
        mmm[2][1] = -sina*self.mat[0][1]+cosa*self.mat[2][1]
        mmm[2][2] = -sina*self.mat[0][2]+cosa*self.mat[2][2]

        self.mat = mmm
        
    def rotZ(self,angle):
        a = math.radians(angle)
        cosa = math.cos(a)
        sina = math.sin(a)
        mmm = [[           0.0,           0.0,           0.0],
               [           0.0,           0.0,           0.0],
               [self.mat[2][0],self.mat[2][1],self.mat[2][2]]]

        mmm[0][0] = cosa*self.mat[0][0]-sina*self.mat[1][0]
        mmm[0][1] = cosa*self.mat[0][1]-sina*self.mat[1][1]
        mmm[0][2] = cosa*self.mat[0][2]-sina*self.mat[1][2]
        
        mmm[1][0] = sina*self.mat[0][0]+cosa*self.mat[1][0]
        mmm[1][1] = sina*self.mat[0][1]+cosa*self.mat[1][1]
        mmm[1][2] = sina*self.mat[0][2]+cosa*self.mat[1][2]

        self.mat = mmm

    def orientation(self):
        r1 = self.mat[0]
        r2 = self.mat[1]
        r3 = self.mat[2]
        return [[r1[0],r1[1],r1[2],0.0],
                [r2[0],r2[1],r2[2],0.0],
                [r3[0],r3[1],r3[2],0.0],
                [0.0,0.0,0.0,1.0]]        

if __name__ == "__main__":

    cs = CS()
    i = 0
    t0 = time.clock()
    while i<1000:
        cs.roll(45.0)
        i+=1
    print time.clock()-t0


    m = Mat3()
    i = 0
    t0 = time.clock()
    while i<1000:
        m3.rotX(45.0)
        i+=1
    print time.clock()-t0
    print Mat3.count
