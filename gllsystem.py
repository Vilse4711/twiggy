from glturtle import *
import time
import math
from vec3 import Vec3
import text

## Diffuse light
light_diffuse = [0.7, 0.7, 0.7, 1.0]

## Ambient light
light_ambient = [0.3, 0.3, 0.3, 1.0]

## Infinite light location
light_position = [-1.0, 1.0, 1.0, 0.0]

##
delta_t = 0.0
step = 0.001

class Viewer:
    def __init__(self,eye,lookat,distance):
        self.eye = eye
        self.lookat = lookat
        self.distance = distance

class MousePos:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hangle = 0
        self.vangle = 0
        self.rotate = False
        self.zoom = False

class Renderer:
    def __init__(self,lsystem,csg,*opt,**name):
        self.width = 1680
        self.hight = 1024
        self.viewer = Viewer(Vec3(-65.0, 35.0, 150.0),Vec3(0.0, 35.0, 0.0),150.0)
        self.mouse = MousePos(0,0)
        self.displayList = None
        self.compiled = False
        self.debug = False
        if 'scale' in name:
            self.scale = name['scale']
        else:
            self.scale = 1.0
        self.steps = 0
        self.lastDraw = 0
        self.lsystem = lsystem
        self.lastInterpreted = []
        if 'drawCSG' in opt and csg <> None:
            self.drawCSG = True
        else:
            self.drawCSG = False
        self.csg = csg
        # Positioning of text
        self.depthPos = Vec3(10,975,0)
        self.decompPos = Vec3(10,950,0)
        self.interpPos = Vec3(10,925,0)
        self.drawPos = Vec3(10,900,0)
    
    def display(self):
        decompTime = 0
        interpTime = 0
        drawTime = 0
        lsystem = self.lsystem
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # glRotatef(-90, 0.0, 1.0, 0.0)
        glScalef(self.scale*0.1,self.scale*0.1,self.scale*0.1)

        t = GLTurtle()

        if lsystem.getCurrentDepth() < lsystem.getDerivationDepth():

            t0 = time.clock()
            lsystem.produce()
            lsystem.decompose()
            decompTime = int((time.clock()-t0)*1000)

        if lsystem.getCurrentDepth() <= lsystem.getDerivationDepth() and not self.compiled:
            # glRotatef(90,0,0,1)
            t0 = time.clock()
            lastInterpreted = lsystem.interpret()
            interpTime = int((time.clock()-t0)*1000)

            t0 = time.clock()
            for module in lastInterpreted:
                module.accept(t)
            self.lastDraw = time.clock()
            drawTime = int((time.clock()-t0)*1000)
            
        if not self.compiled and lsystem.getCurrentDepth() == lsystem.getDerivationDepth():
            displayList = glGenLists(1)
            glNewList(displayList,GL_COMPILE)
            t.debug = self.debug
            #glRotatef(90,0,0,1)
            for module in lastInterpreted:
                module.accept(t)
            glEndList()
            self.displayList = displayList
            self.compiled = True
        elif lsystem.getCurrentDepth() == lsystem.getDerivationDepth():
            t0 = time.clock()
            glCallList(self.displayList)
            drawTime = int((time.clock()-t0)*1000)

        glPopMatrix()

        text.beginText()
        text.drawString(self.depthPos,"Derivation %s of %s" % (lsystem.getCurrentDepth(), lsystem.getDerivationDepth()))
        text.drawString(self.decompPos,"Rewrite: %sms" % decompTime)
        text.drawString(self.interpPos,"Interpret: %sms" % interpTime)
        text.drawString(self.drawPos,"Draw: %sms" % drawTime)
        text.endText()
     
        if self.drawCSG:
            glPushAttrib(GL_LIGHTING_BIT)
            glPushMatrix()
            # glRotatef(-90, 0.0, 1.0, 0.0)
            # glRotatef(90, 0.0, 0.0, 1.0)
            glScalef(self.scale*0.1,self.scale*0.1,self.scale*0.1)
            self.csg.draw(False)
            glPopMatrix()
            glPopAttrib()
        
        glutSwapBuffers()

    def idle(self):
        ## Interpolation
        global delta_t
        if delta_t > 1.0:
            delta_t = 0
        delta_t = delta_t + step
        t0 = time.clock()
        self.display()
        dt = round((time.clock() - t0),5)
        #print "Framerate:",1.0/dt

    def mouseFunc(self,button,state,x,y):
        self.mouse.x = x
        self.mouse.y = y
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse.rotate = True
            else:
                self.mouse.rotate = False
        elif button == GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse.zoom = True
            else:
                self.mouse.zoom = False

    def mouseMotionFunc(self,x,y):
        dx = self.mouse.x - x
        dy = self.mouse.y - y
        #print dy,dx
        dampx = 0.5
        dampy = 0.1
        if self.mouse.rotate:
            self.mouse.hangle = (self.mouse.hangle + dx*dampx)
            self.mouse.vangle = (self.mouse.vangle + dy*dampy)
            if self.mouse.vangle > 0:
                self.mouse.vangle = min(self.mouse.vangle,180)
            elif self.mouse.vangle < 0:
                self.mouse.vangle = max(self.mouse.vangle,-180)
                
            #print self.mouse.vangle
            self.viewer.eye.x = math.cos(math.radians(self.mouse.hangle))*self.viewer.distance
            self.viewer.eye.z = math.sin(math.radians(self.mouse.hangle))*self.viewer.distance
            self.viewer.eye.y = math.sin(math.radians(self.mouse.vangle))*self.viewer.distance
        elif self.mouse.zoom:
            pass
            #print self.viewer.distance
            #self.viewer.distance += 10*dy

        self._viewer()
        self.mouse.x = x
        self.mouse.y = y
        
    def keyboard(self,key,x,y):
        global g_system
        lsystem = self.lsystem
        if key == '+':
            lsystem.setDerivationDepth(lsystem.getDerivationDepth() + 1)
            glDeleteLists(self.displayList,1)
            self.compiled = False
        elif key == '-':
            depth = max(0,lsystem.getDerivationDepth()-1)
            lsystem.setDerivationDepth(depth)
            glDeleteLists(self.displayList,1)
            self.compiled = False
        elif key in '0':
            lsystem.reset()
            glDeleteLists(self.displayList,1)
            self.compiled = False
            return
        elif key == 'c':
            if  self.csg <> None:
                self.drawCSG = not self.drawCSG
        elif key == 'd':
            glDeleteLists(self.displayList,1)
            self.compiled = False
            self.debug = not self.debug
        elif key == ',':
            self.scale = max(0.1,self.scale/1.1)
            return
        elif key == '.':
            self.scale *= 1.1
            return
        else:
            print key
            return

        if lsystem.getCurrentDepth() > lsystem.getDerivationDepth():
            print lsystem.getCurrentDepth(),lsystem.getDerivationDepth()
            lsystem.reset()

    def _viewer(self):
        glLoadIdentity()
        gluLookAt(self.viewer.eye.x,
                  self.viewer.eye.y,
                  self.viewer.eye.z,
                  self.viewer.lookat.x,
                  self.viewer.lookat.y,
                  self.viewer.lookat.z,
                  0.0, 1.0, 0.0)
        
    def _viewSetup(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(self.width)/float(self.hight), 1.0, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        self._viewer()
        
    def init(self):
        ## /* Enable a single OpenGL light. */
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glClearColor(0.5,0.5,1.0,0.0)

        ## /* Use depth buffering for hidden surface elimination. */
        glEnable(GL_DEPTH_TEST)

        ## /* Setup the view */
        self._viewSetup()

    def render(self):
        """Surrender control to renderer"""
        glutInit([]);
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA)
        glutInitWindowSize(self.width,self.hight)
        glutCreateWindow("L-System Viewer")
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutMouseFunc(self.mouseFunc)
        glutMotionFunc(self.mouseMotionFunc)
        glutIdleFunc(self.idle)
        self.init()
        glutMainLoop()
        
if __name__ == "__main__":
    pass

          
