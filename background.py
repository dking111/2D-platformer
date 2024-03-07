import pygame
from constants import DISPLAY_WIDTH,DISPLAY_HEIGHT
from support import import_folder

class Backgrounds(pygame.sprite.Sprite):
    """individual sprites"""
    def __init__(self,folder_path):
        super().__init__()
        self.path = folder_path
        self.images = self.get_images()
        self.image = self.images[0]
        self.image2 = self.images[1]
        self.image_index = 1
        self.rect = self.image.get_rect(topleft = (0,0))

    def get_images(self):
        #loads image
        return import_folder(self.path)
    
    def set_image(self):
        #sets appropriate image
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[self.image_index]


    
class Scenery:
    """controls how background sprites work and move"""
    def __init__(self,display_surface,day):
        self.day = day
        self.display_surface = display_surface
        if self.day:
            self.bg = Backgrounds(f'./graphics/day/backgrounds/backgrounds')
            self.mg = Backgrounds(f'./graphics/day/backgrounds/midgrounds')
        else:
            self.bg = Backgrounds(f'./graphics/night/backgrounds/backgrounds')
            self.mg = Backgrounds(f'./graphics/night/backgrounds/midgrounds')           

    def draw(self):
        #draws all scenery
        iterable = [self.bg,self.mg]
        #repeating backgrounds
        for i in iterable:
            x1 = i.rect.x
            x2 = x1 +DISPLAY_WIDTH
            if x1 > 0:
                x2 = x1 - DISPLAY_WIDTH

            if x1 <= -DISPLAY_WIDTH:
                x1 = DISPLAY_WIDTH
                i.set_image()
            if x2 <= -DISPLAY_WIDTH:
                x2 = DISPLAY_WIDTH
            #scales correctly
            i.image = pygame.transform.scale(i.image, (DISPLAY_WIDTH,DISPLAY_HEIGHT))
            i.image2 = pygame.transform.scale(i.image2, (DISPLAY_WIDTH,DISPLAY_HEIGHT))
            #blits
            self.display_surface.blit(i.image,(x1,0)) # screen 1        
            self.display_surface.blit(i.image2,(x2,0)) #screen 2

            i.rect.x = x1


    def update(self,x_shift):
        self.draw()
        self.bg.rect.x += x_shift / 3    #2.5
        self.mg.rect.x += x_shift / 2       #2





    
