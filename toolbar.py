import pygame
import math

class Toolbar:
    toolbarWidth = 0
    toolbarHeight = 0
    toolbarX = 0

    def __init__(self, width, windowWidth,windowHeight):
        self.toolbarWidth = width
        self.toolbarHeight = windowHeight
        self.toolbarX = windowWidth

    def draw_background(self, display):
        pygame.draw.rect (display, (255,255,255), (self.toolbarX, 0, self.toolbarWidth, self.toolbarHeight)) # draws a white rectangle to make the toolbar look different from the boar
    
    def draw_dpad(self, display, direction): 
        img = self.images['dpad'][direction]   
        img = pygame.transform.scale(img, (int(self.toolbarWidth/2), int(self.toolbarWidth/2))) # take image corresponding to the direction and resclae it to fit toolbar
        display.blit(img,(int(self.toolbarX+self.toolbarWidth/4),int(self.toolbarHeight/8))) #blit it so it renders
    
    def draw_food(self, display, state):
        
        img_indices = [i+4*state[i+8] for i in range(0,4)]
        for idx in img_indices:
            img = self.images['food'][idx]
            img = pygame.transform.scale(img, (int(self.toolbarWidth/2), int(self.toolbarWidth/2))) # take image corresponding to the direction and resclae it to fit toolbar
            display.blit(img,(int(self.toolbarX+self.toolbarWidth/4),int(5*self.toolbarHeight/8))) #blit it so it renders

    def draw_danger(self, display,state):
        # state = [0,1,0,1,1,1,1,1,1,1,1,1]
        #print(state)
        img_indices = state[8:]
        sqnum = len(state)-8
        side = int(math.sqrt(sqnum))
        size = int(self.toolbarWidth/(3*side))
        margin = 30
        for a in range (side):
            for b in range(side):
                num = 5*b+a
                if(state[num]==0):
                    img = self.images['food'][0]
                else:
                    img = self.images['food'][1]
                img = pygame.transform.scale(img, (size,size)) # take image corresponding to the direction and resclae it to fit toolbar
                xshift = (int(a/2)-side)*(size+margin)
                yshift = (int(b/2)-side)*(size+margin)
                display.blit(img,(int(self.toolbarX+self.toolbarWidth/4+xshift),int(self.toolbarHeight/3+yshift))) #blit it so it renders


    def draw(self, display, direction, state):
        self.draw_background(display)
        self.draw_dpad(display, direction)
        #self.draw_danger(display, state)
        self.draw_danger(display,state)
        self.draw_food(display,state)
    
    def load_images(self):
        self.images = {
            'dpad' : [],
            'danger' : [],
            'food' : []
        }

        self.images['dpad'].append(pygame.image.load("images/dpad/dpad_right.png").convert_alpha())
        self.images['dpad'].append(pygame.image.load("images/dpad/dpad_left.png").convert_alpha())
        self.images['dpad'].append(pygame.image.load("images/dpad/dpad_up.png").convert_alpha())
        self.images['dpad'].append(pygame.image.load("images/dpad/dpad_down.png").convert_alpha())

        self.images['danger'].append(pygame.image.load("images/danger4/up_not.png").convert_alpha())
        self.images['danger'].append(pygame.image.load("images/danger4/down_not.png").convert_alpha())
        self.images['danger'].append(pygame.image.load("images/danger4/left_not.png").convert_alpha())
        self.images['danger'].append(pygame.image.load("images/danger4/right_not.png").convert_alpha())
        self.images['danger'].append(pygame.image.load("images/danger4/up.png").convert_alpha())
        self.images['danger'].append(pygame.image.load("images/danger4/down.png").convert_alpha())
        self.images['danger'].append(pygame.image.load("images/danger4/left.png").convert_alpha())
        self.images['danger'].append(pygame.image.load("images/danger4/right.png").convert_alpha())

        self.images['food'].append(pygame.image.load("images/food/up_not.png").convert_alpha())
        self.images['food'].append(pygame.image.load("images/food/down_not.png").convert_alpha())
        self.images['food'].append(pygame.image.load("images/food/left_not.png").convert_alpha())
        self.images['food'].append(pygame.image.load("images/food/right_not.png").convert_alpha())
        self.images['food'].append(pygame.image.load("images/food/up.png").convert_alpha())
        self.images['food'].append(pygame.image.load("images/food/down.png").convert_alpha())
        self.images['food'].append(pygame.image.load("images/food/left.png").convert_alpha())
        self.images['food'].append(pygame.image.load("images/food/right.png").convert_alpha())
        