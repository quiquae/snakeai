# PROBLEM: player doesn't start fresh every episode- needs to be in new position, keeps just killing itself

from pygame.locals import *
from random import randint
import pygame
import time
from dqn import dqnagent
import numpy as np
 
def parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/175 #how much we decrease our exploration by every time
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 150 #size(nodes) of neural network layer 1
    params['second_layer_size'] = 150
    params['third_layer_size'] = 150
    params['episodes'] = 5 #how many trials you do ie played games
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path'] = 'weights/weights.hdf5' #file path for the weights folder
    params['load_weights'] = False
    params['train'] = True
    return(params)

#---
 
class Apple:
    x = 0
    y = 0
    step = 44
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
        print(x, y)
 
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
        print(self.x)
        print(self.y)
    def reset(self, length, xDim, yDim):
        self.length = length #not using random yet
        self.x = []
        self.y = []
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
 
class Game:
    # has a collision occured?
    def isCollision(self,x1,y1,x2,y2,bsize):
        # if x1 >= x2 and x1 <= x2 + bsize:
        #     if y1 >= y2 and y1 <= y2 + bsize:
        #         return True
        if x1 == x2 and y1==y2:
            return True
        return False

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
    
    def draw_food(self, display):
        pass

    def draw_danger(self, display,state):
        # state = [0,1,0,1,1,1,1,1,1,1,1,1]
        print(state)
        img_indices = [i + 4*state[i] for i in range(0,4)]
        
        for idx in img_indices:
            img = self.images['danger'][idx]
            img = pygame.transform.scale(img, (int(self.toolbarWidth/2), int(self.toolbarWidth/2))) # take image corresponding to the direction and resclae it to fit toolbar
            display.blit(img,(int(self.toolbarX+self.toolbarWidth/4),int(self.toolbarHeight/2))) #blit it so it renders

    def draw(self, display, direction, state):
        self.draw_background(display)
        self.draw_dpad(display, direction)
        #self.draw_danger(display, state)
        self.draw_danger(display,state)
    
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
                self._running = False
                
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
            self._running= False
        
        pass

    def on_render(self, state):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.toolbar.draw(self._display_surf, self.player.direction, state)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    # initializing agent before the 1st move
    def init_agent(self, agent):
        state_init1 = agent.get_state(game, self.player, self.food) #first state after random placement
        #first action
        
    def reset_player(self):
        self.player = Player(3,self.windowDimX, self.windowDimY)
        print(self.player.x)
        print(self.player.y)

    def on_execute(self):
        print('starting execution!')
        params = parameters()
        agent = dqnagent(params) #initialize the agent!
        if(agent.load_weights): #load weights maybe
            agent.model.load_weights(agent.weights)
            print("loaded the weights")

        counter = 0 #how many games have been played/trials done
        record = 0 #highest score
        while counter<params['episodes']: #still have more trials to do
            counter += 1

            print("\nEPISODE ", counter, "\n")

            if not params['train']: # if you're not training it, no need for exploration
                agent.epsilon = 0
            else:
                agent.epilson = 1- (counter * params['epsilon_decay_linear'])#exploration/randomness factor that decreases over time

            print("EPSILON = ", agent.epsilon, "\n")

            if self.on_init() == False:
                self._running = False

            print("PLAYER\tx : ", self.player.x,"\ty : ", self.player.y, "\n")

            while(self._running):
                pygame.event.pump()
                keys = pygame.key.get_pressed() 
                if (keys[K_ESCAPE]):
                    exit(0)
                oldstate = agent.get_state(self, self.player, self.apple)
                print("\noldstate = ", oldstate, "\n")

                # get the action
                if randint(0,1) < agent.epsilon: #every so often random exploration
                    action = randint(0,3) #random action
                    print("random action : ",action)
                else: #Actionprecited by agent
                    oldstate = oldstate.reshape(1,12)
                    predictedq= agent.model.predict(oldstate) # predicts the q values for the action in that state
                    action = np.argmax(predictedq[0]) #maximum (highest q) action
                    print("predicted action : ", action, "\tq-values : ", predictedq)

                self.player.do_move(action) #do the action
                newstate = agent.get_state(self, self.player, self.apple) #new state from the action we've taken
                print("\nnewstate = ", newstate, "\n")

                self.on_loop()
                self.on_render(newstate)
                time.sleep (4000.0/1000.0)
            self.player.reset(3,self.windowDimX, self.windowDimY )
            self.on_cleanup()
            
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()