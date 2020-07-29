#imports
import msvcrt
import os
import time
import math

os.system("cls")

#a cuántos FPS  corre el juego
global fps
fps = 60

global x_resolution
global y_resolution
x_resolution = 80
y_resolution = 25

#ALL GAME ENTITIES
class Entity():

    def __init__(self):

        #x and y coordinates
        self.position = [0,0]
        self.gravity  = 0

    #calculates Y-axis distance DOWN to landscape
    #checks from current entity position to the bottom of the screen
    def y_distance(self,landscape):
        y_dist = -1

        for i in range(math.floor(self.position[1]), y_resolution):
            #checks all the way down in player's current X-position 
            if landscape.landscape_matrix[i][math.floor(self.position[0])] == " ":
                y_dist += 1
            else:
                #returns a list with distance to floor and Y-position of floor
                return [y_dist,i]

    #calculates Y-axis distance UP to landscape
    #checks from current entity position to the upper part of the screen
    def y_distance_neg(self,landscape):
        y_dist_neg = -1
        #print(str(y_resolution) + ", " + str(self.position[1]))
        for i in range(math.floor(self.position[1]), -1, -1):
            #checks all the way up in player's current X-position 
            if landscape.landscape_matrix[i][math.floor(self.position[0])] == " ":
                y_dist_neg += 1
            else:
                #returs a list with distance to ceiling and Y-position of ceiling
                return [y_dist_neg,i] #<--- tengo que encontrar la posición de la pieza ql

    #calculates X-axis distance to landscape to the RIGHT
    #checks from current entity position to the leftmost part of the screen
    def x_distance(self,landscape):
        x_dist = -1

        for i in range(math.floor(self.position[0]), x_resolution):
            #checks all the way to the right in entity's current Y-position 
            if landscape.landscape_matrix[math.floor(self.position[1])][i] == " ":
                x_dist += 1
            else:
                #returns a list with distance to the right and X-position of the next piece
                return [x_dist,i]

    #calculates X-axis distance to landscape to the LEFT
    #checks from current entity position to the upper part of the screen
    def x_distance_neg(self,landscape):
        x_dist_neg = -1
        #print(str(y_resolution) + ", " + str(self.position[1]))
        for i in range(math.floor(self.position[0]), -1, -1):
            #checks all the way to the left in entity's current Y-position 
            if landscape.landscape_matrix[math.floor(self.position[1])][i] == " ":
                x_dist_neg += 1
            else:
                #returns a list with distance to the left and X-position of the next piece
                return [x_dist_neg,i] 


#PLAYER CLASS
class Player(Entity):
    
    def __init__(self,player_number):
        Entity.__init__(self)
        self.player_number = player_number
        self.health        = 100
        self.alive         = True
        self.points        = 0
        self.lives         = 3
        self.character     = "☺"
    


    def pl_gravity(self,landscape):
        
        #detemines Y-position and distance to next piece of landscape
        y_dist = self.y_distance(landscape)[0]
        y_coor = self.y_distance(landscape)[1]

        #moves player down because of gravity
        if self.position[1] < y_coor - 1 and y_dist > 0:
            if self.position[1] + math.floor(self.gravity) >= y_coor:
                self.position[1] = y_coor - 1 
            else:
                self.position[1] += math.floor(self.gravity)
        else:
            self.gravity = 0

        #increases gravity
        try:
            if y_dist > 0:
                if self.gravity >= 1:
                    self.gravity += .1  
                else:
                    self.gravity += .3  
        except:
            self.gravity = 0

    

    

    #checks collision with landscape elements
    def collision_ls(self,landscape,old_pos):
        if landscape.landscape_matrix[self.position[1]][self.position[0]] != " ":
            self.position = old_pos

    #checks collision with landscape elements
    def collision_ls_jump(self,landscape):
        if self.y_distance_neg(landscape)[0] == -1: #and self.gravity <= 0  
            self.position[1] = self.y_distance_neg(landscape)[1] + 1


    #checks collision with enemies
    def collision_en(self,enemy,old_pos):
        #print(self.position+", "+enemy.position)
        if self.position == [math.floor(enemy.position[0]),math.floor(enemy.position[1])]:
            #player loses health!
            if enemy.enemy_type == 1:
                self.health  -= 20
                self.position = old_pos                 
        

    def player_movement(self,enemies,landscape):
        if msvcrt.kbhit():
            key = msvcrt.getch().decode("utf-8").lower()
            if key == "w":
                
                if self.y_distance(landscape)[0] == 0:
                    max_position_y    = self.y_distance_neg(landscape)[1]
                    self.gravity      = -1
                    self.position[1] -= 1

                    #checks for collisions with different entities and acts accordingly                                  

                    #enemies collision
                    for i in range(len(enemies)):
                        self.collision_en(enemies[i],max_position_y) 
                        
                
            elif key == "a":
                old_position      = [self.position[0],self.position[1]]
                self.position[0] -= 1

                #checks for collisions with different entities and acts accordingly 
                self.collision_ls(landscape,old_position)

                for i in range(len(enemies)):
                    self.collision_en(enemies[i],old_position)

                
            elif key == "d":
                old_position      = [self.position[0],self.position[1]]
                self.position[0] += 1

                #checks for collisions with different entities and acts accordingly 
                self.collision_ls(landscape,old_position)

                for i in range(len(enemies)):
                    self.collision_en(enemies[i],old_position)


            elif key == "s":
                old_position      = [self.position[0],self.position[1]]
                self.position[1] += 1

                #checks for collisions with different entities and acts accordingly 
                self.collision_ls(landscape,old_position)

                for i in range(len(enemies)):
                    self.collision_en(enemies[i],old_position)


            elif key == "q":
                return "q"                



#ENEMY CLASS
class Enemy(Entity):

    def __init__(self,enemy_type,enemy_speed,movement_type,position):

        Entity.__init__(self)
        self.enemy_type     = enemy_type
        #how many spaces per second
        self.enemy_speed    = enemy_speed
        #position for enemies is a float!
        self.position       = position
        self.movement_type  = movement_type


    def collision(self,landscape):

        if self.movement_type == 0:
            if self.x_distance(landscape)[0] <= 0 or self.x_distance_neg(landscape)[0] <= 0:            
                    self.enemy_speed *= -1

        if self.movement_type == 1:
            if self.y_distance(landscape)[0] <= 0 or self.y_distance_neg(landscape)[0] <= 0:            
                    self.enemy_speed *= -1



    def movement(self,landscape):
        
        """
        movement types: 
        0 = horizontal
        1 = vertical
        """

        if self.movement_type == 0:
            self.position[0] += self.enemy_speed / 10

        if self.movement_type == 1:
            self.position[1] += self.enemy_speed / 10

        self.collision(landscape)



#ITEMS CLASS
class Item(Entity):

    def __init__(self,enemy_type):
        Entity.__init__(self)
        self.item_type = item_type


#LANDSCAPE OBJECTS CLASS
class Landscape():

    def __init__(self):
        self.landscape_matrix = []

        for i in range(y_resolution):
            self.landscape_matrix.append([])
            for j in range(x_resolution):
                self.landscape_matrix[i].append(" ")

        

#PLAYFIELD CLASS
class Playfield():

    def __init__(self):
        pass

    """
    MOST IMPORTANT METHOD
    """
    def print_playfield(self,player,enemies,landscape):

        #we make a matrix representation of the playfield
        screen_matrix = []

        for i in range(y_resolution):
            screen_matrix.append([])
            for j in range(x_resolution):
                screen_matrix[i].append(" ")


        #we insert the level design into the matrix
        for i in range(y_resolution):
            for j in range(x_resolution):
                screen_matrix[i][j] = landscape.landscape_matrix[i][j]


        #we insert the enemies
        for i in range(len(enemies)):

            #enemies move
            enemies[i].movement(level1)
            

            #depends on the type of enemy:
            if enemies[i].enemy_type == 1:
                screen_matrix[math.floor(enemies[i].position[1])][math.floor(enemies[i].position[0])] = "*"


        """
        TEST
        """
        """
        #print(enemies[0].y_distance(landscape))
        print ("X-dist:")
        print(enemies[1].x_distance(landscape))
        #print(enemies[0].y_distance_neg(landscape))
        print ("X-dist-neg:")
        print(enemies[1].x_distance_neg(landscape))
        """

        #calculates effect of gravity in player
        player.pl_gravity(landscape)

        #landscape collision when jumping
        player.collision_ls_jump(landscape)

        #enemy collision
        for i in range(len(enemies)):
            player.collision_en(enemies[i],[player.position[0]-1,player.position[1]])

        #we insert the player character
        screen_matrix[player.position[1]][player.position[0]] = player.character

        #we convert the screen matrix into a string, so we can print it
        matrix_string = ""

        for i in range(y_resolution):
            for j in range(x_resolution):
                matrix_string += screen_matrix[i][j]
            if i < y_resolution - 1:
                matrix_string += "\n"

        os.system("cls")

        print(matrix_string)




        #HUD
        hud = ""

        #points
        hud += "Points: " + str(player.points) + " | Health: " + str(player.health) + " | Y-dist: " 
        hud += str(player.y_distance(level1)[0]) + " | (-)Y-dist: (" + str(player.y_distance_neg(level1)[0]) + "," + str(player.y_distance_neg(level1)[1]) + ")"
        hud += " | Pos: (" + str(player.position[0]) + ", " + str(player.position[1]) + ") | G: "
        hud += str(player.gravity)
        #hud += " | X-dist: (" + str(player.x_distance(level1)[0]) + "," + str(player.x_distance(level1)[1]) + ") | "
        #hud += "(-)X-dist: (" + str(player.x_distance_neg(level1)[0]) + "," + str(player.x_distance_neg(level1)[1]) + ")"

        print(hud)


#we initialize classes
player     = Player(0)
playfield  = Playfield()
level1     = Landscape()
enemies_l1 = []

"""
LEVELSSSSSSS
"""

"""
level 1 design:
"""

player.position = [1,1]

#level 1 landscape
level1.landscape_matrix[0][0]   = "╔" 
level1.landscape_matrix[24][79] = "╝" #should be resolution-1
level1.landscape_matrix[0][79]  = "╗"
level1.landscape_matrix[24][0]  = "╚"

level1.landscape_matrix[5][4]  = "╗"
level1.landscape_matrix[5][3]  = "═"
level1.landscape_matrix[5][2]  = "═"
level1.landscape_matrix[5][1]  = "═"

level1.landscape_matrix[21][8]  = "═"
level1.landscape_matrix[21][7]  = "═"
level1.landscape_matrix[21][6]  = "═"

level1.landscape_matrix[19][9]  = "═"
level1.landscape_matrix[19][10]  = "═"
level1.landscape_matrix[19][11]  = "═"

level1.landscape_matrix[17][5]  = "═"
level1.landscape_matrix[17][6]  = "═"
level1.landscape_matrix[17][7]  = "═"

level1.landscape_matrix[15][10]  = "═"
level1.landscape_matrix[15][11]  = "═"
level1.landscape_matrix[15][12]  = "═"

level1.landscape_matrix[13][16]  = "═"
level1.landscape_matrix[13][17]  = "═"
level1.landscape_matrix[13][18]  = "═"

level1.landscape_matrix[14][22]  = "═"
level1.landscape_matrix[14][23]  = "═"
level1.landscape_matrix[14][24]  = "═"

level1.landscape_matrix[11][29]  = "═"
level1.landscape_matrix[11][30]  = "═"
level1.landscape_matrix[11][31]  = "═"

level1.landscape_matrix[9][31]  = "═"
level1.landscape_matrix[9][32]  = "═"
level1.landscape_matrix[9][33]  = "═"

level1.landscape_matrix[8][36]  = "═"
level1.landscape_matrix[8][37]  = "═"
level1.landscape_matrix[8][38]  = "═"

level1.landscape_matrix[5][39]  = "═"
level1.landscape_matrix[5][40]  = "═"
level1.landscape_matrix[5][41]  = "═"

level1.landscape_matrix[4][31]  = "═"
level1.landscape_matrix[4][32]  = "═"
level1.landscape_matrix[4][33]  = "═"

for i in range (1,24):
    level1.landscape_matrix[i][0]  = "║"
    level1.landscape_matrix[i][79] = "║"

level1.landscape_matrix[5][0]  = "╠"

for i in range (6,23):
    level1.landscape_matrix[i][4]  = "║"

for i in range (1,79):
    level1.landscape_matrix[0][i]  = "═"
    level1.landscape_matrix[24][i] = "═"

#level 1 enemies
enemy1_l1 = Enemy(1,2,1,[10,5])
enemy2_l1 = Enemy(1,4,0,[15,3])
enemy3_l1 = Enemy(1,1,1,[2,2])
enemy4_l1 = Enemy(1,1,1,[32,7])
enemy5_l1 = Enemy(1,4,0,[6,11])
enemy6_l1 = Enemy(1,8,0,[2,23])
enemies_l1.append(enemy1_l1)
enemies_l1.append(enemy2_l1)
enemies_l1.append(enemy3_l1)
enemies_l1.append(enemy4_l1)
enemies_l1.append(enemy5_l1)
enemies_l1.append(enemy6_l1)

"""    
end of level 1
"""

game = True

#playfield.print_playfield(player,level1)

while game:
    

    if player.player_movement(enemies_l1,level1) == "q":
        game = False

    #delay FPS
    time.sleep(1/fps)
            
    playfield.print_playfield(player,enemies_l1,level1)    

    

    

