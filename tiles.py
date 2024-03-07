import pygame
import random

class Tile(pygame.sprite.Sprite):
    """creates a solid block where position given"""
    def __init__(self,pos,size,day):
        super().__init__()
        self.type = "tile"
        self.image = pygame.Surface((size,size))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = pos)
        self.day = day
    
    def update(self,x_shift):
        #accounts for movement of screen
        self.rect.x += x_shift


class RedTile(Tile):
    """same but red"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        self.image.fill('red')


class Tile_Grass_Top(Tile):
    """same but grass"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        if self.day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_Top_'+str(random.randint(1,3))+'.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_Top_'+str(random.randint(1,3))+'.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size,size))

class Tile_No_Side(Tile):
    """same but dirty"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        if self.day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_No_Sides_'+str(random.randint(1,3))+'.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_No_Sides_'+str(random.randint(1,3))+'.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size,size))

class Tile_Right(Tile):
    """same but grass on right"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        if self.day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_Right.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_Right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size,size))

class Tile_Left(Tile):
    """same but grass onn left"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        if self.day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_Left.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_Left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size,size))

class Tile_Top_Left(Tile):
    """same but grass on top and left"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        if self.day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_Top_Left_'+str(random.randint(1,2))+'.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_Top_Left_'+str(random.randint(1,2))+'.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size,size))

class Tile_Top_Right(Tile):
    """same but grass on top and right"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        if day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_Top_Right_'+str(random.randint(1,2))+'.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_Top_Right_'+str(random.randint(1,2))+'.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size,size))

class Tile_Top_Right_Left(Tile):
    """same but grass on top and right and left"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        if self.day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_Top_Right_Left_'+str(random.randint(1,2))+'.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_Top_Right_'+str(random.randint(1,2))+'.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size,size))

class Tile_Spikes(Tile):
    """spike tile"""
    def __init__(self,pos,size,day):
        super().__init__(pos,size,day)
        self.size = size
        self.type = "spike"
        if self.day:
            self.image = pygame.image.load('./graphics/day/tiles/Tile_Spikes.png').convert_alpha()
        else:
            self.image = pygame.image.load('./graphics/night/tiles/Tile_Spikes.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft = pos)
        self.image = pygame.transform.scale(self.image, (size,self.rect.h))
        self.rect = self.image.get_rect(bottomleft = pos)
        self.changed_img = False
    
    def update(self, x_shift):
        #updates tile, detects if image change
        super().update(x_shift)
        if self.type == "dead spike" and self.changed_img == False:                                                                 #if status changed then changes image
            if self.day:
                self.image = pygame.image.load('./graphics/day/tiles/Tile_Spikes_Dead_'+str(random.randint(1,2))+'.png').convert_alpha()
            else:
                self.image = pygame.image.load('./graphics/night/tiles/Tile_Spikes_Dead_'+str(random.randint(1,2))+'.png').convert_alpha()
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            self.image = pygame.transform.scale(self.image, (self.size,self.rect.h))
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            self.changed_img = True
            
        

