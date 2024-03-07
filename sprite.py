import pygame
import math
from support import import_folder
from constants import ANIMATION_SPEED, GRAVITY, PLAYER_JUMP_SPEED, PLAYER_SPEED,TILE_SIZE,PLAYER_SIZE,PLAYER_HEALTH, PROJECTILE_SPEED,PROJECTILE_SIZE,PROJECTILE_ANIMATION_SPEED,DISPLAY_HEIGHT,DISPLAY_WIDTH


class Sprite_base(pygame.sprite.Sprite):
    def __init__(self,pos,day):
        super().__init__()
        #imports different assets
        self.import_character_assets(day)
        self.frame_index = 0
        self.animation_speed = ANIMATION_SPEED
        #adds all assets to dictionary
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(bottomleft = pos)
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)

        #sprite movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 0
        self.gravity = GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED

        #sprite status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        #sprite attack
        self.attack_done = False

        #sprite death
        self.death_complete = False

        #sprite stats
        self.health = 1
        self.deaths = 0

        


    def import_character_assets(self):
        #loads all assetes from multiple folders
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'attack':[],"dead":[]}    #all possible states
        for animation in self.animations.keys():                                            #gets folder for each key
            full_path = self.path + animation                                               #makes path
            self.animations[animation] = import_folder(full_path)                           #calls import folder
        
        

    def animate(self):
        #animates the sprite
        if self.status == 'dead' and self.death_complete == True:   #ensures is allowed to change image
            return
        animation = self.animations[self.status]                    #gets correct animation to use
        self.frame_index += self.animation_speed                    #updates frame index
        #end of animation
        if self.frame_index >= len(animation):                      #end of animation
            self.frame_index = 0                                    
            if self.status == 'attack':                             #resets attack status after full animation played
                self.status = 'run'                                 #resets to run as similar animation
                self.attack_done = False
            if self.status == 'dead':                               #ensures only 1 death animation played
                self.death_complete = True
                return
        
        image = animation[int(self.frame_index)]                    #gets and rescales new image
        image = pygame.transform.scale(image, PLAYER_SIZE)
        if self.facing_right:                                       #makes image face correct direction
            self.image = image
        else:
            #make new image
            self.image = pygame.transform.flip(image,True,False)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        #setting the rect so that sprite always on the floor
        #onground colliding with right
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        #onground colliding with left
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        #onground
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        #onceiling colliding with right
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        #onceiling colliding with left
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        #onceiling
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        
    def get_status(self):
        #gets statuses
        if self.status != 'attack' and self.status != 'dead':           #prevents status being changed so full attack plays or full death
            if self.direction.y < 0:
                self.status = 'jump'

            elif self.direction.y > 1: #is a one due to bug causing irregular movement
                self.status = "fall"

            else:
                if self.direction.x != 0:
                    self.status = 'run'
                else:
                    self.status = 'idle'
    
    def horizontal_movement_collision(self,sprite,tiles,world_shift):
        #controls collisions in the x direction
        sprite.rect.x += sprite.direction.x * sprite.speed        
        #checks for collisions
        for tile in tiles.sprites():
            if tile.rect.colliderect(sprite.rect):
                #detects which side the collision is on
                if tile.type == "spike":
                    self.health -= 1
                    tile.type = "dead spike"
                if sprite.direction.x < 0:
                    sprite.rect.left = tile.rect.right                                #sets sprites left X coord to tiles right X coord
                    sprite.on_left = True
                    self.current_x = sprite.rect.left
                elif sprite.direction.x > 0:
                    sprite.rect.right = tile.rect.left                                #sets sprites right X coord to tiles left X coord
                    sprite.on_right = True
                    self.current_x = sprite.rect.right  
        #resets values when no longer colliding
        if (sprite.on_left and (sprite.rect.left != self.current_x or sprite.direction.x >= 0 )) or world_shift != 0  :
            sprite.on_left = False
        if (sprite.on_right and (sprite.rect.right != self.current_x or sprite.direction.x <= 0)) or world_shift != 0  :
            sprite.on_right = False
        


    def vertical_movement_collision(self,sprite,tiles):
        #controls vertical collisions
        sprite.apply_gravity()                                                              #calls gravity
        #detects collisions
        for tile in tiles.sprites():
            if tile.rect.colliderect(sprite.rect):
                if tile.type == "spike":
                    self.health -= 1
                    tile.type = "dead spike"
                #detects where collision is
                if sprite.direction.y > 0:                                                  #sets sprite bottom to sprite top
                    sprite.rect.bottom = tile.rect.top
                    sprite.direction.y = 0
                    sprite.on_ground = True
                elif sprite.direction.y < 0:
                    sprite.rect.top = tile.rect.bottom                                    #sets sprite top to sprite bottom
                    sprite.on_ceiling = True

        #resets values
        if sprite.on_ground and sprite.direction.y < 0 or sprite.direction.y > 1:
            sprite.on_ground = False
        
        if sprite.on_ceiling and sprite.direction.y > 0:
            sprite.on_ceiling = False

    def projectile_collision(self,sprite,projectile_group):
        #detects collisions between sprite and a projectile group
        for projectile in projectile_group:
            if projectile.rect.colliderect(self.rect) and projectile.status == "moving" and self.status != "dead":
                sprite.health -=1                                                                                       #lowers health and removes projectile
                sprite.deaths +=1
                projectile.kill()       

    def apply_gravity(self):
        #calculates gravity as accelerates
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        #jumps
        self.direction.y = self.jump_speed

    def attack(self):
        self.status = "attack"
 
    def update(self):
        #updates all
        self.get_status()
        self.animate()
        if self.status == 'dead':
            self.speed = 0
            self.direction.x = 0
        if self.rect.y > DISPLAY_HEIGHT:
            self.rect.y == DISPLAY_HEIGHT/2
        if self.rect.x > DISPLAY_WIDTH:
            self.rect.x == DISPLAY_WIDTH/2
            


class Projectile(pygame.sprite.Sprite):
    """Creates a basic projectile"""
    def __init__(self,pos,speed):
        super().__init__()
        #animation
        self.path = './graphics/day/character/arrow/'
        self.import_projectile_assets()
        self.frame_index = 0
        self.animation_speed = PROJECTILE_ANIMATION_SPEED
        self.image = self.animations['moving'][self.frame_index]
        self.rect = self.image.get_rect(bottomleft = pos)
        #movement
        self.speed = speed
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        #status
        self.status = 'moving'
        if self.speed > 0:
            self.facing_right = False
        else:
            self.facing_right = True



    def import_projectile_assets(self):
        #loads all assets from multiple folders
        self.animations = {'moving':[],'stopped':[]}
        for animation in self.animations.keys():                    #loops through keys and gets folders
            full_path = self.path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        #animates projectile
        if self.status == 'dead':                       #doesnt animate if dead
            return
        animation = self.animations[self.status]        #gets correct animation
        self.frame_index += self.animation_speed        #updates frame index

        if self.frame_index >= len(animation):          #end of 1 animation cycle
            self.frame_index = 0
            if self.status == 'stopped':                #when finished stopped animation, sets dead
                self.status = 'dead'
        
        image = animation[int(self.frame_index)]                    #new image to scale
        image = pygame.transform.scale(image, PROJECTILE_SIZE)

        if self.facing_right:                                       #flips accordingly
            self.image = image
        else:
            #make new image
            self.image = pygame.transform.flip(image,True,False)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def collisions(self,tiles):
        #detects collisions between projectile and tiles
        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.speed > 0:                          #finds correct side
                    self.rect.right = tile.rect.left        #attaches to tile
                elif self.speed < 0:
                    self.rect.left = tile.rect.right
                self.status = 'stopped'                     #sets stationary
                self.speed = 0 
    
    def update(self,tiles,world_shift):
        #updates everything that needs to be
        self.animate()    
        self.collisions(tiles)                                        
        self.rect.x += world_shift
        self.rect.x += self.speed
        
        
       
 
        


                




        

    
