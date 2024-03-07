import pygame
from constants import DISPLAY_HEIGHT,DISPLAY_WIDTH
from leaderboard import Leaderboard
from functools import partial
#########classes##############

class Text(pygame.sprite.Sprite):
    """generic text class """
    def __init__(self,text,centerPos,display_surface,colour,size,group):
        super().__init__()
        #takes parameters and assigns to attributes
        self.text = text
        self.pos = centerPos
        self.colour = colour
        self.size = size
        self.display_surface = display_surface
        self.group = group
        #creates font
        self.font = pygame.font.SysFont("freesansbold.ttf", self.size)
        self.create()
    
    def create(self):
        #creates text surface from parameters and automatically adds it to group
        #render text
        self.image = self.font.render(self.text,True,self.colour)
        self.rect = self.image.get_rect(center = self.pos)
        self.group.add(self)
    def update(self,new_text = ""):
        if new_text != "":
            self.text = new_text
            self.create()



class Button(pygame.sprite.Sprite):
    """generic button class that displays text of a clickable button"""
    def __init__(self,text,display_surface,colour,group,btn_rect,btn_colour,btn_active_colour,btn_group,action = None):
       #takes attributes
        super().__init__()
        self.btn_colour = btn_colour
        self.btn_active_colour = btn_active_colour
        self.rect = btn_rect
        self.btn_group = btn_group
        self.action = action
        #automatically creates button and text according to buttons dimensions
        self.create()
        Text(text,self.rect.center,display_surface,colour,int(0.8*self.rect.h),group)
    def create(self):
        #creates rectangle and automatically adds to relavent group
        #trying to make rounded corners
        self.image = pygame.Surface((self.rect[2],self.rect[3]))
        self.image.fill(self.btn_colour)
        #gets rect 
        self.rect = self.image.get_rect(center = (self.rect[0],self.rect[1]))
        self.btn_group.add(self)
    

    def update(self):
        from main import left_click #changed from previous to get mouse button up
        #takes mouse input and changes colour of box if hovered over
        #also call functions
        mouse = pygame.mouse.get_pos()
        x, y, w, h = self.rect
        if x+w > mouse[0] > x and y+h > mouse[1] > y :   #if the mouse is over  btn
            self.image.fill(self.btn_active_colour)
            if left_click and self.action != None:
                
                self.action()
                
             #and btn is down it does action
            
        else:
            self.image.fill(self.btn_colour)  #changes colour back to normal
            
class Image(pygame.sprite.Sprite):
    """creates image from given path and rect"""
    def __init__(self,path,rect,display_surface,group):
        super().__init__()
        #sets attributes
        self.path = path
        self.rect = pygame.Rect(rect)
        self.display_surface = display_surface
        self.group = group
        self.updated = False
        self.create()
    def create(self):
        #creates image and automatically gives rect        
        self.image = pygame.image.load(self.path)
        #makes correct size
        self.image = pygame.transform.scale(self.image, (self.rect[2],self.rect[3]))
        #centers
        if self.updated:
            self.rect = self.image.get_rect(topleft = (self.rect[0],self.rect[1]))
        else:
            self.rect = self.image.get_rect(center = (self.rect[0],self.rect[1]))
        self.group.add(self)

    def update(self,new_path = None):
        if new_path != None:
            self.path = new_path
            self.updated = True
            self.create()

class Shape(pygame.sprite.Sprite):
    """creates a square shape from given colour and rect"""
    def __init__(self,colour,rect,center,display_surface,group):
        super().__init__()
        #sets attributes
        self.colour = colour
        self.rect = pygame.Rect(rect)
        if center == True:
            self.rect.center = (self.rect.x,self.rect.y)
        self.display_surface = display_surface
        self.group = group
        self.updated = False
        self.create()
    def create(self):
        #creates image and automatically gives rect        
        self.image =  pygame.surface.Surface((self.rect.w,self.rect.h))
        self.image.fill(self.colour)
        self.group.add(self)
    def update(self):
        self.updated = True    
            
class Outline(pygame.sprite.Sprite):
    """creates a rectangle outline using the shape class"""
    def __init__(self,colour,rect,border,display_surface,group):
        super().__init__()
        #sets attributes
        self.rect = pygame.Rect(rect)
        self.rect.center = (self.rect.x,self.rect.y)
        self.colour = colour
        self.display_surface = display_surface
        self.group = group
        self.border =border
        self.create()
    
    def create(self):
        #creates outline from 4 shapes
        Shape(self.colour,(self.rect.x,self.rect.y,self.rect.w,self.border),False,self.display_surface,self.group)#top
        Shape(self.colour,(self.rect.x,self.rect.bottom-self.border,self.rect.w,self.border),False,self.display_surface,self.group)#bottom
        Shape(self.colour,(self.rect.x,self.rect.y,self.border,self.rect.h),False,self.display_surface,self.group)#left
        Shape(self.colour,(self.rect.right-self.border,self.rect.y,self.border,self.rect.h),False,self.display_surface,self.group)#right





class GUI:
    """a dictionary of different pages that can be called"""
    def __init__(self,text_group,btn_group,img_group,shape_group,game_display):
        #cretes index of functions to call according to page number
        #sets attributes
        self.current_page = "home"
        self.current_level = None
        #sprite groups
        self.text_group = text_group
        self.btn_group = btn_group
        self.img_group = img_group
        self.shape_group = shape_group
        self.game_display = game_display
        #dictionary of each page method so they can be caleld
        self.dict = {"home":self.page_home,"help":self.page_help,"game":self.game,"game_menu":self.game_menu,"leaderboard":self.page_leaderboard,"levels":self.page_levels,"help game":self.page_help_game,"page_death":self.page_death}
        self.display()

    def page_home(self):
        #home page
        Image(r'.\GUI\page_home.png',(DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2,DISPLAY_WIDTH,DISPLAY_HEIGHT),self.game_display,self.img_group)
        Button("Levels",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.35,DISPLAY_WIDTH*0.3,DISPLAY_HEIGHT*0.15),'red','white',self.btn_group,action = partial(self.change_page,"levels"))
        Button("Leaderboard",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.5,DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.07),'white','light grey',self.btn_group,action = partial(self.change_page,"leaderboard"))
        Button("Help",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.6,DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.07),'white','light grey',self.btn_group,action = partial(self.change_page,"help"))
        Button("Quit",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.7,DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.07),'white','light grey',self.btn_group,action = quit)
    
    def page_help(self):
        #help page
        Image(r'.\GUI\page_help.png',(DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2,DISPLAY_WIDTH,DISPLAY_HEIGHT),self.game_display,self.img_group)
        #button
        Button("Back",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.06,DISPLAY_HEIGHT*0.06,DISPLAY_WIDTH*0.1,DISPLAY_WIDTH*0.05),'white','light grey',self.btn_group,action = partial(self.change_page,"home"))
        Text('Help page',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.1),self.game_display,'red',70,self.text_group)
        #info
        Text('Target is an infinitely long platformer game , every level you get will be different!',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.2),self.game_display,'white',30,self.text_group)
        Text('Aim of the game',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.3),self.game_display,'red',50,self.text_group)
        Text('The aim of the game is to reach as high a score as possible, you can do this through killing enemies, travelling far and doing it fast!',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.35),self.game_display,'white',27,self.text_group)
        Text('Make sure to use platforms to your advantage!',(DISPLAY_WIDTH*0.6,DISPLAY_HEIGHT*0.4),self.game_display,'white',27,self.text_group)
        #controls
        Text('How to play',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.4),self.game_display,'red',50,self.text_group)
        Text('W/UP Arrow/ Spacebar  -  Jump',(DISPLAY_WIDTH*0.17,DISPLAY_HEIGHT*0.45),self.game_display,'white',25,self.text_group)
        Text('A/LEFT Arrow          -  Move Left',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.5),self.game_display,'white',25,self.text_group)
        Text('D/RIGHT Arrow         -  Move Right',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.55),self.game_display,'white',25,self.text_group)
        Text('E/Right shift         -  Shoot',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.6),self.game_display,'white',25,self.text_group)
        Image(r'.\GUI\page_help_photo.png',(DISPLAY_WIDTH*0.6,DISPLAY_HEIGHT*0.6,DISPLAY_WIDTH*0.35,DISPLAY_HEIGHT*0.35),self.game_display,self.img_group)

    def page_help_game(self):
        #help page
        Image(r'.\GUI\page_help.png',(DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2,DISPLAY_WIDTH,DISPLAY_HEIGHT),self.game_display,self.img_group)
        Button("Back",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.06,DISPLAY_HEIGHT*0.06,DISPLAY_WIDTH*0.1,DISPLAY_WIDTH*0.05),'white','light grey',self.btn_group,action = partial(self.change_page,"game_menu"))
        Text('Help page',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.1),self.game_display,'red',70,self.text_group)
        #title
        Text('Target is an infinitely long platformer game , every level you get will be different!',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.2),self.game_display,'white',30,self.text_group)
        #explanations
        Text('Aim of the game',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.3),self.game_display,'red',50,self.text_group)
        Text('The aim of the game is to reach as high a score as possible, you can do this through killing enemies, travelling far and doing it fast!',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.35),self.game_display,'white',27,self.text_group)
        Text('Make sure to use platforms to your advantage!',(DISPLAY_WIDTH*0.6,DISPLAY_HEIGHT*0.4),self.game_display,'white',27,self.text_group)
        #instructions
        Text('How to play',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.4),self.game_display,'red',50,self.text_group)
        Text('W/UP Arrow/ Spacebar  -  Jump',(DISPLAY_WIDTH*0.17,DISPLAY_HEIGHT*0.45),self.game_display,'white',25,self.text_group)
        Text('A/LEFT Arrow          -  Move Left',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.5),self.game_display,'white',25,self.text_group)
        Text('D/RIGHT Arrow         -  Move Right',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.55),self.game_display,'white',25,self.text_group)
        Text('E/Right shift         -  Shoot',(DISPLAY_WIDTH*0.2,DISPLAY_HEIGHT*0.6),self.game_display,'white',25,self.text_group)
        #image
        Image(r'.\GUI\page_help_photo.png',(DISPLAY_WIDTH*0.6,DISPLAY_HEIGHT*0.6,DISPLAY_WIDTH*0.35,DISPLAY_HEIGHT*0.35),self.game_display,self.img_group)




    def page_leaderboard(self):
        #displays the leaderboard page
        Image(r'.\GUI\page_leaderboard.png',(DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2,DISPLAY_WIDTH,DISPLAY_HEIGHT),self.game_display,self.img_group)
        #data
        leaderboard_data = Leaderboard().get_top_entries()
        player_score_data,player_rank = Leaderboard().get_player_entry()
        #background
        self.game_display.fill("light blue")
        #title
        Text('Leaderboard',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.1),self.game_display,'red',50,self.text_group)
        #leaderboard box and continue button
        #back part
        Shape("white",(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.5,DISPLAY_WIDTH*0.7,DISPLAY_HEIGHT*0.7),True,self.game_display,self.shape_group)
        Outline("black",(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.5,DISPLAY_WIDTH*0.7,DISPLAY_HEIGHT*0.7),5,self.game_display,self.shape_group)
        #continue button
        Button("Continue",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.925,DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.1),'red','white',self.btn_group,action = partial(self.change_page,"home"))
        #headings
        headers = ["Name","Score"," Distance","Kills","Time","Rank"]
        for header_index,header in enumerate(headers):
            Text(header,(DISPLAY_WIDTH*(0.2+header_index*0.12),DISPLAY_HEIGHT*0.2),self.game_display,'black',50,self.text_group)
        Outline("black",(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*(0.2),DISPLAY_WIDTH*0.7,DISPLAY_HEIGHT*0.1),3,self.game_display,self.shape_group)
        # iterates through array and creates text widgets of each data point - main section of data
        for row_index,row in enumerate(leaderboard_data):
            row_index +=1
            Outline("black",(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*(0.2+row_index*0.1),DISPLAY_WIDTH*0.7,DISPLAY_HEIGHT*0.1),1,self.game_display,self.shape_group)
            for column_index, column in enumerate(row):
                Outline("black",(DISPLAY_WIDTH*(0.21+column_index*0.12),DISPLAY_HEIGHT*0.5,DISPLAY_WIDTH*0.12,DISPLAY_HEIGHT*0.7),1,self.game_display,self.shape_group)
                Text(str(column),(DISPLAY_WIDTH*(0.2+column_index*0.12),DISPLAY_HEIGHT*(0.2+row_index*0.1)),self.game_display,'black',50,self.text_group)
            Text(str(row_index),(DISPLAY_WIDTH*(0.2+(column_index+1)*0.12),DISPLAY_HEIGHT*(0.2+row_index*0.1)),self.game_display,'black',50,self.text_group)
            Outline("black",(DISPLAY_WIDTH*(0.1999+(column_index+1)*0.12),DISPLAY_HEIGHT*0.5,DISPLAY_WIDTH*0.1,DISPLAY_HEIGHT*0.7),1,self.game_display,self.shape_group)
        # showing current players score
        Outline("red",(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*(0.2+(row_index+1)*0.1),DISPLAY_WIDTH*0.7,DISPLAY_HEIGHT*0.1),3,self.game_display,self.shape_group)
        for i in range(0,5):
            Text(str(player_score_data[i]),(DISPLAY_WIDTH*(0.2+i*0.12),DISPLAY_HEIGHT*(0.2+(row_index+1)*0.1)),self.game_display,'red',50,self.text_group)
        Text(str(player_rank),(DISPLAY_WIDTH*(0.2+(i+1)*0.12),DISPLAY_HEIGHT*(0.2+(row_index+1)*0.1)),self.game_display,'red',50,self.text_group)

    def page_levels(self):
        #the levels page
        Image(r'.\GUI\page_level.png',(DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2,DISPLAY_WIDTH,DISPLAY_HEIGHT),self.game_display,self.img_group)
        self.game_display.fill("light blue")
        Button("Back",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.06,DISPLAY_HEIGHT*0.06,DISPLAY_WIDTH*0.1,DISPLAY_WIDTH*0.05),'white','light grey',self.btn_group,action = partial(self.change_page,"home"))
        Text('Levels',(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.1),self.game_display,'red',75,self.text_group)

        #Images and buttons beneath them
        Button("Level 1",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.375,DISPLAY_WIDTH*0.8,DISPLAY_HEIGHT*0.05),'light grey','white',self.btn_group,action = partial(self.change_page,"game",1))
        Image(r'.\GUI\page_level_level_1.png',                     (DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.25,DISPLAY_WIDTH*0.8,DISPLAY_HEIGHT*0.2),self.game_display,self.img_group)

        Button("Level 2",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.649,DISPLAY_WIDTH*0.8,DISPLAY_HEIGHT*0.05),'light grey','white',self.btn_group,action = partial(self.change_page,"game",2))
        Image(r'.\GUI\page_level_level_2.png',                     (DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.525,DISPLAY_WIDTH*0.8,DISPLAY_HEIGHT*0.2),self.game_display,self.img_group)

        Button("Level 3",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.925,DISPLAY_WIDTH*0.8,DISPLAY_HEIGHT*0.05),'light grey','white',self.btn_group,action = partial(self.change_page,"game",3))
        Image(r'.\GUI\page_level_level_3.png',                     (DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.8,DISPLAY_WIDTH*0.8,DISPLAY_HEIGHT*0.2),self.game_display,self.img_group)

    def game_menu(self):
        #shows both at once
        Image(r'.\GUI\game_menu.png',(DISPLAY_WIDTH/2,DISPLAY_HEIGHT*0.4,DISPLAY_WIDTH/4,DISPLAY_HEIGHT/2),self.game_display,self.img_group)
        Button("Main Menu",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.3,200,50),'red','white',self.btn_group,partial(self.change_page,"home"))
        Button("Help",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.4,200,50),'red','white',self.btn_group,partial(self.change_page,"help game"))
        Button("Exit",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.5,200,50),'red','white',self.btn_group,action = quit)



    def game(self):
        #when this page is called, it will mean that the actual game is shown
        pass
    

    def page_death(self):
        Image(r'.\GUI\page_death.png',(DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2,DISPLAY_WIDTH,DISPLAY_HEIGHT),self.game_display,self.img_group)
        Button("Continue",self.game_display,'black',self.text_group,(DISPLAY_WIDTH*0.5,DISPLAY_HEIGHT*0.8,DISPLAY_WIDTH*0.25,DISPLAY_HEIGHT*0.1),'red','white',self.btn_group,action = partial(self.change_page,"leaderboard"))



    def change_page(self,new_page,level = None):
        #clears previous page and loads new page
        self.current_page = new_page
        self.btn_group.empty()
        self.text_group.empty()
        self.img_group.empty()
        self.shape_group.empty()
        self.display()
        #loads level if level button has been clicked
        match level:
            case None:
                pass
            case 1:
                self.current_level = 1
            case 2:
                self.current_level = 2
            case 3:
                self.current_level = 3
            

    def display(self):
        #displays current page
        self.dict[self.current_page]()
        
