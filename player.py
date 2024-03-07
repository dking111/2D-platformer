import pygame
from support import import_folder
from constants import ANIMATION_SPEED, GRAVITY, PLAYER_JUMP_SPEED, PLAYER_SPEED,TILE_SIZE,PLAYER_SIZE,PLAYER_HEALTH,PROJECTILE_SPEED,PROJECTILE_SIZE
from sprite import Sprite_base, Projectile

class Player(Sprite_base):
    def __init__(self,pos,day):
        super().__init__(pos,day)
        #path
        self.path  = './graphics/character/'
        #statistics
        self.health = PLAYER_HEALTH
        self.kills = 0
        self.deaths = 0
        self.distance = 0

    def import_character_assets(self,day):
        #loads all assets from multiple folders
        if day:
            self.path = './graphics/day/character/'
        else:
            self.path = './graphics/night/character/'
        super().import_character_assets()
        

    def get_input(self,projectile_group):
        #detects inputs for relevent key presses
        keys = pygame.key.get_pressed()
        #x direction
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False   
        else:
            self.direction.x = 0
        #y direction
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.on_ground:
                self.jump()
        #attack
        if keys[pygame.K_e] or keys[pygame.K_RSHIFT]:
            self.attack(projectile_group)


    def attack(self,projectile_group):
        #starts attack sequence
        super().attack()
        if self.attack_done == False:                                                                                           #if allowed to attack
            if self.facing_right:
                projectile_group.add(Projectile((self.rect.right,self.rect.centery - PROJECTILE_SIZE[1]/2),PROJECTILE_SPEED))   #spawns arrow to the right
            else:
                projectile_group.add(Projectile((self.rect.left,self.rect.centery - PROJECTILE_SIZE[1]/2),-PROJECTILE_SPEED))   #spawns arrow to the left
            self.attack_done =True
    
    def update(self,projectile_group):
        #updates all
        self.get_input(projectile_group)
        super().update()
        

    