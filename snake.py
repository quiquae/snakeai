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
    params['episodes'] = 150 #how many trials you do ie played games
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path'] = 'weights/weights.hdf5' #file path for the weights folder
    params['load_weights'] = False
    params['train'] = True
    return(params)
     
 #-----------------------
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
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(1000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*44
       self.x[2] = 2*44
 
    def update(self):
        print("x=",self.x[:self.length])
        print("y=",self.y[:self.length2])
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
    def do_move(self,action):
        self.direction = action
        
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
 
class App:
 
    windowWidth = 800
    windowHeight = 600
    player = 0
    apple = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame Snake game!')
        self._running = True
        self._image_surf = pygame.image.load("pink.png").convert()
        self._apple_surf = pygame.image.load("pink.png").convert()
        print('initialized game.')
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        print('started loop')
        self.player.update()
        print("LENGTH=",self.player.length)
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],44):
                self.apple.x = randint(2,9) * 44
                self.apple.y = randint(2,9) * 44
                self.player.length = self.player.length + 1
 
        print("length=",self.player.length)
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)
        print ('end of loop')
        pass
 
    def on_render(self):
        self._display_surf.fill((70,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    # initializing the agent before the first move?
    def init_agent(self, agent, player, game, food, batch_size):
        state_init1 = agent.get_state(game,player,food) #first state after random placement
        #first action
        player.do_move

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
            

            if not params['train']: # if you're not training it, no need for exploration
                agent.epsilon = 0
            else:
                agent.epilson = 1- (counter * params['epsilon_decay_linear'])#exploration/randomness factor that decreases over time


            if self.on_init() == False:
                self._running = False

            while( self._running ):
                pygame.event.pump()
                oldstate = agent.get_state(self, self.player,self.apple)
                # get the action
                if randint(0,1)<agent.epsilon: #every so often random exploration
                    action = randint(0,3) #random action
                    print("random action= ",action)
                else: #Actionprecited by agent
                    oldstate = oldstate.reshape(1,12)
                    predictedq= agent.model.predict(oldstate) # predicts the q values for the action in that state
                    print("predicted q-value for action= ",predictedq)
                    action = np.argmax(predictedq[0]) #maximum (highest q) action
                    print("predicted action= ",action)

                self.player.do_move(action) #do the action
                newstate = agent.get_state(self, self.player, self.apple) #new state from the action we've taken

                self.on_loop()
                self.on_render()
    
                time.sleep (50.0 / 1000.0)
            self.on_cleanup()
 
if __name__ == "__main__" :
    print('we got to main')
    theApp = App()
    print('about to execute')
    theApp.on_execute()
    


