import pygame
from constants import  MOVEMENT_BORDER, PLAYER_SPEED, TILE_SIZE,DISPLAY_WIDTH, PLAYER_HEALTH, TILE_SIZE,DISPLAY_HEIGHT,PLAYER_SIZE
from tiles import *
from background import Scenery
from generate import Generate
from GUI import *
from leaderboard import Leaderboard
class Level:
    """ Class that creates level and controls the running of the game"""
    def __init__ (self,surface,type):
        #display surface
        self.display_surface = surface
        #type of level
        self.type = type
        self.day = True
        if type ==3:
            self.day = False
        #creates tiles
        self.world_shift = 0
        self.current_x = 0
        #loads background
        self.setup_level()
        self.backgrounds = Scenery(self.display_surface,self.day)     #NEW where 1 = theme
        #name entry
        self.name_group = pygame.sprite.Group()
        self.name_entered = False
        self.name_array = ["-","-","-"]
        self.name = ""
        self.name_entry_make()
        #HUD
        self.HUD_group = pygame.sprite.Group() 
        self.HUD_asset_heart = r'.\graphics\HUD\heartalive.png'
        self.HUD_asset_heart_dead = r'.\graphics\HUD\heartdead.png'
        self.HUD_make()
        #projectiles
        self.projectile_group_player = pygame.sprite.Group()
        self.projectile_group_enemy = pygame.sprite.Group()
        #leaderboard
        self.leaderboard = Leaderboard()
        

    def name_entry_make(self):
        #creates inital sprites that will be displayed on name entry
        self.enter_name = Text('ENTER NAME',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.2),self.display_surface,'red',100,self.name_group)
        self.letter1 = Text('-',(DISPLAY_WIDTH*0.25,DISPLAY_HEIGHT*0.4),self.display_surface,'white',100,self.name_group)
        self.letter2 = Text('-',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.4),self.display_surface,'white',100,self.name_group)
        self.letter3 = Text('-',(DISPLAY_WIDTH*0.75,DISPLAY_HEIGHT*0.4),self.display_surface,'white',100,self.name_group)
        self.enter_button = Button("Continue",self.display_surface,'black',self.name_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.7,DISPLAY_WIDTH*0.25,DISPLAY_HEIGHT*0.1),'red','white',self.name_group,action = self.name_entry_finish)
        

    def name_entry_update(self,character_input):
        #updates the name entry fields according to characters input passed as paramenter
        def add(letter):
            #add a letter to the name
            for i in range(len(self.name_array)):
                if self.name_array[i] == "-":
                    self.name_array[i] = letter
                    return
        def remove():
            #removes a letter from the name
            for i in range(len(self.name_array)-1,-1,-1):
                if self.name_array[i] != "-":
                    self.name_array[i] = "-"
                    return

        #determines action based on character input   
        if character_input == "DEL":
            remove()
        elif character_input == "ENTER":
            self.name_entry_finish()
        elif character_input == None:
            pass
        else:
            add(character_input)
        #updates letter sprites
        self.letter1.update(self.name_array[0])
        self.letter2.update(self.name_array[1])
        self.letter3.update(self.name_array[2])
        self.enter_button.update()
        
        
    def name_entry_finish(self):
        #checks if valid name entered, allows game start if so
        for item in self.name_array:
            if item == "-":
                return
        for item in self.name_array:
            self.name = self.name + (item)
        self.name_entered = True
        self.time = 0
        self.clock = pygame.time.Clock()
        self.time = 0
        print(self.time)
    


    def HUD_make(self):
        #makes all the assets for the HUD
        self.HUD_hearts = [None,None,None,None,None]    
        self.HUD_distance = Text('Distance:'+str(0),(DISPLAY_WIDTH*0.075,DISPLAY_HEIGHT*0.05),self.display_surface,'black',50,self.HUD_group)
        self.HUD_time = Text('Time:'+str(0),(DISPLAY_WIDTH*0.075,DISPLAY_HEIGHT*0.95),self.display_surface,'black',50,self.HUD_group)

        for i in range (0,5):
            self.HUD_hearts[i] = Image(self.HUD_asset_heart,(DISPLAY_WIDTH*0.3+(i*0.15*DISPLAY_HEIGHT),DISPLAY_HEIGHT*0.95,DISPLAY_WIDTH*0.1,DISPLAY_HEIGHT*0.1),self.display_surface,self.HUD_group)
            

    def HUD_update(self):
        #displays all the assets for the hearts
        self.HUD_distance.update("Distance:"+str(int(self.player.sprite.distance/TILE_SIZE)))   #gives updated distance
        self.HUD_time.update('Time:'+str(int(self.time/1000)))                                  #gives updated time
        for i in range(PLAYER_HEALTH):                                                          #fills in hearts according to health  
            if self.player.sprite.health > i:
                self.HUD_hearts[i].update(self.HUD_asset_heart)
            else:
                self.HUD_hearts[i].update(self.HUD_asset_heart_dead)


    def setup_level(self):
        #called at start to generate level
        self.level_generator = Generate()                                               #instance of generate class
        self.tiles,self.player,self.enemies = self.level_generator.generate_start(self.day)     #generatess flat level
        self.time = 0                                                                   #starts clock at 0

    def scroll_x(self):
        #controls the horizontal movement of the player and backgrounds 
        #shortens commonly used variables
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        #detects when player at movement border then set x-shift
        if player_x < 0 and direction_x < 0:                                            #makes player stationary and world move
            player.speed = 0
        elif player_x > (1-MOVEMENT_BORDER)*DISPLAY_WIDTH and direction_x > 0:          
            self.world_shift = -PLAYER_SPEED
            player.speed = 0                                                            #makes player stationary and world move
        else:
            self.world_shift = 0
            player.speed = PLAYER_SPEED                                                 #makes world stationary and player move


    def calc_stats(self):
        #calculates overall KD and VEL
        #shortens var
        player = self.player.sprite
        try:
            KD = player.kills/player.deaths
        except ZeroDivisionError:                                   #cant divide by 0
            if player.kills > 0:
                KD = player.kills
            else:
                KD = 0
        try:
            VEL = (player.distance/TILE_SIZE)/(self.time/1000)
        except ZeroDivisionError:                                   #cant divide by 0
            VEL = 0
        
        return float(int(KD)),float(int(VEL))                       #concatenates values to a single digit
    
    def get_score(self):
         #calculates score
         return int(self.player.sprite.kills)*2 + int(self.player.sprite.distance/TILE_SIZE/20)

    def get_distance(self):
        #gets the distance from the start of the level, constantly called to keep updated
        player = self.player.sprite
        if player.on_right == False and player.on_left == False and player.rect.x >0:    
            player.distance+=(player.direction.x*PLAYER_SPEED)      #calculates distance

    def delete_offscreen(self):
        # This deletes tiles that disappear off the left of the screen
        # Is also tied in with all generation as the generation is timed of when a tile is deleted
        player = self.player.sprite
        for tile in self.tiles:
            if tile.rect.x <= 0-TILE_SIZE:
                self.calc_stats()                                       #calculates statisitics about the player
                self.level_generator.kills = player.kills               #passes value into generate instance
                self.level_generator.deaths = player.deaths             #passes value into generate instance
                self.level_generator.time = self.time/1000              #passes value into generate instance
                self.level_generator.passthrough = self.calc_stats()    #gets values passed through into learn
                self.level_generator.tile_create = True                 #sets flag that tile should be made
                
                tile.kill()                                             #deletes old tile
        for enemy in self.enemies:
            if enemy.rect.x <= 0- TILE_SIZE:
                enemy.kill()                                            #deletes enemy
        
        for projectile in self.projectile_group_player:                 #iterates though player projectiles
            if (
            projectile.rect.y < - 0.1*DISPLAY_HEIGHT or                 #everywhere outside visible display
            projectile.rect.y > DISPLAY_HEIGHT or 
            projectile.rect.x > DISPLAY_WIDTH or 
            projectile.rect.x < 0-DISPLAY_WIDTH*0.1):
                projectile.kill()                                       #kills
        
        for projectile in self.projectile_group_enemy:                  #iterates through enemy projectiles
            if (
            projectile.rect.y < - 0.1*DISPLAY_HEIGHT or                 #everywhere outside visible display
            projectile.rect.y > DISPLAY_HEIGHT or 
            projectile.rect.x > DISPLAY_WIDTH or 
            projectile.rect.x < 0-DISPLAY_WIDTH*0.1):
                projectile.kill()                                       #kills



    def display(self,character_input = None):
        #displays all tiles and updates
        #####name entry loop######
        #game doesn't start yet
        if self.name_entered == False:
            image = pygame.image.load(r'.\GUI\page_level.png').convert_alpha()
            self.display_surface.blit(image,(0,0))
            self.name_entry_update(character_input)
            self.name_group.draw(self.display_surface)
            return                                                                  #ensures game isn't played until name entered
        
        #####main game#####
        #level generation
        self.delete_offscreen()
        self.level_generator.generate()

        #background
        self.backgrounds.update(self.world_shift) 

        #level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #player
        self.player.update(self.projectile_group_player)
        for p in self.player:
            if p.health <= 0:                                               #if player dies, returns to main file
                self.leaderboard.set_entry(self.name,self.get_score(),int(p.distance/TILE_SIZE),p.kills,int(self.time/1000))
                return False
            p.horizontal_movement_collision(p,self.tiles,self.world_shift)  #collisions
            p.vertical_movement_collision(p,self.tiles)
            p.projectile_collision(p,self.projectile_group_enemy)
        self.player.draw(self.display_surface)                              #displays
        self.get_distance()

        #enemies
        self.enemies.update(self.world_shift,self.player.sprite,self.projectile_group_enemy)
        for e in self.enemies:
            e.horizontal_movement_collision(e,self.tiles,self.world_shift)
            e.vertical_movement_collision(e,self.tiles)
            e.projectile_collision(e,self.projectile_group_player)
            if e.facing_right == False and   e.status == "attack" and e.type == 'melee':    #if a melee enemy is attacking, their image is displayed to make
                self.display_surface.blit(e.image,(e.rect.x-PLAYER_SIZE[0],e.rect.y))       # it at the correct position
            else:
                self.display_surface.blit(e.image,e.rect)                                   #otherwise normal displaying
            
        #Clock
        self.clock.tick(60)
        self.time += self.clock.get_time()
        
        #projectiles
        self.projectile_group_player.update(self.tiles,self.world_shift)
        self.projectile_group_enemy.update(self.tiles,self.world_shift) 
        self.projectile_group_player.draw(self.display_surface)
        self.projectile_group_enemy.draw(self.display_surface)

        #determines level type, level 2 is flipped
        if self.type == 2:
            surf = self.display_surface
            surf = pygame.transform.flip(surf,False,True)
            self.display_surface.blit(surf,(0,0))

        #HUD
        self.HUD_update()
        self.HUD_group.draw(self.display_surface)





        

        

        

        



        

    