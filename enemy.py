import pygame
from constants import ANIMATION_SPEED, PLAYER_SPEED,PLAYER_SIZE,DISPLAY_WIDTH,PROJECTILE_SPEED,PROJECTILE_SIZE,MELEE_ANIMATION_SPEED,PROJECTILE_ENEMY_ANIMATION_SPEED
from sprite import Sprite_base, Projectile

class Enemy(Sprite_base):
    """basis of both types of enemy sprite"""
    def __init__(self,pos,day):
        super().__init__(pos,day)
        self.path = ''
        
    def import_character_assets(self):
        #loads all assetes from multiple folders
        super().import_character_assets()

    def update(self,x_shift,player,projectile_group):
        #updates all
        self.rect.x += x_shift                                  #offset
        if self.direction.x == 1:
            self.facing_right = True                            #updates direction
        else:
            self.facing_right = False
        self.decision_tree(player,projectile_group)             #calls decision tree
        if self.health <= 0 and self.status != 'dead':          #sets as dead when no health left
            player.kills += 1
            self.status = "dead"
            self.frame_index = 0
        super().update()
        


class Enemy_melee(Enemy):
    """melee enemy"""
    def __init__(self,pos,day):
        super().__init__(pos,day)
        self.type = "melee"                                     #sets type

    def import_character_assets(self,day):
        #loads all assetes from multiple folders
        if day:
            self.path = './graphics/day/enemies/dark knight/'
        else:
            self.path = './graphics/night/enemies/dark knight/'

        super().import_character_assets()
        self.get_scale_multiplier()

    def animate(self):
        #animates melee enemy, different to base sprite
        if self.status == "dead" and self.death_complete == True:   #exits if dead and no longer meant to be animated
            return 
        #
        animation = self.animations[self.status]                    #gets correct animation for status
        self.frame_index += self.animation_speed                    #increments frame index
        #
        if self.frame_index >= len(animation):                      #end of the animation
            self.frame_index = 0
            if self.status == 'attack':                             #resets attack status after full animation played
                self.status = 'run'                                 #resets to run as similar animation
                self.attack_done = False
                self.decision_tree(self.player,"")                  
                if self.status == "attack":                         #ensures player is still within range 
                    self.player.health -= 1                         #does damage
            if self.status == "dead":                               #checks that death animation played fully
                self.death_complete = True
                return


        image = animation[int(self.frame_index)]                    #gets image from animation
        width = (image.get_rect()).w                                #gets width of image
        image = pygame.transform.scale(image,(width/self.scale_multiplier,PLAYER_SIZE[1]) ) #gets a standard size image
        fake_image =  pygame.transform.scale(image,PLAYER_SIZE )                            #creates normal rect  to use with collisions
        

        if self.facing_right:
            self.image = image                                                              #sets image attribute to image made      
        else:
            self.image = pygame.transform.flip(image,True,False)                            #flips image if facing left

        #setting the rect so that sprite always on the floor    
        #onground colliding with right
        if self.on_ground and self.on_right:
            self.rect = fake_image.get_rect(bottomright = self.rect.bottomright)            #makes sure rect is always matching (fake)image
        #onground colliding with left
        elif self.on_ground and self.on_left:
            self.rect = fake_image.get_rect(bottomleft = self.rect.bottomleft)
        #onground
        elif self.on_ground:
            self.rect = fake_image.get_rect(midbottom = self.rect.midbottom)

        #onceiling colliding with right
        elif self.on_ceiling and self.on_right:
            self.rect = fake_image.get_rect(topright = self.rect.topright)
        #onceiling colliding with left
        elif self.on_ceiling and self.on_left:
            self.rect = fake_image.get_rect(topleft = self.rect.topleft)
        #onceiling
        elif self.on_ceiling:
            self.rect = fake_image.get_rect(midtop = self.rect.midtop)



    def get_scale_multiplier(self):
        #finds the amount to multiply the length of a melee enemies attack image by
        rect = self.animations["idle"][0].get_rect()
        self.scale_multiplier = rect.h/PLAYER_SIZE[1]

    def decision_tree(self,player,_):
        #determines what the enemy should do
        if self.status == "dead":                                                           #nothing if dead
            return
        self.player = player                                                                #takes player sprite for reference
        if player.rect.x > self.rect.x:                                                     #player on left of enemy
            if player.rect.x - self.rect.x <= DISPLAY_WIDTH*0.25:                           #if within 1/4 of the screen 
                self.direction.x = 1
                self.speed = PLAYER_SPEED*0.75                                              #move towards
            else:
                self.speed = 0                                                              #otherwise idle
            if player.rect.x - self.rect.x <= PLAYER_SIZE[1] and self.rect.y == player.rect.y:  #if within 1 player width
                self.attack()                                                                   #attack

        elif player.rect.x < self.rect.x:                                                   #if on right
            if self.rect.x - player.rect.x <= DISPLAY_WIDTH*0.25:                           #if within 1/4 of the screen
                self.direction.x = -1
                self.speed = PLAYER_SPEED*0.75                                              #move towards
            else:
                self.speed = 0                                                              #otherwise idle
            if self.rect.x - player.rect.x <= PLAYER_SIZE[1] and self.rect.y == player.rect.y:  #if within 1 player distance
                self.attack()                                                                   #attack
        
        if self.rect.centerx in range(player.rect.left,player.rect.right):                      #prevents rapid movement if player on top
            self.speed = 0                                                                      #by setting idle
    
    def update(self,x_shift,player,projectile_group):
        if self.status == "attack" or self.status == 'dead':                            #if needing fast animations
            self.animation_speed = MELEE_ANIMATION_SPEED                                #use fast animations
        else:
            self.animation_speed = ANIMATION_SPEED                                      #otherwise use standard speed
        super().update(x_shift,player,projectile_group)                                 #from base enemy class


       
    

class Enemy_arrow(Projectile):
    """enemy arrows, only do damage to player"""
    def __init__(self,pos,speed):
        super().__init__(pos,speed)                                     #from base class
        self.path = './graphics/day/enemies/dark archer/arrow/'             #sets path
        self.import_projectile_assets()                                 #gets assets
        
        

class Enemy_projectile(Enemy):
    """projectile enemy"""
    def __init__(self,pos,day):
        super().__init__(pos,day)                           #from base
        self.type = "projectile"                        #sets identifier
        
    def import_character_assets(self,day):                  
        #loads all assetes from multiple folders
        if day:
            self.path = './graphics/day/enemies/dark archer/'   #sets path
        else:
            self.path = './graphics/night/enemies/dark archer/'
        super().import_character_assets()               #from enemy base
    
    def decision_tree(self,player,projectile_group):
        """controls what the enemy does"""
        if self.status == "dead":                                                                   #nothing if dead
            return
        if player.rect.x > self.rect.x:                                                             #if on left 
            self.facing_right = True                                                                
            if player.rect.x - self.rect.x in range(int(DISPLAY_WIDTH*0.2),int(DISPLAY_WIDTH*0.4)): #if within range
                self.attack(projectile_group)                                                       #attack
            elif player.rect.x - self.rect.x in range(0,int(DISPLAY_WIDTH*0.2)):                    #if within closer range
                self.direction.x = -1                                                               #run away
                self.speed = PLAYER_SPEED*0.65                                                      #slower than player
            else:
                self.speed = 0                                                                      #otherwise do nothing

        elif player.rect.x < self.rect.x:                                                           #if on right
            self.facing_right = False                                                               
            if self.rect.x - player.rect.x in range(int(DISPLAY_WIDTH*0.2),int(DISPLAY_WIDTH*0.4)): #if within range
                self.attack(projectile_group)                                                       #attack
            elif self.rect.x - player.rect.x in range(0,int(DISPLAY_WIDTH*0.2)):                    #if within closer range
                self.direction.x = +1                                                               #run away
                self.speed = PLAYER_SPEED*0.65                                                      #slower than player
            else:   
                self.speed = 0                                                                      #otherwise do nothing
        
        if self.rect.centerx in range(player.rect.left,player.rect.right):                          #prevents rapid movement when player is on top
            self.speed = 0

    def attack(self,projectile_group):
        #starts the attack sequence in the enemy
        super().attack()
        if self.attack_done == False:                                                                                           #checks if allowed to attack
            if self.facing_right:           
                projectile_group.add(Enemy_arrow((self.rect.right,self.rect.centery - PROJECTILE_SIZE[1]/2),PROJECTILE_SPEED))  #spawns arrow going right
            else:
                projectile_group.add(Enemy_arrow((self.rect.left,self.rect.centery - PROJECTILE_SIZE[1]/2),-PROJECTILE_SPEED))  #spawns arrow going left
            self.attack_done =True                                                                                              #cannot constantly attack


    def update(self, x_shift, player, projectile_group):
        if self.status == 'dead':                                       #uses fast animation for death sequence
            self.animation_speed = PROJECTILE_ENEMY_ANIMATION_SPEED
        else:
            self.animation_speed = ANIMATION_SPEED                      #otherwise uses normal
        super().update(x_shift, player, projectile_group)
        if self.death_complete:
            self.kill()                                                 #removes sprite when death animation finished
        
        