import random
import pygame
import math
from noise import pnoise1
from tiles import *
from player import Player
from enemy import Enemy_melee, Enemy_projectile
from constants import TILE_SIZE,BASELINE,BASEMAX,L1_WIDTH,L2_WIDTH,L3_WIDTH,L1_SEPARATION,L2_SEPARATION,L3_SEPARATION,DISPLAY_HEIGHT,DISPLAY_WIDTH
from learning import Learn

class Generate:
    """class to control the generation of the world in realtime"""
    def __init__(self):
        #runtime generation
        self.tile_create = False
        self.tile_count = int(DISPLAY_WIDTH/TILE_SIZE)+1
        self.tile_batch_num = 0
        #groups
        #each group will be used for calcualations
        #column groups will be made dynamically
        self.tile_group = pygame.sprite.Group()
        self.base_group = pygame.sprite.Group()
        self.L1_group = pygame.sprite.Group()
        self.L2_group = pygame.sprite.Group()
        self.L3_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        #columns
        self.column_num = int(DISPLAY_WIDTH/(L1_WIDTH*TILE_SIZE))

        #perlin settings
        self.octaves = random.randint(1,4)
        self.persistence = random.randint(1,10)
        self.lacunarity = 1
        self.repeat = random.randint(64,256)
  
        #learning
        self.learn_handler = Learn(0,0,0,0)                             #calls learning class
        self.passthrough = None                                         #passthrough is used to pass variable from level to learning
            #vel
        self.time = 0                                                   #overall time for game
        self.time_for_batch = 0                                         #time taken for entire batch
            #kd
        self.kills = 0                                                  #Player.kills
        self.deaths = 0                                                 #Player.deaths
        self.old_kill_total = 0                                         #Player.kills from last batch
        self.old_death_total = 0                                        #Player.deaths from last batch

        #difficultys
        self.platform_dif = 0
        self.perlin_dif = 0
        self.melee_dif = 0
        self.projectile_dif = 0


    def generate_start(self,day = True):
        #the intial generation of the level - completely flat
        self.day = day
        if self.day == False:
             self.lacunarity == 2
             
        for i in range (-1,int(DISPLAY_WIDTH/TILE_SIZE)+1):                     #determines number of tiles, iterates through
            x = i*TILE_SIZE                                                     #x value
            y = DISPLAY_HEIGHT-BASELINE*TILE_SIZE                               #y value
            if i == 2:                                                          #player spawn value
                player_sprite = Player((x,y),self.day)                                   #creates player
                self.player_group.add(player_sprite)
            tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                              #creates top tile
            self.tile_group.add(tile)
            self.base_group.add(tile)
            for i in range(BASELINE-1,0,-1):                                    #fills in below top tile for each x
                y = DISPLAY_HEIGHT-i*TILE_SIZE                                  #determines new y, no change in x
                tile = Tile_No_Side((x,y),TILE_SIZE,self.day)
                self.tile_group.add(tile)
                self.base_group.add(tile)        
        return self.tile_group,self.player_group,self.enemy_group               #returns groups as needed in level


    def generate(self):
        #generates level in realtime, called tick
        if self.tile_create == True:                                            #increments every time a tile is deleted
            self.tile_count +=1
            self.tile_create = False                                            #resets value
            
        if self.tile_count >= int(DISPLAY_WIDTH/TILE_SIZE)+1:                   #generates new batch when a screens worth of tiles has been deleted
            self.tile_count = 0                                                 #resets counter
            #batch calculations
            time_taken = self.time - self.time_for_batch
            kills_for_batch = self.kills - self.old_kill_total
            deaths_for_batch = self.deaths - self.old_death_total
            #call learning
            self.melee_dif, self.projectile_dif,self.perlin_dif,self.platform_dif = self.learn_handler.learn(self.passthrough,time_taken,kills_for_batch,deaths_for_batch) #feedback from learning
            #more batch calculations
            self.old_kill_total = self.kills
            self.old_death_total = self.deaths
            self.time_for_batch = self.time
           #changing perlin settings
            self.lacunarity = 1 + (4 * self.perlin_dif)                         
            
            #1 batch (screen)
            y_max = self.generate_base()                                        #generates a new batch
            self.generate_L1(y_max)
            self.generate_L2(y_max)
            self.generate_L3(y_max)
            self.tile_batch_num +=1                                             #increments batch num

    
    def generate_base(self):
        #generates base with perlin noise, to change according to difficulty later, change perlin settings, lancuarity will change difficulty
        def tile_type(x,y,num,y_middle):
            #uses correct tile should still work even with changing lacunarity
            y_behind = int(pnoise1(math.sqrt((num-1)/4),  self.octaves, self.persistence, self.lacunarity, self.repeat)*10)     #y value of tile behind
            y_infront = int(pnoise1(math.sqrt((num+1)/4),  self.octaves, self.persistence, self.lacunarity, self.repeat)*10)    #y value of tile infront
            if y_behind < 0: y_behind = y_behind* -1                                                                            #modulus of value
            if y_infront < 0: y_infront = y_infront * -1                                                                        #modulus of value
            if y_behind > BASEMAX : y_behind = BASEMAX                                                                          #sets limits
            if y_infront > BASEMAX : y_infront = BASEMAX                                                                        #sets limits

            #conditions
            if y_behind == y_middle and y_infront == y_middle:                                                                  #uses if else statement to determine   
                tile = Tile_Grass_Top((x,y),TILE_SIZE+2,self.day)                                                                        #correct tile to use
            elif y_behind == y_middle and y_infront < y_middle:
                tile = Tile_Top_Right((x,y),TILE_SIZE+2,self.day)
            elif y_behind == y_middle and y_infront > y_middle:
                tile = Tile_Grass_Top((x,y),TILE_SIZE+2,self.day)
            elif y_behind < y_middle and y_infront == y_middle:
                tile = Tile_Top_Left((x,y),TILE_SIZE+2,self.day)
            elif y_behind > y_middle and y_infront == y_middle:
                tile = Tile_Grass_Top((x,y),TILE_SIZE+2,self.day)
            elif y_behind < y_middle and y_infront < y_middle:
                tile = Tile_Top_Right_Left((x,y),TILE_SIZE+2,self.day) 
            else:
                tile = Tile_Grass_Top((x,y),TILE_SIZE+2,self.day)                                                                        #default                
            self.tile_group.add(tile)                                                                                           #add to groups
            self.base_group.add(tile)


        y_max = {}                                                                                                          #y_max is a dictionary of highest points in each batch
        for i in range (0,int(DISPLAY_WIDTH/TILE_SIZE)+1):                                                                  #creates amount that has been deleted
            #x coord
            x = DISPLAY_WIDTH + TILE_SIZE*i                                                                                 #x coord 
            
            #y coord
            num = self.tile_batch_num*int(DISPLAY_WIDTH/TILE_SIZE)+1+i                                                      # for tidiness number entered into perlin calculated here
            perlin_val = int(pnoise1(math.sqrt(num/4),  self.octaves, self.persistence, self.lacunarity, self.repeat)*10)   #value from perlin taken
            if perlin_val < 0:
                perlin_val= -1*perlin_val                                                                                   #modulus function of perlin value
            if perlin_val > BASEMAX:                                                                                        #sets limits
                perlin_val = BASEMAX
            y = DISPLAY_HEIGHT - perlin_val*TILE_SIZE - BASELINE*TILE_SIZE                                                  #calculates y coordinate from perlin

            #tile
            tile_type(x,y,num,perlin_val)                                                                                   #calls function to create correct tile

            #enemy spawning
            if random.uniform(0,10) < self.melee_dif:                                                                         #chance of enemy spawn *RL OPPORTUNITY*
                enemy = Enemy_melee((x,y+TILE_SIZE),self.day)
                self.enemy_group.add(enemy)
            #tile spawning
            if random.uniform(0,5) < self.platform_dif:                                                                     #chance of tile spawn *RL OPPORTUNITY 
                tile = Tile_Spikes((x,y),TILE_SIZE,self.day)
                self.tile_group.add(tile)
                
            #determines values for y_max dictionary
            for i in range(0,self.column_num):                                                                              #iterates through each column
                max_height = DISPLAY_HEIGHT                                                                                 #initial max height
                lower_bound = DISPLAY_WIDTH + i * L1_WIDTH*TILE_SIZE                                                        #x lower bound 
                upper_bound = DISPLAY_WIDTH + (i+1) * L1_WIDTH*TILE_SIZE                                                    #x upper bound
                if x > lower_bound and x < upper_bound:                                                                     #checks x is in column
                    if y < max_height:
                        try:                                                                                                #updates y_max if y is less
                            if y < y_max[i]:
                                y_max[i] = y
                        except KeyError:
                            y_max[i] = y                                                                                    #creates new entry if none
                            
                
               

            #creating filler tiles below
            for o in range(perlin_val-1,-BASELINE,-1):
                y = DISPLAY_HEIGHT - o*TILE_SIZE - BASELINE*TILE_SIZE
                tile = Tile_No_Side((x,y),TILE_SIZE+2,self.day)
                self.tile_group.add(tile)
                self.base_group.add(tile)
            
        return y_max
            
            

 
    def generate_L1(self,y_max):
        #generates 1 batch of L1
        for i in range(0,self.column_num):                                                              #each column
            if random.uniform(-1,1) < self.platform_dif:                                                #chance of no column spawn
                for j in range(0,L1_WIDTH):                                                             #each tile
                    if j != random.randint(1,L1_WIDTH) and j != int(L2_WIDTH/2):                        #chance of no tile spawn, no tile spawn in centre of each
                        x = DISPLAY_WIDTH + i*L1_WIDTH*TILE_SIZE + j*TILE_SIZE                          #correct x 
                        y = y_max[i]- L1_SEPARATION*TILE_SIZE - TILE_SIZE                               #correct y
                        #extra tile
                        if random.uniform(0.5,10) < self.platform_dif:                                   #chance of extra tile above *RL OPPORTUNITY*
                            tile = Tile_No_Side((x,y),TILE_SIZE,self.day)                               #creates and adds tile
                            tile_extra = Tile_Top_Right_Left((x,y-TILE_SIZE),TILE_SIZE,self.day)        #creates and extra tile
                            self.tile_group.add(tile_extra)
                            self.L1_group.add(tile_extra)
                            self.tile_group.add(tile)
                            self.L1_group.add(tile)                        
                            #enemy spawning
                        elif random.uniform(0,5) < self.melee_dif:                                      #chance of enemy spawn *RL OPPORTUNITY*
                                enemy = Enemy_melee((x,y+TILE_SIZE),self.day)
                                self.enemy_group.add(enemy)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                         #normal tile creation
                                self.tile_group.add(tile)
                                self.L1_group.add(tile)  
                                #projectile enemy spawning
                        elif random.uniform(0,10) < self.projectile_dif:                                #chance of enemy spawn *RL OPPORTUNITY*
                                enemy = Enemy_projectile((x,y+TILE_SIZE),self.day)
                                self.enemy_group.add(enemy)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                         #normal tile creation
                                self.tile_group.add(tile)
                                self.L1_group.add(tile)  
                            #tile spawning
                        elif random.uniform(0.3,2) < self.platform_dif:                                 #chance of tile spawn *RL OPPORTUNITY*
                                #spike
                                tile = Tile_Spikes((x,y),TILE_SIZE,self.day)
                                self.tile_group.add(tile)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                         #normal tile creation
                                self.tile_group.add(tile)
                                self.L1_group.add(tile)                                
                        else:
                            #normal tile
                            tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                             #normal tile creation
                            self.tile_group.add(tile)
                            self.L1_group.add(tile)



    
    def generate_L2(self,y_max):
        #generates 1 batch of L2
        for i in range(0,self.column_num):                                                              #each column
            if random.uniform(-0.5,1) < self.platform_dif:                                              #chance of no column spawn
                for j in range(0,L2_WIDTH):                                                             #each tile
                    if j != random.randint(1,L2_WIDTH) and j != int(L2_WIDTH/2):                        #chance of no tile spawn, no tile spawn in centre of each
                        x = DISPLAY_WIDTH + i*L1_WIDTH*TILE_SIZE + j*TILE_SIZE                          #correct x
                        y = y_max[i]- (L1_SEPARATION+L2_SEPARATION+1)*TILE_SIZE - TILE_SIZE             #correct y
                        #extra tile
                        if random.uniform(0.6,10) < self.platform_dif:                                   #chance of extra tile above *RL OPPORTUNITY*
                            tile = Tile_No_Side((x,y),TILE_SIZE,self.day)                               #creates and adds tile
                            tile_extra = Tile_Top_Right_Left((x,y-TILE_SIZE),TILE_SIZE,self.day)        #creates and extra tile
                            self.tile_group.add(tile_extra)
                            self.L2_group.add(tile_extra)
                            self.tile_group.add(tile)
                            self.L2_group.add(tile)                        
                            #enemy spawning
                        elif random.uniform(0,10) < self.melee_dif:                                     #chance of enemy spawn *RL OPPORTUNITY*
                                enemy = Enemy_melee((x,y+TILE_SIZE),self.day)
                                self.enemy_group.add(enemy)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                         #normal tile creation
                                self.tile_group.add(tile)
                                self.L2_group.add(tile)  
                            #projectile enemy spawning
                        elif random.uniform(0,7) < self.projectile_dif:                                 #chance of enemy spawn *RL OPPORTUNITY*
                                enemy = Enemy_projectile((x,y+TILE_SIZE),self.day)
                                self.enemy_group.add(enemy)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                         #normal tile creation
                                self.tile_group.add(tile)
                                self.L2_group.add(tile)  
                            #tile spawning
                        elif random.uniform(0.4,3) < self.platform_dif:                                 #chance of tile spawn *RL OPPORTUNITY*
                                #spike
                                tile = Tile_Spikes((x,y),TILE_SIZE,self.day)
                                self.tile_group.add(tile)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                         #normal tile creation
                                self.tile_group.add(tile)
                                self.L2_group.add(tile)                                
                        else:
                            #normal tile
                            tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                             #normal tile creation
                            self.tile_group.add(tile)
                            self.L2_group.add(tile)
    
    def generate_L3(self,y_max):
        #generates 1 batch of L3
        for i in range(0,self.column_num):                                                                  #each column
            if random.uniform(-0.25,1) < self.platform_dif:                                                 #chance of column spawn
                for j in range(0,L3_WIDTH) :                                                                #each tile
                    if j != random.randint(1,L1_WIDTH) and j != int(L3_WIDTH/2):                            #chance of no tile spawn, no tile spawn in centre of each
                        x = DISPLAY_WIDTH + i*L1_WIDTH*TILE_SIZE + j*TILE_SIZE                              #correct x
                        y = y_max[i] - (L1_SEPARATION+L2_SEPARATION+L3_SEPARATION+2)*TILE_SIZE - TILE_SIZE  #correct y
                        #extra tile
                        if random.uniform(0.7,10) < self.platform_dif:                                       #chance of extra tile above *RL OPPORTUNITY*
                            tile = Tile_No_Side((x,y),TILE_SIZE,self.day)                                   #creates and adds tile
                            tile_extra = Tile_Top_Right_Left((x,y-TILE_SIZE),TILE_SIZE,self.day)            #creates and extra tile
                            self.tile_group.add(tile_extra)
                            self.L3_group.add(tile_extra)
                            self.tile_group.add(tile)
                            self.L3_group.add(tile)                        
                            #enemy spawning
                        elif random.uniform(0,15) < self.melee_dif:                                         #chance of enemy spawn *RL OPPORTUNITY*
                                enemy = Enemy_melee((x,y+TILE_SIZE),self.day)
                                self.enemy_group.add(enemy)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                             #normal tile creation
                                self.tile_group.add(tile)
                                self.L3_group.add(tile)  
                            #projectile enemy spawning
                        elif random.uniform(0,5) < self.projectile_dif:                                     #chance of enemy spawn *RL OPPORTUNITY*
                                enemy = Enemy_projectile((x,y+TILE_SIZE),self.day)
                                self.enemy_group.add(enemy)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                             #normal tile creation
                                self.tile_group.add(tile)
                                self.L3_group.add(tile)                                 
                            #tile spawning
                        elif random.uniform(0.6,4) < self.platform_dif:                                     #chance of tile spawn *RL OPPORTUNITY*
                                #spike
                                tile = Tile_Spikes((x,y),TILE_SIZE,self.day)
                                self.tile_group.add(tile)
                                #normal tile
                                tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                             #normal tile creation
                                self.tile_group.add(tile)
                                self.L3_group.add(tile)                                
                        else:
                            #normal tile
                            tile = Tile_Grass_Top((x,y),TILE_SIZE,self.day)                                 #normal tile creation
                            self.tile_group.add(tile)
                            self.L3_group.add(tile)
