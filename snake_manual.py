# problems to fix:
# initialized length is 5?
# apple disappears
# when snake on left or top of apple can eat it without being on it directly?
# if starting game on length 3 only crashes on wall if you have 2 blocks on game board- should crash directly on the 1st block that touches wall
# you can't go back into yourself to die

from pygame.locals import *
from random import randint
import pygame
import time
 
class Apple:
    x = 0
    y = 0
    step = 44
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
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
        # random snake position dependent on the initial direction
        if(self.direction==0):
            self.x.append(randint(5,xDim)*self.step)
            self.y.append(0)
            for i in range(1,length):
                self.x.append(self.x[i-1]-self.step)
                self.y.append(self.y[0])
        elif(self.direction==1):
            self.x.append(randint(0,xDim-5)*self.step)
            self.y.append(0)
            for i in range(1,length):
                self.x.append(self.x[i-1]+self.step)
                self.y.append(self.y[0])
        elif(self.direction==2):
            self.y.append(randint(5,yDim)*self.step)
            self.x.append(0)
            for i in range(1,length):
                self.y.append(self.y[i-1]+self.step)
                self.x.append(self.x[0])
        else:
            self.y.append(randint(0,yDim-5)*self.step)
            self.x.append(0)
            for i in range(1,length):
                self.y.append(self.y[i-1]-self.step)
                self.x.append(self.x[0])

        for i in range(1,length):
            self.x.append(self.x[i-1]-self.step)
            self.y.append(self.y[0])
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
        print("rileftght")
 
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
 
class Game:
    # has a collision occured?
    def isCollision(self,x1,y1,x2,y2,bsize):
        # if x1 >= x2 and x1 <= x2 + bsize:
        #     if y1 >= y2 and y1 <= y2 + bsize:
        #         return True
        if x1 == x2 and y1==y2:
            return True
        return False
 
class App:
 
    windowDimY = 14
    windowDimX = 18
    windowWidth = 0
    windowHeight = 0
    player = 0
    apple = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3,self.windowDimX, self.windowDimY) 
        self.windowWidth = self.windowDimX*self.player.step
        self.windowHeight = self.windowDimY*self.player.step
        self.apple = Apple(5,5)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame Snake game!')
        self._running = True
        self._image_surf = pygame.image.load("images/game_objects/smake.png").convert()
        self._apple_surf = pygame.image.load("images/game_objects/smapple.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self): 
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
                self.apple.x = randint(0,self.windowDimX) * self.player.step
                self.apple.y = randint(0,self.windowDimY) * self.player.step
                print("apple x=",self.apple.x,"apple y=",self.apple.y)
                self.player.eatenApple = True
 
        #does snake collide with wall?
        if(self.player.x[0]<0 or self.player.x[0]>self.windowWidth or self.player.y[0]<0 or self.player.y[0]>self.windowHeight):
            print("You lose! Collision with wall: ")
            print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
            exit(0)

        self.player.update()
        pass

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
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
 
            time.sleep (50.0/1000.0)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()