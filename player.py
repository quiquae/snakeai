import pygame
from random import randint

class Player:
    x = []
    y = []
    step = 44
    direction = 0
    length = 3 
    eatenApple = False
    crashed = False
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length, xDim, yDim):
        self.length = length #not using random yet

        self.direction = randint(0,3)

        #print(self.direction)

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

        # self.direction = randint(0,3)
        # print(self.direction)
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
        #print(self.x)
        #print(self.y)
    def reset(self, length, xDim, yDim):
        self.length = length #not using random yet
        self.x = []
        self.y = []
        self.crashed = False
        self.direction = randint(0,3)

        #print(self.direction)

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


 
    def update(self):
 
        # self.updateCount = self.updateCount + 1
        # if self.updateCount > self.updateCountMax: #don't want it to update many times based on 1 action/key press
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
        # self.updateCount = 0
 
    # agent picks the move 
    def do_move(self,action):
        self.direction = action

    #drawing the snake
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 