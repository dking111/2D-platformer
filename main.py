

import pygame
from constants import DISPLAY_WIDTH,DISPLAY_HEIGHT, ALPHABET
from level import Level
from GUI import *

#######initialisation######
pygame.init()
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Target")
clock = pygame.time.Clock()
#########groups##############d

#GUI
text_group = pygame.sprite.Group()
btn_group = pygame.sprite.Group()
img_group = pygame.sprite.Group()
shape_group = pygame.sprite.Group()
GUI_constructor = GUI(text_group,btn_group,img_group,shape_group,game_display)

#MAINLOOP
while True:
    character_input = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    #ESCAPE KEY FOR IN GAME
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and GUI_constructor.current_page == "game":
                GUI_constructor.change_page("game_menu")
            elif event.key == pygame.K_ESCAPE and GUI_constructor.current_page == "game_menu":
                GUI_constructor.change_page("game")
    #MOUSE CLICKS
        if event.type == pygame.MOUSEBUTTONUP:
            if pygame.BUTTON_LEFT == 1:
                left_click = True  
        else:
            left_click = False
    #CHARACTER INPUT FOR ENTRY PAGE
        if event.type == pygame.KEYUP:
            if event.unicode.upper() in ALPHABET:
                character_input = event.unicode.upper()
            if event.key == pygame.K_BACKSPACE:
                character_input = "DEL"
            if event.key == pygame.K_RETURN:
                character_input = "ENTER"

    
    #takes values from button clicked on level page
    #LOADING DIFFERENT LEVELS
    match GUI_constructor.current_level:        
        case 1:
            level = Level(game_display,1)
            GUI_constructor.current_level = None
        case 2:
            level = Level(game_display,2)
            GUI_constructor.current_level = None
        case 3:
            level = Level(game_display,3)
            GUI_constructor.current_level = None
        case _:
            pass
    
    #normal game
    if GUI_constructor.current_page == "game":
        if level.display(character_input) == False:                    #if player dies, false is returned
            GUI_constructor.change_page("page_death")   #goes to death page
            level = None

    #game with in game menu
    elif GUI_constructor.current_page == "game_menu":
        if level.display(character_input) == False:                    #if player dies, false is returned
            GUI_constructor.change_page("page_death")   #goes to death page
            level = None
        #draw all shapes
        shape_group.draw(game_display)
        btn_group.draw(game_display)
        text_group.draw(game_display)
        img_group.draw(game_display)
        btn_group.update()
    else:
    #GUI
        #draw all shapes
        img_group.draw(game_display)
        shape_group.draw(game_display)
        btn_group.draw(game_display)
        text_group.draw(game_display)
        btn_group.update()

    #updates
    pygame.display.update()
    clock.tick(60)
