
from toolbar import Toolbar
from apple import Apple
from game import Game
from pygame.locals import *
from random import randint
import pygame
import time
import numpy as np
dim = 5
 
class Player:
    x = []
    y = []
    step = 44
    direction = 0
    length = 3 
    eatenApple = False
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length, xDim, yDim):
        self.length = length #not using random yet
        self.direction = randint(0,3)
        print(self.direction)

        x0 = randint(self.length, xDim-self.length)*self.step
        y0 = randint(self.length, yDim-self.length)*self.step

        self.x.append(x0)
        self.y.append(y0)

        for i in range(1,length):
            if self.direction == 0: #right
                self.x.append(self.x[i-1]-self.step)
                self.y.append(self.y[0])
            elif self.direction == 1: #left
                self.x.append(self.x[i-1]+self.step)
                self.y.append(self.y[0])
            elif self.direction == 2: #up
                self.x.append(self.x[0])
                self.y.append(self.y[i-1]+self.step)
            elif self.direction == 3: #down
                self.x.append(self.x[0])
                self.y.append(self.y[i-1]-self.step)

        # # random snake position dependent on the initial direction
        # if(self.direction==0):
        #     self.x.append(randint(5,xDim)*self.step)
        #     self.y.append(0)
        #     for i in range(1,length):
        #         self.x.append(self.x[i-1]-self.step)
        #         self.y.append(self.y[0])
        # elif(self.direction==1):
        #     self.x.append(randint(0,xDim-5)*self.step)
        #     self.y.append(0)
        #     for i in range(1,length):
        #         self.x.append(self.x[i-1]+self.step)
        #         self.y.append(self.y[0])
        # elif(self.direction==2):
        #     self.y.append(randint(5,yDim)*self.step)
        #     self.x.append(0)
        #     for i in range(1,length):
        #         self.y.append(self.y[i-1]+self.step)
        #         self.x.append(self.x[0])
        # else:
        #     self.y.append(randint(0,yDim-5)*self.step)
        #     self.x.append(0)
        #     for i in range(1,length):
        #         self.y.append(self.y[i-1]-self.step)
        #         self.x.append(self.x[0])

        # for i in range(1,length):
        #     self.x.append(self.x[i-1]-self.step)
        #     self.y.append(self.y[0])
       # initial positions, no collision: random x and y head and body follows
        print(self.x)
        print(self.y)

 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax: #don't want it to update many times based on 1 action/key press
            if(self.eatenApple):
                self.length = self.length + 1
                self.x.append(self.x[-1])
                self.y.append(self.y[-1])
                self.eatenApple = False
            # update position to be the previouis one
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake based on direction, move it in that direction by step amount
            if self.direction == 0:
                self.x[0] += self.step
            if self.direction == 1:
                self.x[0] -= self.step
            if self.direction == 2:
                self.y[0] -= self.step
            if self.direction == 3:
                self.y[0] += self.step
            self.updateCount = 0
 
    # moving in dfferent directions
    def moveRight(self):
        self.direction = 0
        print("right")
 
    def moveLeft(self):
        self.direction = 1
        print("left")
 
    def moveUp(self):
        self.direction = 2
        print("up")
 
    def moveDown(self):
        self.direction = 3 
        print("down")
 
    #drawing the snake
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class App:
    windowDimY = 14
    windowDimX = 18
    windowWidth = 0
    windowHeight = 0
    toolbarWidth = 200
    player = 0
    apple = 0
    toolbar = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        
        self.game = Game()
        self.player = Player(3,self.windowDimX, self.windowDimY) 
        self.windowWidth = self.windowDimX*self.player.step
        self.windowHeight = self.windowDimY*self.player.step
        self.toolbar = Toolbar(self.toolbarWidth, self.windowWidth, self.windowHeight)
        self.apple = Apple(randint(0,self.windowDimX-1), randint(0,self.windowDimY-1))
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth+self.toolbarWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame Snake game!')
        self._running = True
        self._image_surf = pygame.image.load("images/game_objects/smake.png").convert()
        self._apple_surf = pygame.image.load("images/game_objects/smapple.png").convert()
        self.toolbar.load_images()        
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self): 
        self.player.update()

        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],self.player.step-1):
                print("You lose! Collision with yourself: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)
                
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],self.player.step-1):
                self.apple.x = randint(0,self.windowDimX-1) * self.player.step
                self.apple.y = randint(0,self.windowDimY-1) * self.player.step
                print("apple x=",self.apple.x,"apple y=",self.apple.y)
                self.player.eatenApple = True
 
        #does snake collide with wall?
        if(self.player.x[0]<0 or self.player.x[0]>=self.windowWidth or self.player.y[0]<0 or self.player.y[0]>=self.windowHeight):
            print("You lose! Collision with wall: ")
            print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
            exit(0)

        pass
    def state(self):
        middle = int(dim/2)
        grid = np.zeros((dim,dim),dtype=bool)
        print("x=",self.player.x,"y=",self.player.y)
        relativex = [int((a-self.player.x[0])/self.player.step+middle) for a in self.player.x]
        relativey = [int((a-self.player.y[0])/self.player.step+middle) for a in self.player.y]
        for x,y in zip(relativex, relativey):
            if(x>=0 and y>=0 and x<dim and y<dim):
                grid[y,x]= True
        print("x",relativex, "y",relativey)

        right = int(self.windowDimX-(self.player.x[0]/self.player.step)+middle)
        down = int(self.windowDimY-(self.player.y[0]/self.player.step)+middle)
        up = int(middle-(self.player.y[0]/self.player.step))
        left = int(middle-(self.player.x[0]/self.player.step))
        if(right<dim and right>=0):
            grid[:,right:] = True
        if(left<dim and left>=0):
            grid[:,:left] = True
        if(down<dim and down>=0):
            grid[down:,:] = True
        if(up<dim and up>=0):
            grid[:up,:] = True
        print(right,left,up,down)
        
        print("GRID after")
        print(grid)
        grid = list(grid.flatten())

        state = [

            self.player.direction == 0, #right
            self.player.direction == 1, #left
            self.player.direction == 2, #up
            self.player.direction == 3, #down

            self.apple.y < self.player.y[0], #food is up from the player
            self.apple.y > self.player.y[0], #food is down from the player
            self.apple.x < self.player.x[0], #food is to the left of the player
            self.apple.x > self.player.x[0] #food is to the right of the player
             
        ]
        state += grid
        for i in range(len(state)): #convert list to 0s and 1s
            if(state[i]):
                state[i] = 1
            else:
                state[i]=0
        return np.asarray(state)
            
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        print(self.state())
        self.toolbar.draw(self._display_surf, self.player.direction,self.state())
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (70.0/1000.0)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()