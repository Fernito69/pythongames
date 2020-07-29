#imports
import os
import time
import math

os.system("cls")

global fps
fps = 60

global x_resolution
global y_resolution
global distanceToSpec
#global screenWidth
#global screenHeight
global aspectRatio
global dist_fog
x_resolution = 200
y_resolution = 50
distanceToSpec = 100         #fov^-1
#screenWidth = 10
#screenHeight = 5
aspectRatio = 1.78           #aspect ratio of characters in console
dist_fog = 13                 #how quickly the characters change when objects get closer to the spectator


class Entity():

    def __init__(self, position=[0,0,0], size=1, angle=[0,0,0], movMatrix=[0,0,0], rotMatrix=[0,0,0]):
        pass

    def movement(self):        
        self.position[0] += self.movMatrix[0]
        self.position[1] += self.movMatrix[1]        
        self.position[2] += self.movMatrix[2]
        
        self.angle[0] -= self.rotMatrix[0]
        self.angle[1] -= self.rotMatrix[1]
        self.angle[2] -= self.rotMatrix[2]
    
    def apply_rotations(self, vertexes):

        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        s = self.size        
        aX = math.radians(self.angle[0])
        aY = math.radians(self.angle[1])
        aZ = math.radians(self.angle[2])

        #XY
        orig = []
        for i in range(len(vertexes)):
            orig.append(vertexes[i][:])

        for i in range(len(vertexes)):            
            vertexes[i][0] =  (orig[i][0] - x)*math.cos(aX) + (orig[i][1] - y)*math.sin(aX) + x
            vertexes[i][1] =  -(orig[i][0] - x)*math.sin(aX) + (orig[i][1] - y)*math.cos(aX) + y
        
        #XZ        
        orig = []
        for i in range(len(vertexes)):
            orig.append(vertexes[i][:])

        for i in range(len(vertexes)):               
            vertexes[i][0] =  (orig[i][0] - x)*math.cos(aY) + (orig[i][2] - z)*math.sin(aY) + x
            vertexes[i][2] =  -(orig[i][0] - x)*math.sin(aY) + (orig[i][2] - z)*math.cos(aY) + z

        #YZ
        orig = []
        for i in range(len(vertexes)):
            orig.append(vertexes[i][:])
        
        for i in range(len(vertexes)):              
            vertexes[i][1] =  (orig[i][1] - y)*math.cos(aZ) + (orig[i][2] - z)*math.sin(aZ) + y
            vertexes[i][2] =  -(orig[i][1] - y)*math.sin(aZ) + (orig[i][2] - z)*math.cos(aZ) + z
        
        return vertexes

################

class Cube(Entity):

    def __init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0]):
        Entity.__init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0])        
        self.position       = position
        self.size           = size
        self.angle          = angle #XY, XZ, YZ
        self.movMatrix      = movMatrix
        self.rotMatrix      = rotMatrix

    def calc_vertexes(self):
        vertexes = []
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        s = self.size        
        
        vertexes.append([x + s/2, y + s/2, z + s/2])
        vertexes.append([x + s/2, y - s/2, z + s/2])
        vertexes.append([x - s/2, y + s/2, z + s/2])
        vertexes.append([x - s/2, y - s/2, z + s/2])
        vertexes.append([x + s/2, y + s/2, z - s/2])
        vertexes.append([x + s/2, y - s/2, z - s/2])
        vertexes.append([x - s/2, y + s/2, z - s/2])
        vertexes.append([x - s/2, y - s/2, z - s/2])
        
        #"voxels" for the edges 
        for i in range(s):
            vertexes.append([x + s/2 - i, y + s/2    , z + s/2])
            vertexes.append([x + s/2    , y + s/2 - i, z + s/2])
            vertexes.append([x + s/2    , y + s/2    , z + s/2 - i])
            
            vertexes.append([x - s/2, y + s/2 - i, z + s/2])
            vertexes.append([x - s/2, y + s/2    , z + s/2 - i])
            
            vertexes.append([x + s/2 - i, y - s/2, z + s/2])
            vertexes.append([x + s/2    , y - s/2, z + s/2 - i])

            vertexes.append([x + s/2 - i, y + s/2    , z - s/2])
            vertexes.append([x + s/2    , y + s/2 - i, z - s/2])

            vertexes.append([x + s/2 - i, y + s/2    , z - s/2])
            vertexes.append([x + s/2    , y + s/2 - i, z - s/2])

            vertexes.append([x + s/2 - i, y - s/2    , z - s/2])
            vertexes.append([x - s/2    , y + s/2 - i, z - s/2])
            vertexes.append([x - s/2    , y - s/2    , z + s/2 - i])
        
        return self.apply_rotations(vertexes)

################  

class Tetra(Entity):

    def __init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0]):
        Entity.__init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0])        
        self.position       = position
        self.size           = size
        self.angle          = angle #XY, XZ, YZ
        self.movMatrix      = movMatrix
        self.rotMatrix      = rotMatrix

    def calc_vertexes(self):
        vertexes = []
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        r = .707
        s = self.size        
        
        vertexes.append([x + s, y, z - r*s])
        vertexes.append([x - s, y, z - r*s])
        vertexes.append([x, y + s, z + r*s])
        vertexes.append([x, y - s, z + r*s])

        for t in range(s*2):
            vertexes.append([(x - s + t), (y), (z - r*s)])           #1 - 2
            vertexes.append([(x + s - t/2), (y + t/2), (z - r*s + r*t)]) #1 - 3
            vertexes.append([(x + s - t/2), (y - t/2), (z - r*s + r*t)]) #1 - 4
            vertexes.append([(x - s + t/2), (y + t/2), (z - r*s + r*t)]) #2 - 3
            vertexes.append([(x - s + t/2), (y - t/2), (z - r*s + r*t)]) #2 - 4
            vertexes.append([(x), (y - s + t), (z + r*s)])           #3 - 4       
        
        return self.apply_rotations(vertexes)

################

class Ico(Entity):

    def __init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0]):
        Entity.__init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0])        
        self.position       = position
        self.size           = size
        self.angle          = angle #XY, XZ, YZ
        self.movMatrix      = movMatrix
        self.rotMatrix      = rotMatrix

    def calc_vertexes(self):
        vertexes = []
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        s = self.size
        phi = 1.618
        
        vertexes.append([x, y + s, z + phi*s,"1"]) #vertex 1
        vertexes.append([x, y - s, z + phi*s,"2"]) #vertex 2
        vertexes.append([x, y + s, z - phi*s,"3"]) #vertex 3
        vertexes.append([x, y - s, z - phi*s,"4"]) #vertex 4

        vertexes.append([x + s, y + phi*s, z,"5"]) #vertex 5
        vertexes.append([x + s, y - phi*s, z,"6"]) #vertex 6
        vertexes.append([x - s, y + phi*s, z,"7"]) #vertex 7
        vertexes.append([x - s, y - phi*s, z,"8"]) #vertex 8

        vertexes.append([x + phi*s, y, z + s,"9"]) #vertex 9
        vertexes.append([x + phi*s, y, z - s,"X"]) #vertex 10
        vertexes.append([x - phi*s, y, z + s, "J"]) #vertex 11
        vertexes.append([x - phi*s, y, z - s, "Q"]) #vertex 12 

        #edges of icosahedron
        for t in range(s): 
            
            vertexes.append([(x), (y + s - 2*t), (z + phi*s),"."])                         #vertex 1 - 2
            vertexes.append([(x + t), (y + s - t*(1-phi)), (z + phi*s - phi*t),"."])        #vertex 1 - 5
            vertexes.append([(x - t), (y + s - t*(1-phi)), (z + phi*s - phi*t),"."])       #vertex 1 - 7
            vertexes.append([(x + phi*t), (y + s - t), (z + phi*s - t*(phi-1)),"."])        #vertex 1 - 9
            vertexes.append([(x - phi*t), (y + s - t), (z + phi*s - t*(phi-1)),"."])       #vertex 1 - 11

            vertexes.append([(x + phi*t), (y - s + t), (z + phi*s - t*(phi-1)),"."])       #vertex 2 - 9
            vertexes.append([(x + t), (y - s + t*(1-phi)), (z + phi*s - phi*t),"."])       #vertex 2 - 6
            vertexes.append([(x - t), (y - s + t*(1-phi)), (z + phi*s - phi*t),"."])       #vertex 2 - 8
            vertexes.append([(x - phi*t), (y - s + t), (z + phi*s - t*(phi-1)),"."])       #vertex 2 - 11

            vertexes.append([(x + t), (y + s - t*(1-phi)), (z - phi*s + phi*t),"."])       #vertex 3 - 5
            vertexes.append([(x), (y + s - 2*t), (z - phi*s),"."])                          #vertex 3 - 4
            vertexes.append([(x - t), (y + s - t*(1-phi)), (z - phi*s + phi*t),"."])       #vertex 3 - 7
            vertexes.append([(x + phi*t), (y + s - t), (z - phi*s + t*(phi-1)),"."])        #vertex 3 - 10
            vertexes.append([(x - phi*t), (y + s - t), (z - phi*s + t*(phi-1)),"."])        #vertex 3 - 12            

            vertexes.append([(x + t), (y - s + t*(1-phi)), (z - phi*s + phi*t),"."])        #vertex 4 - 6
            vertexes.append([(x - t), (y - s + t*(1-phi)), (z - phi*s + phi*t),"."])        #vertex 4 - 8
            vertexes.append([(x + phi*t), (y - s + t), (z - phi*s + t*(phi-1)),"."])        #vertex 4 - 10
            vertexes.append([(x - phi*t), (y - s + t), (z - phi*s + t*(phi-1)),"."])        #vertex 4 - 12

            vertexes.append([(x + s - 2*t), (y + phi*s), (z),"."])                         #vertex 5 - 7
            vertexes.append([(x + s - t*(1-phi)), (y + phi*s - phi*t), (z + t),"."])        #vertex 5 - 9
            vertexes.append([(x + s - t*(1-phi)), (y + phi*s - phi*t), (z - t),"."])        #vertex 5 - 10

            vertexes.append([(x + s - 2*t), (y - phi*s), (z),"."])                          #vertex 6 - 8
            vertexes.append([(x + s - t*(1-phi)), (y - phi*s + phi*t), (z + t),"."])        #vertex 6 - 9
            vertexes.append([(x + s - t*(1-phi)), (y - phi*s + phi*t), (z - t),"."])        #vertex 6 - 10

            vertexes.append([(x - s + t*(1-phi)), (y + phi*s - phi*t), (z + t),"."])        #vertex 7 - 11
            vertexes.append([(x - s + t*(1-phi)), (y + phi*s - phi*t), (z - t),"."])        #vertex 7 - 12

            vertexes.append([(x - s + t*(1-phi)), (y - phi*s + phi*t), (z + t),"."])        #vertex 8 - 11
            vertexes.append([(x - s + t*(1-phi)), (y - phi*s + phi*t), (z - t),"."])        #vertex 8 - 12

            vertexes.append([(x + phi*s), (y), (z + s - 2*t),"."])                          #vertex 9 - 10

            vertexes.append([(x - phi*s), (y), (z + s - 2*t),"."])                          #vertex 11 - 12

        return self.apply_rotations(vertexes)
        
################

class Dodeca(Entity):

    def __init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0]):
        Entity.__init__(self, position, size, angle, movMatrix=[0,0,0], rotMatrix=[0,0,0])        
        self.position       = position
        self.size           = size
        self.angle          = angle #XY, XZ, YZ
        self.movMatrix      = movMatrix
        self.rotMatrix      = rotMatrix

    def calc_vertexes(self):
        vertexes = []
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        s = self.size
        phi = 1.618
        iphi = .618
        
        vertexes.append([x + s, y + s, z + s,"1"]) #vertex 1
        vertexes.append([x + s, y - s, z + s,"2"]) #vertex 2
        vertexes.append([x + s, y + s, z - s,"3"]) #vertex 3
        vertexes.append([x + s, y - s, z - s,"4"]) #vertex 4
        vertexes.append([x - s, y + s, z + s,"5"]) #vertex 5
        vertexes.append([x - s, y - s, z + s,"6"]) #vertex 6
        vertexes.append([x - s, y + s, z - s,"7"]) #vertex 7
        vertexes.append([x - s, y - s, z - s,"8"]) #vertex 8

        vertexes.append([x, y + phi*s, z + iphi*s,"9"]) #vertex 9
        vertexes.append([x, y - phi*s, z + iphi*s,"A"]) #vertex 10
        vertexes.append([x, y + phi*s, z - iphi*s,"B"]) #vertex 11
        vertexes.append([x, y - phi*s, z - iphi*s,"C"]) #vertex 12

        vertexes.append([x + iphi*s, y, z + phi*s,"D"]) #vertex 13
        vertexes.append([x + iphi*s, y, z - phi*s,"E"]) #vertex 14
        vertexes.append([x - iphi*s, y, z + phi*s,"F"]) #vertex 15
        vertexes.append([x - iphi*s, y, z - phi*s,"G"]) #vertex 16

        vertexes.append([x + phi*s, y + iphi*s, z,"H"]) #vertex 17
        vertexes.append([x + phi*s, y - iphi*s, z,"I"]) #vertex 18
        vertexes.append([x - phi*s, y + iphi*s, z,"J"]) #vertex 19
        vertexes.append([x - phi*s, y - iphi*s, z,"K"]) #vertex 20
        

        #edges of dodecahedron
        for t in range(s): 
            vertexes.append([(x + s - t), (y + s - t*(1-phi)), (z + s - t*(1-iphi)),"."]) #vertex 1 - 9
            vertexes.append([(x + s - t*(1-iphi)), (y + s - t), (z + s - t*(1-phi)),"."]) #vertex 1 - 13
            vertexes.append([(x + s - t*(1-phi)), (y + s - t*(1-iphi)), (z + s - t),"."]) #vertex 1 - 17

            vertexes.append([(x + s - t), (y - s + t*(1-phi)), (z + s - t*(1-iphi)),"."]) #vertex 2 - 10
            vertexes.append([(x + s - t*(1-iphi)), (y - s + t), (z + s - t*(1-phi)),"."]) #vertex 2 - 13
            vertexes.append([(x + s - t*(1-phi)), (y - s + t*(1-iphi)), (z + s - t),"."]) #vertex 2 - 18 3HBE

            vertexes.append([(x + s - t), (y + s - t*(1-phi)), (z - s + t*(1-iphi)),"."]) #vertex 3 - 11
            vertexes.append([(x + s - t*(1-iphi)), (y + s - t), (z - s + t*(1-phi)),"."]) #vertex 3 - 14
            vertexes.append([(x + s - t*(1-phi)), (y + s - t*(1-iphi)), (z - s + t),"."]) #vertex 3 - 17 4CEI

            vertexes.append([(x + s - t), (y - s + t*(1-phi)), (z - s + t*(1-iphi)),"."]) #vertex 4 - 12
            vertexes.append([(x + s - t*(1-iphi)), (y - s + t), (z - s + t*(1-phi)),"."]) #vertex 4 - 14
            vertexes.append([(x + s - t*(1-phi)), (y - s + t*(1-iphi)), (z - s + t),"."]) #vertex 4 - 18 59FJ

            vertexes.append([(x - s + t), (y + s - t*(1-phi)), (z + s - t*(1-iphi)),"."]) #vertex 5 - 9
            vertexes.append([(x - s + t*(1-iphi)), (y + s - t), (z + s - t*(1-phi)),"."]) #vertex 5 - 15
            vertexes.append([(x - s + t*(1-phi)), (y + s - t*(1-iphi)), (z + s - t),"."]) #vertex 5 - 19 6AFK

            vertexes.append([(x - s + t), (y - s + t*(1-phi)), (z + s - t*(1-iphi)),"."]) #vertex 6 - 10
            vertexes.append([(x - s + t*(1-iphi)), (y - s + t), (z + s - t*(1-phi)),"."]) #vertex 6 - 15
            vertexes.append([(x - s + t*(1-phi)), (y - s + t*(1-iphi)), (z + s - t),"."]) #vertex 6 - 20 7BGJ

            vertexes.append([(x - s + t), (y + s - t*(1-phi)), (z - s + t*(1-iphi)),"."]) #vertex 7 - 11
            vertexes.append([(x - s + t*(1-iphi)), (y + s - t), (z - s + t*(1-phi)),"."]) #vertex 7 - 16
            vertexes.append([(x - s + t*(1-phi)), (y + s - t*(1-iphi)), (z - s + t),"."]) #vertex 7 - 19 8CGK

            vertexes.append([(x - s + t), (y - s + t*(1-phi)), (z - s + t*(1-iphi)),"."]) #vertex 8 - 12
            vertexes.append([(x - s + t*(1-iphi)), (y - s + t), (z - s + t*(1-phi)),"."]) #vertex 8 - 16
            vertexes.append([(x - s + t*(1-phi)), (y - s + t*(1-iphi)), (z - s + t),"."]) #vertex 8 - 20

            vertexes.append([(x), (y + phi*s), (z + iphi*s - 2*iphi*t),"."]) #vertex 9 - 11
            vertexes.append([(x), (y - phi*s), (z + iphi*s - 2*iphi*t),"."]) #vertex 10 - 12
            vertexes.append([(x + iphi*s - 2*iphi*t), (y), (z - phi*s),"."]) #vertex 13 - 15
            vertexes.append([(x + iphi*s - 2*iphi*t), (y), (z + phi*s),"."]) #vertex 14 - 16
            vertexes.append([(x + phi*s), (y + iphi*s - 2*iphi*t), (z),"."]) #vertex 17 - 18
            vertexes.append([(x - phi*s), (y + iphi*s - 2*iphi*t), (z),"."]) #vertex 19 - 20

        return self.apply_rotations(vertexes)

################

class Player():

    def __init__(self, position, angle):

        self.position       = position      
        self.angle          = angle  

### where things are rendered
class Playfield():

    def __init__(self):
        pass

    def print_playfield(self,player,objects):

        #we make a matrix representation of the playfield
        screen_matrix = []

        for y in range(y_resolution):
            screen_matrix.append([])
            for x in range(x_resolution):
                screen_matrix[y].append(" ")

        #we draw the border of the screen
        screen_matrix[0][0]   = "╔" 
        screen_matrix[y_resolution - 1][x_resolution - 1] = "╝" 
        screen_matrix[0][x_resolution - 1]  = "╗"
        screen_matrix[y_resolution - 1][0]  = "╚"

        for y in range (1,y_resolution - 1):
            screen_matrix[y][0]  = "║"
            screen_matrix[y][x_resolution - 1] = "║"

        for x in range (1,x_resolution - 1):
            screen_matrix[0][x] = "═"
            screen_matrix[y_resolution - 1][x] = "═"

            
        #rendering objects
        for obj in objects:

            #calculate movement
            obj.movement()

            #we get vertexes from object
            objVertexes = obj.calc_vertexes()            

            #we add the vertexes to the screen matrix
            for vertex in objVertexes:

                vX = vertex[0]
                vY = vertex[1] if vertex[1] != 0 else 0.001
                vZ = vertex[2]

                xPos = int(round(vX * distanceToSpec / vY) + round(x_resolution/2)) if vY > 0 else 0
                yPos = int(round((vZ * distanceToSpec / vY) + round(y_resolution/2))/aspectRatio) if vY > 0 else 0
                
                if yPos < y_resolution and xPos < x_resolution and xPos > 0 and yPos > 0:
                                        
                    #calculate distance between point and observer
                    d = (vX**2 + vY**2 + vZ**2)**.5

                    # according to this distance, choose character
                    chars = '█▓@Øø*°,.¸'
                    
                    #if its x,y coordinates are negative, just don't draw the character
                    index = int(math.floor(d/dist_fog)) if int(math.floor(d/dist_fog)) >= 0 else 0
                    index = index if index <= 9 else 9

                    defchar = chars[index]
                    
                                                     
                    #checks if another vertex has been drawn in the specified coord and draws only the one closest to the spectator                    
                    if screen_matrix[yPos][xPos] != " ": 
                        if screen_matrix[yPos][xPos] not in chars[:index] and screen_matrix[yPos][xPos] not in "║═╚╝╔╗":
                            screen_matrix[yPos][xPos] = defchar 
                    else:
                        screen_matrix[yPos][xPos] = defchar                     
                    
                    #just for debugging (shows vertex number)
                    #screen_matrix[yPos][xPos] = vertex[3]                   

        
        #we convert the screen matrix into a string, so we can print it
        matrix_string = ""

        for y in range(y_resolution):
            for x in range(x_resolution):
                matrix_string += screen_matrix[y][x]
            if y < y_resolution - 1:
                matrix_string += "\n"

        os.system("cls")
        print(matrix_string)        


#we initialize classes
player     = Player([0,0,0],0)
playfield  = Playfield()

#cube1      = Cube(position=[-40,100,20], size=50, angle=[0,0,0], movMatrix=[0,2,0], rotMatrix=[2,2,2])
#cube2      = Cube(position=[150,300,-50], size=40, angle=[0,0,0], movMatrix=[-1,-.8,.5], rotMatrix=[2,10,2])
#cube3      = Cube(position=[-80,80,10], size=10, angle=[0,30,0], movMatrix=[1,-.5,0], rotMatrix=[2,0,5])
ico1      = Ico(position=[0,250,2], size=20, angle=[0,0,0], movMatrix=[0,-.6,0], rotMatrix=[1,2,3])
cube4       =Cube(position=[0,150,1], size=20, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[3,0,.1])
cube5       =Cube(position=[-25,150,0], size=8, angle=[0,0,30], movMatrix=[0,-.3,0], rotMatrix=[0,2,.1])
cube6       =Cube(position=[25,150,-1], size=9, angle=[30,0,0], movMatrix=[0,-.3,0], rotMatrix=[0,.3,4])

dodeca7       =Dodeca(position=[0,250,1], size=50, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[.4,-.5,.6])

cube8       =Cube(position=[0,250,1], size=50, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[3,1,.1])

cube9       =Cube(position=[0,250,1], size=20, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[1,-.2,1])
cube11       =Tetra(position=[0,250,1], size=5, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[-2,.5,0])
ico1       =Ico(position=[-60,250,5], size=25, angle=[0,30,0], movMatrix=[.1,-.3,0], rotMatrix=[-1,1,-.5])

tetra3      =Tetra(position=[-50,1000,0], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[2,3,1])
tetra4      =Tetra(position=[50,1100,10], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[-2,5,7])
tetra5     =Tetra(position=[0,1200,-20], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[2,-2,0])
tetra6      =Tetra(position=[20,1300,20], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[-2,5,-1])
tetra7      =Tetra(position=[-40,1400,40], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[2,-5,5])
tetra8      =Tetra(position=[70,1500,-30], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[-2,6,4])
tetra9      =Tetra(position=[-60,1600,5], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[2,2,3])
tetra10      =Tetra(position=[10,1700,50], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[-2,7,2])
tetra11      =Tetra(position=[40,1800,20], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[2,-5,0])
tetra12      =Tetra(position=[-50,1900,10], size=20, angle=[0,30,0], movMatrix=[0,-5,0], rotMatrix=[-2,5,1])

ico3      =Ico(position=[-50,2000,0], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[2,3,1])
ico4      =Dodeca(position=[50,2100,10], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[-2,5,7])
ico5     =Ico(position=[0,2200,-20], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[2,-2,0])
ico6      =Dodeca(position=[20,2300,20], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[-2,5,-1])
ico7      =Ico(position=[-40,2400,40], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[2,-5,5])
ico8      =Dodeca(position=[70,2500,-30], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[-2,6,4])
ico9      =Ico(position=[-60,2600,5], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[2,2,3])
ico10      =Dodeca(position=[10,2700,50], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[-2,7,2])
ico11      =Ico(position=[40,2800,20], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[2,-5,0])
ico12      =Dodeca(position=[-50,2900,10], size=15, angle=[0,30,0], movMatrix=[0,-4,0], rotMatrix=[-2,5,1])

tetra1      =Tetra(position=[0,150,2], size=15, angle=[15,15,15], movMatrix=[0,-.3,0], rotMatrix=[1,3,5])
dodeca1     =Dodeca(position=[0,200,14], size=25, angle=[15,15,15], movMatrix=[0,-.5,0], rotMatrix=[1,2,3])

tetra2       =Tetra(position=[0,200,1], size=10, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[2,1,-1])
cube10       =Cube(position=[0,200,1], size=20, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[2,1,-1])
ico2       =Ico(position=[0,200,1], size=15, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[2,1,-1])
dodeca2       =Dodeca(position=[0,200,1], size=20, angle=[0,30,0], movMatrix=[0,-.3,0], rotMatrix=[2,1,-1])
cube13       =Cube(position=[0,150,-35], size=150, angle=[38,0,-10], movMatrix=[0,0,0], rotMatrix=[0,0,.1])

cube14      = Cube(position=[0,3500,5], size=300, angle=[0,0,0], movMatrix=[0,-4,0], rotMatrix=[1,-1,1])


#animation begins

game = True

try:
    while game:
    
        #delay FPS
        #time.sleep(1/fps)

        #playfield.print_playfield(player, [cube13]) 
        #playfield.print_playfield(player, [dodeca7, cube8, cube9, cube11]) 
        playfield.print_playfield(player, [ico1]) 
        #playfield.print_playfield(player, [tetra3,tetra4,tetra5,tetra6,tetra7,tetra8,tetra9,tetra10,tetra11,tetra12,ico3,ico4,ico5,ico6,ico7,ico8,ico9,ico10,ico11,ico12]) 

except KeyboardInterrupt:
    pass




        